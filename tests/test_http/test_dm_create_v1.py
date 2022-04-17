"""
u_ids contains the user(s) that this DM is directed to, and will not include the creator. The creator is the owner of the DM. name should be automatically generated based on the users that are in this DM. The name should be an alphabetically-sorted, comma-and-space-separated list of user handles, e.g. 'ahandle1, bhandle2, chandle3'.
"""
import random
import pytest
import requests
import json
from src.config import url
from src.error import AccessError, InputError

@pytest.fixture(name = 'login_list')
def login_users():
    '''
    
    This function is to pre-login 4 users for further tests
    
    returns:
        login_list, contains 4 pre-register users' information
        
    '''
    login_list = []
    requests.delete(f"{url}clear/v1", json = {})    # clear all info in server
    requests.post(f"{url}auth/register/v2",
                                   json = { 'email': 'z5374603@unsw.com',
                                            'password': '123456',
                                            'name_first': 'Steve',
                                            'name_last': 'Yang'})
    requests.post(f"{url}auth/register/v2",
                                   json = { 'email': 'z5374602@unsw.com',
                                            'password': '123456',
                                            'name_first': 'Brian',
                                            'name_last': 'Lee'})
    requests.post(f"{url}auth/register/v2",
                                   json = { 'email': 'z5374601@unsw.com',
                                            'password': '123456',
                                            'name_first': 'Bojin',
                                            'name_last': 'Li'})
    requests.post(f"{url}auth/register/v2",
                                   json = {  'email': 'z5374600@unsw.com',
                                            'password': '123456',
                                            'name_first':'Cicy',
                                            'name_last': 'Zhou'})
    login_list.append(requests.post(url + "auth/login/v2",
                                    json = {"email": "z5374603@unsw.com",
                                            "password": "123456"}).json())
    login_list.append(requests.post(url + "auth/login/v2",
                                    json = {"email": "z5374602@unsw.com",
                                            "password": "123456"}).json())
    login_list.append(requests.post(url + "auth/login/v2",
                                    json = {"email": "z5374601@unsw.com",
                                            "password": "123456"}).json())
    login_list.append(requests.post(url + "auth/login/v2",
                                    json = {"email": "z5374600@unsw.com",
                                            "password": "123456"}).json())
    return login_list

def test_dm_create_successfully(login_list):
    '''
    
    This test is for testing create a dm successfully
    
    Parameters:
        login_list
        
    Return:
        N/A
        
    '''
    response_1 = requests.post(f'{url}dm/create/v1',
                               json = {'token': login_list[0]['token'],
                                       'u_ids': [login_list[1]['auth_user_id'], login_list[2]['auth_user_id']],})
    response_2 = requests.post(f'{url}dm/create/v1',
                               json = {'token': login_list[0]['token'],
                                       'u_ids': [],})
    assert response_1.status_code == 200
    assert response_2.status_code == 200

def test_dm_create_invalid_uid(login_list):
    """
        Test invalid user id
        
        Raises:
            InputError
    """
    invalid_u_ids = []
    while(len(invalid_u_ids) < 3):
        new_id = random.random()
        if not new_id in [login_list[i]['auth_user_id'] for i in range(0,4)]:
            invalid_u_ids.append(new_id)
    response_1 = requests.post(url + "dm/create/v1",
                               json = {'token': login_list[0]['token'],
                                       'u_ids': invalid_u_ids})
    response_2 = requests.post(url + "dm/create/v1",
                               json = {'token': login_list[0]['token'],
                                       'u_ids': [invalid_u_ids[0],login_list[1]['auth_user_id']]})
    assert response_1.status_code == InputError.code
    assert response_2.status_code == InputError.code

def test_dm_create_duplicated_uid(login_list):
    """
    
        Test duplicated user id
        
        Raises:
            InputError
            
    """
    response_1 = requests.post(url + "dm/create/v1",
                               json = {'token': login_list[0]['token'],
                                       'u_ids': [login_list[1]['auth_user_id'], login_list[1]['auth_user_id']]})
    assert response_1.status_code == InputError.code
    
def test_dm_create_wrong_uid(login_list):
    """
    
        Test wrong user id
        
        Raises:
            InputError
            
    """
    response_1 = requests.post(url + "dm/create/v1",
                               json = {'token': login_list[0]['token'],
                                       'u_ids': [-1, -2]})
    assert response_1.status_code == InputError.code
    
def test_dm_create_invalid_token(login_list):
    """
    
        Test invalid token
        
        Raises:
            AccessError
            
    """
    # normal situation
    response_1 = requests.post(f'{url}dm/create/v1',
                               json = {'token': -1,
                                       'u_ids': [login_list[1]['auth_user_id'], login_list[2]['auth_user_id']],})
    assert response_1.status_code == AccessError.code
    
    # invalid_u_id
    invalid_u_ids = []
    while(len(invalid_u_ids)<3):
        new_id = random.randint(-65535, 65535)
        if not new_id in [login_list[i]['auth_user_id'] for i in range(0,3)]:
            invalid_u_ids.append(new_id)
    response_1 = requests.post(url + "dm/create/v1",
                               json = {'token': -1,
                                       'u_ids': invalid_u_ids})
    assert response_1.status_code == AccessError.code
    
    # duplicated uid
    response_1 = requests.post(url + "dm/create/v1",
                               json = {'token': -1,
                                       'u_ids': [login_list[1]['auth_user_id'], login_list[1]['auth_user_id']]})
    assert response_1.status_code == AccessError.code
    
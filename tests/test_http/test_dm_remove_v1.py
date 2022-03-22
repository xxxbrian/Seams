import pytest
import requests
import json
import random
from src.config import url
from src.error import InputError, AccessError

@pytest.fixture(name = 'user_list')
def create_user_list():
    '''
    This function is to pre-register 4 users for further tests
    
    returns:
    user_list (dictionary), contains 4 pre-register users' information
    '''
    requests.delete(f"{url}clear/v1", json = {})    # clear all info in server
    user_list = list()
    user_list.append(requests.post(f"{url}auth/register/v2",
                                   json = { 'email': 'z5374603@unsw.com',
                                            'password': '123456',
                                            'name_first': 'Steve',
                                            'name_last': 'Yang'}))
    user_list.append(requests.post(f"{url}auth/register/v2",
                                   json = { 'email': 'z5374602@unsw.com',
                                            'password': '123456',
                                            'name_first': 'Brian',
                                            'name_last': 'Lee'}))
    user_list.append(requests.post(f"{url}auth/register/v2",
                                   json = { 'email': 'z5374601@unsw.com',
                                            'password': '123456',
                                            'name_first': 'Bojin',
                                            'name_last': 'Li'}))
    user_list.append(requests.post(f"{url}auth/register/v2",
                                   json = {  'email': 'z5374600@unsw.com',
                                            'password': '123456',
                                            'name_first':'Cicy',
                                            'name_last': 'Zhou'}))
    return user_list

@pytest.fixture(name = 'login_list')
def login_users():
    '''
    
    This function is to pre-login 4 users for further tests
    
    returns:
        login_list, contains 4 pre-register users' information
        
    '''
    login_list = []
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

@pytest.fixture(name = 'dm_list')
def create_dm(login_list):
    '''
    This function is to pre-create some dms for further tests
    
    Return:
        dm_list, contain dm_id and name
    '''
    dm_list = []
    # dm_list[0]: user[0], user[1], user[2]
    dm_list.append(requests.post(url + "dm/create/v1",
                                 json = {'token': login_list[0]['token'],
                                         'u_ids': [login_list[1]['auth_user_id'], login_list[2]['auth_user_id']]}).json())
    # dm_list[1]: user[0], user[2]. user[3]
    dm_list.append(requests.post(url + "dm/create/v1",
                                 json = {'token': login_list[0]['token'],
                                         'u_ids': [login_list[3]['auth_user_id'], login_list[2]['auth_user_id']]}).json())
    
    # dm_list[2]: user[1], user[2]. user[3]
    dm_list.append(requests.post(url + "dm/create/v1",
                                 json = {'token': login_list[1]['token'],
                                         'u_ids': [login_list[2]['auth_user_id'], login_list[3]['auth_user_id']]}).json())
    
    return dm_list


def test_dm_remove_normal(user_list, login_list, dm_list):
    '''
    
    Test remove successfully
    
    Parameters:
        user_list, login_list, dm_list
        
    Assumption:
        dm/list/v1 is working well

    '''
    dm_1 = 'bojinli, cicyzhou, steveyang'
    requests.delete(url + 'dm/remove/v1',
                    json = {"token": login_list[0]["token"], 
                            "dm_id": dm_list[0]['dm_id']})
    response_1 = requests.get(url + "dm/list/v1",
                              params = {'token': login_list[0]['token']}).json()
    # remove dm[0]
    assert response_1 == {
        'dms':[
        {
            'dm_id': dm_list[1]['dm_id'],
            'name': dm_1
        },
    ]}

def test_dm_remove_invalid_dm_id(user_list, login_list, dm_list):
    """
    
    Test dm_remove_v1 input a invalid dm ID.
    
    Parameters:
        user_list, login_list, dm_list
    
    Raises:
        InputError
        
    """
    new_id = random.randint(-65535, 65535)
    invalid_dm_id = []
    while len(invalid_dm_id) < 1:
        if not new_id in [dm_list[i]['dm_id'] for i in range(0,3)]:
            invalid_dm_id.append(new_id)
    response_1 = requests.delete(url + 'dm/remove/v1',
                                 json = {"token": login_list[0]["token"], 
                                         "dm_id": invalid_dm_id[0]})
    assert response_1.status_code == InputError.code

def test_dm_remove_author_not_creator(user_list, login_list, dm_list):
    """
    
    Test dm/remove/v1 when the user is not the original DM creator 
    
    Raise:
        AccessError
        
    """

    response_1 = requests.delete(url + 'dm/remove/v1',
                                 json = {"token": login_list[3]["token"], 
                                         "dm_id": dm_list[1]["dm_id"]})
    assert response_1.status_code == AccessError.code

def test_dm_remove_creater_no_longer_in_dm(user_list, login_list, dm_list):
    '''
    
    Test when creater leave the dm
    
    Raises:
        AccessError
        
    Assumption:
        dm/leave/v1 is working well
        
    '''
    # user[1] leaves the dm[2]
    requests.post(url + "dm/leave/v1",
                  json = {'token': login_list[1]['token'],
                          'dm_id': dm_list[2]['dm_id']})
    response_1 = requests.delete(url + 'dm/remove/v1',
                                 json = {"token": login_list[1]["token"], 
                                         "dm_id": dm_list[2]["dm_id"]})
    assert response_1.status_code == AccessError.code
    
def test_dm_remove_creater_invalid_token(user_list, login_list, dm_list):
    '''
    
    This test is to test when token is invalid 
    
    Raises:
        AccessError
        
    '''
    # normal
    response_1 = requests.delete(url + 'dm/remove/v1',
                                 json = {"token": -1, 
                                         "dm_id": dm_list[0]['dm_id']})
    assert response_1.status_code == AccessError.code
    
    # Invalid dm ID
    new_id = random.randint(-65535, 65535)
    invalid_dm_id = []
    while len(invalid_dm_id) < 1:
        if not new_id in [dm_list[i]['dm_id'] for i in range(0,3)]:
            invalid_dm_id.append(new_id)
    response_2 = requests.delete(url + 'dm/remove/v1',
                                 json = {"token": -1, 
                                         "dm_id": invalid_dm_id[0]})
    assert response_2.status_code == AccessError.code
    
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
    user_list = []
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

def test_dm_details_normal(user_list, login_list, dm_list):
    '''
    
    This test is to test when everything is fine and return correct info
    
    Assumption:
        dm/create/v1 is working well
    '''
    dm_0 = 'bojinli, brianlee, steveyang'
    dm_1 = 'bojinli, cicyzhou, steveyang'
    dm_2 = 'bojinli, brianlee, cicyzhou'
    response_1 = requests.get(url + 'dm/details/v1',
                              params = {'token': login_list[0]['token'],
                                        'dm_id': dm_list[0]['dm_id']}).json()
    response_2 = requests.get(url + 'dm/details/v1',
                              params = {'token': login_list[0]['token'],
                                        'dm_id': dm_list[1]['dm_id']}).json()
    response_3 = requests.get(url + 'dm/details/v1',
                              params = {'token': login_list[1]['token'],
                                        'dm_id': dm_list[2]['dm_id']}).json()
    assert response_1 == {
        'name': dm_0,
        'members':
            [
                {
                    'u_id': login_list[1]['auth_user_id'],
                    'email': "z5374602@unsw.com",
                    'name_first': 'Brian',
                    'name_last': 'Lee',
                    'handle_str': 'brianlee'
                },
                {
                    'u_id': login_list[2]['auth_user_id'],
                    'email': "z5374601@unsw.com",
                    'name_first': 'Bojin',
                    'name_last': 'Li',
                    'handle_str': 'bojinli'
                },
                {
                    'u_id': login_list[0]['auth_user_id'],
                    'email': "z5374603@unsw.com",
                    'name_first': 'Steve',
                    'name_last': 'Yang',
                    'handle_str': 'steveyang'
                },
            ]
    }
    assert response_2 == {
        'name': dm_1,
        'members':
            [
                {
                    'u_id': login_list[3]['auth_user_id'],
                    'email': "z5374600@unsw.com",
                    'name_first': 'Cicy',
                    'name_last': 'Zhou',
                    'handle_str': 'cicyzhou'
                },
                {
                    'u_id': login_list[2]['auth_user_id'],
                    'email': "z5374601@unsw.com",
                    'name_first': 'Bojin',
                    'name_last': 'Li',
                    'handle_str': 'bojinli'
                },
                {
                    'u_id': login_list[0]['auth_user_id'],
                    'email': "z5374603@unsw.com",
                    'name_first': 'Steve',
                    'name_last': 'Yang',
                    'handle_str': 'steveyang'
                },
            ]
    }
    assert response_3 == {
        'name': dm_2,
        'members':
            [
                {
                    'u_id': login_list[2]['auth_user_id'],
                    'email': "z5374601@unsw.com",
                    'name_first': 'Bojin',
                    'name_last': 'Li',
                    'handle_str': 'bojinli'
                },
                {
                    'u_id': login_list[3]['auth_user_id'],
                    'email': "z5374600@unsw.com",
                    'name_first': 'Cicy',
                    'name_last': 'Zhou',
                    'handle_str': 'cicyzhou'
                },
                {
                    'u_id': login_list[1]['auth_user_id'],
                    'email': "z5374602@unsw.com",
                    'name_first': 'Brian',
                    'name_last': 'Lee',
                    'handle_str': 'brianlee'
                },
            ]
    }
    
def test_dm_details_invalid_dm_id(user_list, login_list, dm_list):
    '''
    
    This test is to test when input a invalid dm_id
    
    Raises:
        InputError
        
    '''
    
    
    
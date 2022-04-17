import pytest
import requests
import json
from src.config import url
from src.error import AccessError

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

def test_dm_list_normal(login_list, dm_list):
    '''
    
    Test for all correct
    
    Parameters:
        login_list, dm_list
        
    Return:
        N/A
    
    '''
    dm_0 = 'bojinli, brianlee, steveyang'
    dm_1 = 'bojinli, cicyzhou, steveyang'
    dm_2 = 'bojinli, brianlee, cicyzhou'
    
    response_1 = requests.get(url + "dm/list/v1",
                              params = {'token': login_list[0]['token']}).json()
    response_2 = requests.get(url + "dm/list/v1",
                              params = {'token': login_list[1]['token']}).json()
    response_3 = requests.get(url + "dm/list/v1",
                              params = {'token': login_list[2]['token']}).json()
    response_4 = requests.get(url + "dm/list/v1",
                              params = {'token': login_list[3]['token']}).json()
   
    assert response_1 == {
        'dms':[
        {
            'dm_id': dm_list[0]['dm_id'],
            'name': dm_0
        },
        {
            'dm_id': dm_list[1]['dm_id'],
            'name': dm_1
        },
    ]}
    assert response_2 == {
        'dms':[
        {
            'dm_id': dm_list[0]['dm_id'],
            'name': dm_0
        },
        {
            'dm_id': dm_list[2]['dm_id'],
            'name': dm_2
        },
    ]}
    assert response_3 == {
        'dms':[
        {
            'dm_id': dm_list[0]['dm_id'],
            'name': dm_0
        },
        {
            'dm_id': dm_list[1]['dm_id'],
            'name': dm_1
        },
        {
            'dm_id': dm_list[2]['dm_id'],
            'name': dm_2
        },
    ]}
    assert response_4 == {
        'dms':[
        {
            'dm_id': dm_list[1]['dm_id'],
            'name': dm_1
        },
        {
            'dm_id': dm_list[2]['dm_id'],
            'name': dm_2
        },
    ]}
    
def test_dm_list_invalid_token():
    '''
    
    This test is to test input token is invalid
    
    Raises:
        AccessError
    
    '''
    response_1 = requests.get(url + "dm/list/v1",
                              params = {'token': -1})
    assert response_1.status_code == AccessError.code
    
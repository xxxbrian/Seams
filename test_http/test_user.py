import re
import pytest
import requests
import json
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
                                   json = 
                                       {'email': 'z5374603@unsw.com',
                                        'password': '123456',
                                        'name_first': 'Steve',
                                        'name_last': 'Yang'}).json())
    user_list.append(requests.post(f"{url}auth/register/v2",
                                   json = 
                                       {'email': 'z5374602@unsw.com',
                                        'password': '123456',
                                        'name_first': 'Brian',
                                        'name_last': 'Lee'}).json())
    user_list.append(requests.post(f"{url}auth/register/v2",
                                   json = 
                                       {'email': 'z5374601@unsw.com',
                                        'password': '123456',
                                        'name_first': 'Bojin',
                                        'name_last': 'Li'}).json())
    user_list.append(requests.post(f"{url}auth/register/v2",
                                   json = 
                                       {'email': 'z5374600@unsw.com',
                                        'password': '123456',
                                        'name_first':'Cicy',
                                        'name_last': 'Zhou'}).json())
    return user_list

def users(user_list):
    '''
    Make a list of users' info 
    
    Return:
        users 
        Type: list[dict]
    '''
    users = [
        {
            'u_id': user_list[0]['auth_user_id'],
            'email': 'z5374603@unsw.com',
            'name_first': 'Steve',
            'name_last': 'Yang',
            'handle_str': 'steveyang'
        },
        {
            'u_id': user_list[1]['auth_user_id'],
            'email': 'z5374602@unsw.com',
            'name_first': 'Brian',
            'name_last': 'Lee',
            'handle_str': 'brianlee'
        },
        {
            'u_id': user_list[2]['auth_user_id'],
            'email': 'z5374601@unsw.com',
            'name_first': 'Bojin',
            'name_last': 'Li',
            'handle_str': 'bojinli'
        },
        {
            'u_id': user_list[3]['auth_user_id'],
            'email': 'z5374600@unsw.com',
            'name_first':'Cicy',
            'name_last': 'Zhou',
            'handle_str': 'cicyzhou'
        }
    ]
    return users

################################################ users/all/v1 test ################################################
 
def test_users_all_valid_token(user_list, users):
    '''
    This test is testing token is valid for user/all/v1
    
    parameters:
        user_list
        
    returns:
        N/A
    '''
    respon = requests.get(url + "users/all/v1", params = {
        'token': user_list[0]['token']
    })

    # assert all users in the response return
    for i in range(4):
        assert users[i] in respon.json()

def test_users_all_invalid_token(user_list):
    '''
    Test users/all/v1 takes in an invalid token
    
    Raises:
        AccessError
    '''
    respon = requests.get(url + 'users/all/v1', params = {
        'token': -100})
    
    assert respon.status_code == AccessError.code
    
################################################ users/profile/v1 test ################################################ 

def test_users_profile_valid_token_and_uid(user_list, users):
    '''
    Test when u_id and token are both correct
    
    parameters:
        user_list
        
    returns:
        N/A
    '''
    response_1 = requests.get(url + "users/profile/v1", 
                              params = {
                                  'token': user_list[0]['token'],
                                  'u_id': user_list[0]['auth_user_id']
                              })
    response_2 = requests.get(url + "users/profile/v1", 
                              params = {
                                  'token': user_list[1]['token'],
                                  'u_id': user_list[1]['auth_user_id']
                              })
    
    assert response_1.json() == users[0]
    assert response_2.json() == users[1]
    
def test_users_profile_invalid_uid(user_list):
    '''
    Test when input u_id is wrong but token is correct
    
    Raises:
        InpuError
    '''
    response_1 = requests.get(url + "users/profile/v1", 
                              params = {
                                  'token': user_list[0]['token'],
                                  'u_id': -100
                              })
    assert response_1.status_code == InputError.code
    
def test_users_profile_invalid_token(user_list):
    '''
    Test when input token is wrong but u_id is correct
    and when token and u_id are both wrong
    
    Raises:
        AccessError
    '''
    response_1 = requests.get(url + "users/profile/v1", 
                              params = {
                                  'token': -100,
                                  'u_id': user_list[0]['auth_user_id']
                              })
    response_2 = requests.get(url + "users/profile/v1", 
                              params = {
                                  'token': -100,
                                  'u_id': -100
                              })
    
    assert response_1.status_code == AccessError.code
    assert response_2.status_code == AccessError.code
    
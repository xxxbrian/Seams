"""
u_ids contains the user(s) that this DM is directed to, and will not include the creator. The creator is the owner of the DM. name should be automatically generated based on the users that are in this DM. The name should be an alphabetically-sorted, comma-and-space-separated list of user handles, e.g. 'ahandle1, bhandle2, chandle3'.
"""

import pytest
import requests
import json
from src.config import url
from src.error import InputError

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

@pytest.fixture(name = 'info')
def one_user_create_dm(user_list):
    dict_list = user_list
    """User01 logs in"""
    r = requests.post(url + 'auth/login/v2', 
                    json = {'email': 'z5374603@unsw.com',
                            'password': '123456',})
    payload = r.json()
    token = payload['token']
    auth_user_id = payload['auth_user_id']
    # User01 create a dm
    u_id = []
    u_id.append(dict_list[1]['auth_user_id'])
    u_id.append(dict_list[2]['auth_user_id'])
    u_id.append(dict_list[3]['auth_user_id'])
    r = requests.post(url + 'dm/create/v1', 
                    json = {'token': token,
                            'u_ids': u_id,})
    payload = r.json()
    dm_id = payload['dm_id']
    return {
        'token': token,
        'u_id': auth_user_id,
        'dm_id': dm_id,
    }

def test_dm_create_invalid_uid(info):
    """
        Test invalid user id
        Raises:
            InputError
    """
    res = requests.post(url + 'dm/create/v1',
                        json = {'token': info['token'],
                                'u_ids': [-5, -80],})
    assert res.status_code == InputError.code

def test_dm_create_multiple_uid(info):
    """
        Test duplicated user id
        Raises:
            InputError
    """
    res = requests.post(url + 'dm/create/v1',
                        json = {'token': info['token'],
                                'u_ids': [1,1,1],})
    payload = res.json()
    temp = -999
    is_duplicate = False

    for id in payload['u_ids']:
        if id == temp:
            is_duplicate = True
        temp = id

    if is_duplicate is True:
        assert res.status_code == InputError.code
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
    u_id.append(dict_list[1].json()['auth_user_id'])
    u_id.append(dict_list[2].json()['auth_user_id'])
    u_id.append(dict_list[3],json()['auth_user_id'])
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

@pytest.fixture(name="dm1")
def users_setup():
    """User1 creates a dm and it directes to user4 and store the dm_id and name"""
    resp = requests.post(url + 'auth/login/v2',
                        json = {'email': 'z5374603@unsw.com', 
                                'password': '123456'})
    user1 = resp.json()
    
    resp = requests.post(url + 'auth/login/v2',
                        json = {"email": "z5374602@unsw.com",
                                "password": "123456",})
    user4 = resp.json()
    
    u_ids = []
    u_ids.append(user4["auth_user_id"])
    resp = requests.post(url + 'dm/create/v1',
                        json = {"token": user1["token"],
                                'u_ids': u_ids,})
    requests.post(url + 'auth/logout/v1', json={'token': user1['token']})
    requests.post(url + 'auth/logout/v1', json={'token': user4['token']})
    dm1 = resp.json()

    return dm1

def test_invalid_dm_id(user_list):
    """Test dm_remove_v1, it will raise Input error 
    if give a invalid dm ID."""
    res = requests.delete(url + 'dm/remove/v1',
                            json = {"token": user_list[0]["token"], 
                                    "dm_id": -1})
    assert res.status_code == InputError.code

def test_author_not_creator(user_list, dm1):
    """Test dm/remove/v1 when the user is 
    not the original DM creator 
    then raise AccessError."""

    resp = requests.delete(url + 'dm/remove/v1',
                            json = {"token": user_list[3].json()["token"], 
                                    "dm_id": dm1["dm_id"]})
    assert resp.status_code == AccessError.code

def test_remove_success(user_list, dm1):
    """
    User1 creates a dm and it directes to user4
    User1 remove dm1 successfully.
    """ 
    requests.delete(url + 'dm/remove/v1',
                    json = {"token": user_list[0].json()["token"], 
                            "dm_id": dm1["dm_id"]})

    resp = requests.get(url + 'dm/list/v1',
                        params = {"token": user_list[0].json()["token"]}) 
    assert json.loads(resp.text) == {"dms": []}
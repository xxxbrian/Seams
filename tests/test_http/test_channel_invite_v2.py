import pytest
import requests
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
                                   json = 
                                       {'email': 'z5374603@unsw.com',
                                        'password': '123456',
                                        'name_first': 'Steve',
                                        'name_last': 'Yang'}))
    user_list.append(requests.post(f"{url}auth/register/v2",
                                   json = 
                                       {'email': 'z5374602@unsw.com',
                                        'password': '123456',
                                        'name_first': 'Brian',
                                        'name_last': 'Lee'}))
    user_list.append(requests.post(f"{url}auth/register/v2",
                                   json = { 'email': 'z5374601@unsw.com',
                                            'password': '123456',
                                            'name_first': 'Bojin',
                                            'name_last': 'Li'}))

    return user_list

@pytest.fixture(name = 'login_list')
def login_two_users():
    login_list = []
    login_list.append(requests.post(url + 'auth/login/v2',
                                    json = {'email': 'z5374603@unsw.com',
                                            'password': '123456'}))
    login_list.append(requests.post(url + 'auth/login/v2',
                                    json = {'email': 'z5374602@unsw.com',
                                            'password': '123456'}))
    login_list.append(requests.post(url + 'auth/login/v2',
                                    json = {'email': 'z5374601@unsw.com',
                                            'password': '123456'}))
    return  login_list

@pytest.fixture(name = 'channel_id_list')
def test_create_channel_normal(user_list, login_list):
#         """
#         Test cases for create channel normal
#         Args:
#             token: user token
#             name:  normal
#             is_public: true
#         Returns:
#             200
#         """
    channel_id_list = []
    for login_user in login_list:
        channel_id_list.append(requests.post(f"{url}channels/create/v2",
                                json = {'token': login_user.json()['token'],
                                        'name': 'testname',
                                        'is_public':True}))
    return channel_id_list


def test_channels_show_detail(user_list, login_list, channel_id_list):
#         """
#         Test cases for show channel detail normal
#             token: user token
#             channel_id:  
#         Returns:
#             200
#         Returns:
#             N/A
#         """
    for  idx, login_user in enumerate(login_list):
        respon = requests.get(f"{url}channel/details/v2",
                                params= {'token': login_user.json()['token'],
                                        'channel_id': channel_id_list[idx].json()['channel_id']})
        assert respon.status_code == 200


def test_channels_detail_with_valid_channelid_and_unauthorised_user(user_list, login_list, channel_id_list):
#         """
#         Test cases for show channel detail with invalid channelid
#             token: user token
#             channel_id:  valid id, but unauthorised user
#         Returns:
#             AccessError.code
#         Returns:
#             N/A
#         """
        respon = requests.get(f"{url}channel/details/v2",
                                params= {'token': login_list[0].json()['token'],
                                        'channel_id': channel_id_list[1].json()['channel_id']})
        assert respon.status_code == AccessError.code

def test_channels_invite_user_normal(user_list, login_list, channel_id_list):
#         """
#         Test cases for show channel detail with invalid channelid
#             token: user token
#             channel_id:  valid id
#         Returns:
#             200
#         Returns:
#             N/A
#         """
        response_1 = requests.post(f"{url}channel/invite/v2",
                                json= {'token': login_list[0].json()['token'],
                                        'channel_id': channel_id_list[0].json()['channel_id'],
                                        'u_id':login_list[1].json()['auth_user_id']})
                                        
        assert response_1.status_code == 200
        response_2 = requests.get(f"{url}channel/details/v2",
                                params= {'token': login_list[1].json()['token'],
                                        'channel_id': channel_id_list[0].json()['channel_id']})
        assert response_2.status_code == 200

def test_channels_invite_user_with_invalid_channel_id(user_list, login_list, channel_id_list):
#         """
#         Test cases for join channel detail with invalid channelid
#             token: user token
#             channel_id:  invalid id
#         Returns:
#             InputError
#         Returns:
#             N/A
#         """
        respon = requests.post(f"{url}channel/invite/v2",
                                json= {'token': login_list[0].json()['token'],
                                        'channel_id': '999999999',
                                        'u_id':login_list[1].json()['auth_user_id']})
        assert respon.status_code == InputError.code

def test_channels_invite_user_with_invalid_uid(user_list, login_list, channel_id_list):
#         """
#         Test cases for invite invalid uid
#             token: user token
#             channel_id:  valid id
#         Returns:
#             InputError
#         Returns:
#             N/A
#         """
        respon = requests.post(f"{url}channel/invite/v2",
                                json= {'token': login_list[0].json()['token'],
                                        'channel_id': channel_id_list[0].json()['channel_id'],
                                        'u_id':'999999999'})
        assert respon.status_code == InputError.code
        
def test_channels_invite_invalid_token(user_list, login_list, channel_id_list):
    '''
    
    This test is to test when token is invalid 
    
    Raises:
        AccessError
        
    '''
    response_1 = requests.get(f"{url}channel/details/v2",
                                params= {'token': -1,
                                        'channel_id': channel_id_list[0].json()['channel_id']})
    assert response_1.status_code == AccessError.code
    
    response_2 = requests.post(f"{url}channel/invite/v2",
                                json= {'token': -1,
                                        'channel_id': channel_id_list[0].json()['channel_id'],
                                        'u_id':login_list[1].json()['auth_user_id']})             
    assert response_2.status_code == AccessError.code
    response_3 = requests.get(f"{url}channel/details/v2",
                                params= {'token': -1,
                                        'channel_id': channel_id_list[0].json()['channel_id']})
    assert response_3.status_code == AccessError.code
    
    response_4 = requests.post(f"{url}channel/invite/v2",
                                json= {'token': -1,
                                        'channel_id': '999999999',
                                        'u_id':login_list[1].json()['auth_user_id']})
    assert response_4.status_code == AccessError.code
    response_5 = requests.post(f"{url}channel/invite/v2",
                                json= {'token': -1,
                                        'channel_id': channel_id_list[0].json()['channel_id'],
                                        'u_id':'999999999'})
    assert response_5.status_code == AccessError.code

def test_channels_invite_auth_user_isnot_in_channel(user_list, login_list, channel_id_list):
    '''
    
    This test is to test when auth_user isn't in channel
    
    Raises:
        AccessError
        
    ''' 
    response_1 = requests.post(f"{url}channel/invite/v2",
                                json= {'token': login_list[1].json()['token'],
                                        'channel_id': channel_id_list[0].json()['channel_id'],
                                        'u_id': login_list[2].json()['auth_user_id']})
    response_1.status_code == AccessError.code
    
def test_channels_invite_user_already_in_channel(user_list, login_list, channel_id_list):
    '''
    
    This test is to test when user already in channel
    
    Raises:
        InputError
        
    ''' 
    response_1 = requests.post(f"{url}channel/invite/v2",
                                json= {'token': login_list[0].json()['token'],
                                        'channel_id': channel_id_list[0].json()['channel_id'],
                                        'u_id': login_list[0].json()['auth_user_id']})
    response_1.status_code == InputError.code
    
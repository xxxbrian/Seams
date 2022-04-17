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

    return user_list

@pytest.fixture(name = 'login_list')
def login_four_users():
    login_list = []
    login_list.append(requests.post(url + 'auth/login/v2',
                                    json = {'email': 'z5374603@unsw.com',
                                            'password': '123456'}))
    login_list.append(requests.post(url + 'auth/login/v2',
                                    json = {'email': 'z5374602@unsw.com',
                                            'password': '123456'}))
    return  login_list

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
    for login_user in login_list:
        respon = requests.post(f"{url}channels/create/v2",
                                json = {'token': login_user.json()['token'],
                                        'name': 'testname',
                                        'is_public':'true'})
        assert respon.status_code == 200


def test_channels_create_name_too_short(user_list, login_list):
#         """
#         Test cases for create channel normal with name too short
#         Args:
#             token: user token
#             name:  empty
#             is_public: true
#         Returns:
#             200
#         Returns:
#             N/A
#         """
    for login_user in login_list:
        respon = requests.post(f"{url}channels/create/v2",
                                json = {'token': login_user.json()['token'],
                                        'name': '',
                                        'is_public':'true'})
        assert respon.status_code == InputError.code

def test_channels_create_name_too_long(user_list, login_list):
#         """
#         Test cases for create channel normal with name too short
#         Args:
#             token: user token
#             name:  lenght larger than 20
#             is_public: true
#         Returns:
#             N/A
#         """
    for login_user in login_list:
        respon = requests.post(f"{url}channels/create/v2",
                                json = {'token': login_user.json()['token'],
                                        'name': 'name_is_too_looooog_than_20',
                                        'is_public':'true'})
        assert respon.status_code == InputError.code
        
def test_channels_create_invalid_token(user_list, login_list):
    '''
    
    This test is to test when input invalid token
    
    Raises: 
        AccessError
        
    '''
    respon = requests.post(f"{url}channels/create/v2",
                           json = {'token': -1,
                                   'name': 'testname',
                                   'is_public':'true'})
    assert respon.status_code == AccessError.code

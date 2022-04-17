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
def login_two_users():
    login_list = []
    login_list.append(requests.post(url + 'auth/login/v2',
                                    json = {'email': 'z5374603@unsw.com',
                                            'password': '123456'}))
    login_list.append(requests.post(url + 'auth/login/v2',
                                    json = {'email': 'z5374602@unsw.com',
                                            'password': '123456'}))
    return  login_list


def test_channels_list_with_user(user_list, login_list):
#         """
#         Test cases for show all channel list
#             token: user token
#         Returns:
#             channel list info
#         Returns:
#             N/A
#         """
    for login_user in login_list:
        requests.post(f"{url}channels/create/v2",
                                json = {'token': login_user.json()['token'],
                                        'name': 'testname001',
                                        'is_public':'true'})
        requests.post(f"{url}channels/create/v2",
                                json = {'token': login_user.json()['token'],
                                        'name': 'testname002',
                                        'is_public':'true'})
        requests.post(f"{url}channels/create/v2",
                                json = {'token': login_user.json()['token'],
                                        'name': 'testname003',
                                        'is_public':'false'})

    for login_user in login_list:
        respon = requests.get(f"{url}channels/list/v2",
                                params= {'token': login_user.json()['token']})
        
        assert respon.status_code == 200
        assert len(respon.json()['channels']) == 3


def test_channels_list_with_un_associated_user(user_list, login_list):
#         """
#         Test cases for show all channel list with associated user
#             token: user token
#         Returns:
#             no result result
#         Returns:
#             N/A
#         """
        login_user = login_list[0]
        requests.post(f"{url}channels/create/v2",
                                json = {'token': login_user.json()['token'],
                                        'name': 'testname001',
                                        'is_public':'true'})
        requests.post(f"{url}channels/create/v2",
                                json = {'token': login_user.json()['token'],
                                        'name': 'testname002',
                                        'is_public':'true'})
        requests.post(f"{url}channels/create/v2",
                                json = {'token': login_user.json()['token'],
                                        'name': 'testname003',
                                        'is_public':'false'})

        check_user = login_list[1]
        respon = requests.get(f"{url}channels/list/v2",
                                params= {'token': check_user.json()['token']})
        
        assert respon.status_code == 200
        assert len(respon.json()['channels']) == 0
        
def test_channels_list_with_invalid_token(user_list, login_list):
    '''
    
    This test is to test when input invalid token
    
    Raises: 
        AccessError
        
    '''
    for login_user in login_list:
        requests.post(f"{url}channels/create/v2",
                                json = {'token': login_user.json()['token'],
                                        'name': 'testname001',
                                        'is_public':'true'})
        requests.post(f"{url}channels/create/v2",
                                json = {'token': login_user.json()['token'],
                                        'name': 'testname002',
                                        'is_public':'true'})
        requests.post(f"{url}channels/create/v2",
                                json = {'token': login_user.json()['token'],
                                        'name': 'testname003',
                                        'is_public':'false'})

    respon = requests.get(f"{url}channels/list/v2",
                            params= {'token': -1})
    assert respon.status_code == AccessError.code
    
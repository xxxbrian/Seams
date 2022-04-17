import pytest
import requests
from src.config import url
from src.error import AccessError

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
                                   json = 
                                       {'email': 'z5374601@unsw.com',
                                        'password': '123456',
                                        'name_first': 'Bojin',
                                        'name_last': 'Li'}))
    user_list.append(requests.post(f"{url}auth/register/v2",
                                   json = 
                                       {'email': 'z5374600@unsw.com',
                                        'password': '123456',
                                        'name_first':'Cicy',
                                        'name_last': 'Zhou'}))
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
    login_list.append(requests.post(url + 'auth/login/v2',
                                    json = {'email': 'z5374601@unsw.com',
                                            'password': '123456'}))
    login_list.append(requests.post(url + 'auth/login/v2',
                                    json = {'email': 'z5374600@unsw.com',
                                            'password': '123456'}))
    return login_list

def test_logout(user_list, login_list):
        """
        Test cases for user logout

        Args:
            user_list: 4 pre-register users, obtain their return value as a response

        Returns:
            N/A

        """
        for log_out_user in login_list:
            respon_1 = requests.post(url + 'auth/logout/v1',
                                   json={'token': log_out_user.json()['token']})
            respon_2 = requests.get(url + 'channels/listall/v2',
                                     json={'token': log_out_user.json()['token']})
            assert respon_1.status_code == 200
            assert respon_2.status_code == AccessError.code

def test_logout_twice(user_list, login_list):
    """
        Test cases for user logout twice

        Args:
            user_list: 4 pre-register users, obtain their return value as a response

        Returns:
            N/A

    """
    requests.post(url + 'auth/logout/v1',
                  json={'token': login_list[0].json()['token']})
    respon = requests.post(url + 'auth/logout/v1',
                           json={'token': login_list[0].json()['token']})
    assert respon.status_code == AccessError.code


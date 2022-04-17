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

def test_auth_login_return_type(user_list):
    '''
    Test the return value of auth_login_v2
    
    parameter:
        user_list (list)
        
    return:
        N/A
    '''
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
    for login_user in login_list:
        assert type(login_user.json()['token']).__name__ == 'str'
        assert type(login_user.json()['auth_user_id']).__name__ == 'int'
        
def test_auth_login_correct_user_id(user_list):
    '''
    Test login user return correct user_id
    
    parameter:
        user_list (list)
        
    return:
        N/A
    '''
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
    for index, login_user in enumerate(login_list):
        assert login_user.json()['auth_user_id'] == user_list[index].json()['auth_user_id']
        
def test_auth_login_empty_email(user_list):
    '''
    This test is testing empty emails and raising InputError
    
    parameters:
        user_list(list)
        
    Raises:
        InputError
        
    return:
        N/A
    ''' 
    respon = requests.post(url + 'auth/login/v2',
                             json=
                                {'email': '',
                                 'password': '123456'})
    assert respon.status_code == InputError.code
    respon = requests.post(url + 'auth/login/v2',
                             json=
                                {'email': ' ',
                                 'password': '123456'})
    assert respon.status_code == InputError.code
    respon = requests.post(url + 'auth/login/v2',
                             json=
                                {'email': '  ',
                                 'password': '123456'})
    assert respon.status_code == InputError.code
    
def test_auth_login_no_at_email(user_list):
    '''
    This test is testing non_@ emails and raising InputError
    
    parameters:
        user_list(list)
        
    Raises:
        InputError
        
    return:
        N/A
    ''' 
    respon = requests.post(url + 'auth/login/v2',
                             json=
                                {'email': 'email',
                                 'password': '123456'})
    assert respon.status_code == InputError.code
    respon = requests.post(url + 'auth/login/v2',
                             json=
                                {'email': 'email.com',
                                 'password': '123456'})
    assert respon.status_code == InputError.code
    respon = requests.post(url + 'auth/login/v2',
                             json=
                                {'email': '12345.com',
                                 'password': '123456'})
    assert respon.status_code == InputError.code
    
def test_auth_login_no_dot_email(user_list):
    '''
    This test is testing no '.com' emails and raising InputError
    
    parameters:
        user_list(list)
        
    Raises:
        InputError
        
    return:
        N/A
    ''' 
    respon = requests.post(url + 'auth/login/v2',
                             json=
                                {'email': 'email@com',
                                 'password': '123456'})
    assert respon.status_code == InputError.code
    respon = requests.post(url + 'auth/login/v2',
                             json=
                                {'email': '123@Steve',
                                 'password': '123456'})
    assert respon.status_code == InputError.code
    respon = requests.post(url + 'auth/login/v2',
                             json=
                                {'email': '123@123',
                                 'password': '123456'})
    assert respon.status_code == InputError.code
    
def test_auth_login_empty_password(user_list):
    '''
    Test correct email with empty password
    
    parameters:
        user_list(list)
        
    Raises:
        InputError
        
    return:
        N/A
    '''
    respon = requests.post(url + 'auth/login/v2',
                             json=
                                {'email': 'z5374603@unsw.com',
                                 'password': ''})
    assert respon.status_code == InputError.code
    respon = requests.post(url + 'auth/login/v2',
                             json=
                                {'email': 'z5374602@unsw.com',
                                 'password': ''})
    assert respon.status_code == InputError.code
    
def test_auth_login_wrong_password(user_list):
    '''
    Test correct email with empty password
    
    parameters:
        user_list(list)
        
    Raises:
        InputError
        
    return:
        N/A
    '''
    respon = requests.post(url + 'auth/login/v2',
                             json=
                                {'email': 'z5374603@unsw.com',
                                 'password': '123'})
    assert respon.status_code == InputError.code
    respon = requests.post(url + 'auth/login/v2',
                             json=
                                {'email': 'z5374602@unsw.com',
                                 'password': 'abc'})
    assert respon.status_code == InputError.code

def test_auth_login_the_same_user_login_twice(user_list):
    '''
    When the same user login twice, test tokens are different
    
    parameters:
        user_list
        
    return:
        N/A
    '''
    response_1 = requests.post(url + 'auth/login/v2',
                  json = {'email' : 'z5374603@unsw.com',
                          'password' : '123456'})
    response_2 = requests.post(url + 'auth/login/v2',
                  json = {'email' : 'z5374603@unsw.com',
                          'password' : '123456'})
    assert response_1.json()['token'] != response_2.json()['token']
    
def test_auth_login_different_user_login(user_list):
    '''
    When different users login, return different token
    
    parameters:
        user_list
        
    return:
        N/A
    '''
    response_1 = requests.post(url + 'auth/login/v2',
                  json = {'email' : 'z5374603@unsw.com',
                          'password' : '123456'})
    response_2 = requests.post(url + 'auth/login/v2',
                  json = {'email' : 'z5374602@unsw.com',
                          'password' : '123456'})
    assert response_1.json()['token'] != response_2.json()['token']
    
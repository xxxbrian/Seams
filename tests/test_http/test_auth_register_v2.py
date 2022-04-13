import pytest
import requests
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
                                   json ={  'email': 'z5374600@unsw.com',
                                            'password': '123456',
                                            'name_first':'Cicy',
                                            'name_last': 'Zhou'}))
    return user_list
    
def test_auth_register_type(user_list):
    '''
    This test is testing the return value's types
    
    parameter:
        user_list (list))
        
    Return:
        N/A
    '''
    # Assert return 'token' is string, 'auth_user_id' is int
    for user in user_list:
        assert type(user.json()['token']).__name__ == 'str'
        assert type(user.json()['auth_user_id']).__name__ == 'int'
    
def test_auth_register_unique_user_id(user_list):
    '''
    This test is testing all auth_user_id s are different
    
    parameter:
        user_list (list)
        
    return:
        N/A
    '''
    user_id_list = []
    for user in user_list:
        user_id_list.append(user.json()['auth_user_id'])
    assert len(user_id_list) == len(set(user_id_list))  # user_id is unique
    
def test_auth_register_unique_token(user_list):
    '''
    This test is testing all token s are different
    
    parameters:
        user_list (list)
        
    return:
        N/A
    '''
    user_token_list = []
    for user in user_list:    
        user_token_list.append(user.json()['token'])
    assert len(user_token_list) == len(set(user_token_list))    # user_token is unique
    
def test_auth_register_empty_email(user_list):
    '''
    This test is testing empty emails and raising InputError
    
    parameters:
        user_list (list)
        
    Raises:
        InputError
        
    return:
        N/A
    ''' 
    respon = requests.post(url + 'auth/register/v2',
                             json = {'email': '',
                                    'password': '123456',
                                    'name_first': 'Empty',
                                    'name_last': 'Email'})
    assert respon.status_code == InputError.code
    respon = requests.post(url + 'auth/register/v2',
                             json = {'email': ' ',
                                    'password': '123456',
                                    'name_first': 'Steve',
                                    'name_last': 'Yang'})
    assert respon.status_code == InputError.code
    respon = requests.post(url + 'auth/register/v2',
                             json = {'email': '  ',
                                    'password': '123456',
                                    'name_first': 'Bojin',
                                    'name_last': 'Li'})
    assert respon.status_code == InputError.code
    
def test_auth_register_no_at_email(user_list):
    '''
    This test is testing non_@ emails and raising InputError
    
    parameters:
        user_list (list)
        
    Raises:
        InputError
        
    return:
        N/A
    ''' 
    respon = requests.post(url + 'auth/register/v2',
                             json = {'email': 'email',
                                     'password': '123456',
                                     'name_first': 'Steve',
                                     'name_last': 'Yang'})
    assert respon.status_code == InputError.code
    respon = requests.post(url + 'auth/register/v2',
                             json = {'email': 'email.com',
                                    'password': '123456',
                                    'name_first': 'Bojin',
                                    'name_last': 'Li'})
    assert respon.status_code == InputError.code
    respon = requests.post(url + 'auth/register/v2',
                             json = {'email': '12345.com',
                                    'password': '123456',
                                    'name_first': 'Brian',
                                    'name_last': 'Lee'})
    assert respon.status_code == InputError.code
    
def test_auth_register_no_dot_email(user_list):
    '''
    This test is testing no '.com' emails and raising InputError
    
    parameters:
        user_list (list)
        
    Raises:
        InputError
        
    return:
        N/A
    ''' 
    respon = requests.post(url + 'auth/register/v2',
                             json = {'email': 'email@com',
                                    'password': '123456',
                                    'name_first': 'Steve',
                                    'name_last': 'Yang'})
    assert respon.status_code == InputError.code
    respon = requests.post(url + 'auth/register/v2',
                             json = {'email': '123@Steve',
                                    'password': '123456',
                                    'name_first': 'Bojin',
                                    'name_last': 'Li'})
    assert respon.status_code == InputError.code
    respon = requests.post(url + 'auth/register/v2',
                             json = {'email': '123@123',
                                    'password': '123456',
                                    'name_first': 'Brian',
                                    'name_last': 'Lee'})
    assert respon.status_code == InputError.code
    
def test_auth_register_email_been_used(user_list):
        """
        This test is testing the user register with email that have been used

        register 2 users with the same email as 2 pre-register users
        
        Returns:
            N/A

        Raises:
            InputError: When the email address of the user has been used

        """
        respon = requests.post(url + 'auth/register/v2',
                                 json = {'email': 'z5374603@unsw.com',
                                        'password': '123456',
                                        'name_first': 'Steve',
                                        'name_last': 'Young'})
        assert respon.status_code == InputError.code
        respon = requests.post(url + 'auth/register/v2',
                                 json = {'email': 'z5374602@unsw.com',
                                        'password': '123456',
                                        'name_first': 'Brian',
                                        'name_last': 'leeeee'})
        assert respon.status_code == InputError.code

def test_auth_register_empty_password(user_list):
    """
        This test is testing the user register with empty password
        
        Returns:
            N/A

        Raises:
            InputError: When the password is empty

    """
    respon = requests.post(url + 'auth/register/v2',
                             json=
                                {'email': 'z5374603@ad.unsw.edu.au',
                                 'password': '',
                                 'name_first': 'Steve',
                                 'name_last': 'Yang'})
    assert respon.status_code == InputError.code
    respon = requests.post(url + 'auth/register/v2',
                             json=
                                {'email': 'z5374602@ad.unsw.edu.au',
                                 'password': '',
                                 'name_first': 'Bojin',
                                 'name_last': 'Li'})
    assert respon.status_code == InputError.code
    
def test_auth_register_too_short_password(user_list):
    """
        This test is testing the user register with too short password
        
        Returns:
            N/A

        Raises:
            InputError: When the password is too short

    """
    respon = requests.post(url + 'auth/register/v2',
                             json=
                                {'email': 'z5374603@ad.unsw.edu.au',
                                 'password': '12345',
                                 'name_first': 'Steve',
                                 'name_last': 'Yang'})
    assert respon.status_code == InputError.code
    respon = requests.post(url + 'auth/register/v2',
                             json=
                                {'email': 'z5374602@ad.unsw.edu.au',
                                 'password': 'abc',
                                 'name_first': 'Bojin',
                                 'name_last': 'Li'})
    assert respon.status_code == InputError.code
    
def test_auth_register_empty__first_name(user_list):
    """
        This test is testing the user register with too short first name
        
        Returns:
            N/A

        Raises:
            InputError: When the first name is too short

    """
    respon = requests.post(url + 'auth/register/v2',
                             json=
                                {'email': 'z5374603@ad.unsw.edu.au',
                                 'password': '123456',
                                 'name_first': '',
                                 'name_last': 'Yang'})
    assert respon.status_code == InputError.code
    respon = requests.post(url + 'auth/register/v2',
                             json=
                                {'email': 'z5374602@ad.unsw.edu.au',
                                 'password': '123456',
                                 'name_first': '',
                                 'name_last': 'Li'})
    assert respon.status_code == InputError.code

def test_auth_register_empty_last_name(user_list):
    """
        This test is testing the user register with too short last name
        
        Returns:
            N/A

        Raises:
            InputError: When the last name is too short

    """
    respon = requests.post(url + 'auth/register/v2',
                             json=
                                {'email': 'z5374603@ad.unsw.edu.au',
                                 'password': '123456',
                                 'name_first': 'Steve',
                                 'name_last': ''})
    assert respon.status_code == InputError.code
    respon = requests.post(url + 'auth/register/v2',
                             json=
                                {'email': 'z5374602@ad.unsw.edu.au',
                                 'password': '123456',
                                 'name_first': 'Bojin',
                                 'name_last': ''})
    assert respon.status_code == InputError.code
    
def test_auth_register_too_long_first_name(user_list):
    """
        This test is testing the user register with too long first name
        
        Returns:
            N/A

        Raises:
            InputError: When the first name is too long

    """
    too_long_name = ""
    while len(too_long_name) < 51:
        too_long_name += 'a'
    respon = requests.post(url + 'auth/register/v2',
                             json=
                                {'email': 'z5374603@ad.unsw.edu.au',
                                 'password': '123456',
                                 'name_first': too_long_name,
                                 'name_last': 'Yang'})
    assert respon.status_code == InputError.code
    respon = requests.post(url + 'auth/register/v2',
                             json=
                                {'email': 'z5374602@ad.unsw.edu.au',
                                 'password': '123456',
                                 'name_first': too_long_name,
                                 'name_last': 'Li'})
    assert respon.status_code == InputError.code

def test_auth_register_too_long_last_name(user_list):
    """
        This test is testing the user register with too long last name
        
        Returns:
            N/A

        Raises:
            InputError: When the last name is too long

    """
    too_long_name = ""
    while len(too_long_name) < 51:
        too_long_name += 'a'
    respon = requests.post(url + 'auth/register/v2',
                             json=
                                {'email': 'z5374603@ad.unsw.edu.au',
                                 'password': '123456',
                                 'name_first': 'Steve',
                                 'name_last': too_long_name})
    assert respon.status_code == InputError.code
    respon = requests.post(url + 'auth/register/v2',
                             json=
                                {'email': 'z5374602@ad.unsw.edu.au',
                                 'password': '123456',
                                 'name_first': 'Bojin',
                                 'name_last': too_long_name})
    assert respon.status_code == InputError.code   
    
def test_auth_register_empty_name(user_list):
    """
        This test is testing the user register with too short name
        
        Returns:
            N/A

        Raises:
            InputError: When the name is too short

    """
    respon = requests.post(url + 'auth/register/v2',
                             json=
                                {'email': 'z5374603@ad.unsw.edu.au',
                                 'password': '123456',
                                 'name_first': '',
                                 'name_last': ''})
    assert respon.status_code == InputError.code
    respon = requests.post(url + 'auth/register/v2',
                             json=
                                {'email': 'z5374602@ad.unsw.edu.au',
                                 'password': '123456',
                                 'name_first': '',
                                 'name_last': ''})
    assert respon.status_code == InputError.code
    
def test_auth_register_too_long_name(user_list):
    """
        This test is testing the user register with too long name
        
        Returns:
            N/A

        Raises:
            InputError: When the name is too long

    """
    too_long_name = ""
    while len(too_long_name) < 51:
        too_long_name += 'a'
    respon = requests.post(url + 'auth/register/v2',
                             json=
                                {'email': 'z5374603@ad.unsw.edu.au',
                                 'password': '123456',
                                 'name_first': too_long_name,
                                 'name_last': too_long_name})
    assert respon.status_code == InputError.code
    respon = requests.post(url + 'auth/register/v2',
                             json=
                                {'email': 'z5374602@ad.unsw.edu.au',
                                 'password': '123456',
                                 'name_first': too_long_name,
                                 'name_last': too_long_name})
    assert respon.status_code == InputError.code   
       
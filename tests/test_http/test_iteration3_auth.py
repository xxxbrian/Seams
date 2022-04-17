import pytest
import requests
from src.config import SECRET, url 
from src.error import InputError

def test_auth_passwordreset_request_normal():
    '''
    
    This test is to test when email is valid and send successfully
    
    '''
    requests.post(f"{url}auth/register/v2",
                  json = { 'email': '1981686549@qq.com',
                           'password': '123456',
                           'name_first': 'Steven',
                           'name_last': 'Yang'})
    res = requests.post(url + "auth/passwordreset/request/v1",
                        json = {'email': '1981686549@qq.com'})
    assert res.status_code == 200
    
def test_auth_passwordreset_request_not_user():
    '''
    
    This test is to test when email is not refer to a user
    
    '''
    res = requests.post(url + "auth/passwordreset/request/v1",
                        json = {'email': '1981@qq.com'})
    assert res.status_code == 200
    
def test_auth_passwordreset_reset_correct_reset_code():
    '''
    
    This test is to test when reset code is correct
    
    Raises:
        InputError
        
    '''
    requests.post(url + "auth/passwordreset/request/v1",
                        json = {'email': '1981686549@qq.com'})
    bd = requests.get(url + 'backdoor/v1',
                 params = SECRET).json()
    re_code = bd['rcode'][-1]
    res = requests.post(url + 'auth/passwordreset/reset/v1',
                        json = {'reset_code': re_code,
                                'new_password': "123456"})
    assert res.status_code == 200
    
def test_auth_passwordreset_reset_invalid_new_password():
    '''
    
    This test is to test when reset code is correct
    
    Raises:
        InputError
        
    '''
    requests.post(url + "auth/passwordreset/request/v1",
                        json = {'email': '1981686549@qq.com'})
    bd = requests.get(url + 'backdoor/v1',
                 params = SECRET).json()
    re_code = bd['rcode'][-1]
    res = requests.post(url + 'auth/passwordreset/reset/v1',
                        json = {'reset_code': re_code,
                                'new_password': "12"})
    assert res.status_code == InputError.code

def test_auth_passwordreset_reset_wrong_reset_code():
    '''
    
    This test is to test when reset code is wrong
    
    Raises:
        InputError
        
    '''
    requests.post(url + "auth/passwordreset/request/v1",
                        json = {'email': '1981686549@qq.com'})
    res = requests.post(url + 'auth/passwordreset/reset/v1',
                        json = {'reset_code': '123456',
                                'new_password': "123456"})
    assert res.status_code == InputError.code
    
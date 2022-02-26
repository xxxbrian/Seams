import pytest
from src.auth import auth_login_v1, auth_register_v1
from src.other import clear_v1
from src.error import InputError
    
@pytest.fixture(name = "user_list")
def create_users():
    """
    This function is to pre_register 4 users for tests
    
    Return a list of user_id (type: dict)

    """
    clear_v1()
    user_list = list()
    user_list.append(auth_register_v1("z5374603@ad.unsw.edu.au", "Ymc123", "Steve", "Yang"))
    user_list.append(auth_register_v1("z5201314@ad.unsw.edu.au", "Bojin123", "Bojin", "Li"))
    user_list.append(auth_register_v1("12345678@qq.com", "Cicy123", "Cicy", "Zhou"))
    user_list.append(auth_register_v1("13579@gmail.com", "Lebron123", "Lebron", "James"))
    return user_list

def test_login_user_id(user_list):
    assert auth_login_v1("z5374603@ad.unsw.edu.au", "Ymc123") == user_list[0]
    assert auth_login_v1("z5201314@ad.unsw.edu.au", "Bojin123") == user_list[1]
    assert auth_login_v1("12345678@qq.com", "Cicy123") == user_list[2]
    assert auth_login_v1("13579@gmail.com", "Lebron123") == user_list[3]
    
    
def test_login_empty_email():
    with pytest.raises(InputError):
        assert auth_login_v1("", "asdfg")   # test empty email
        
def test_login_string_email():        
    with pytest.raises(InputError):
        assert auth_login_v1("email", "123456") # test string
        
def test_login_without_at_email():        
    with pytest.raises(InputError):
        assert auth_login_v1("email.com", "1234")   # test without '@'

def test_login_without_com_email():
    with pytest.raises(InputError):
        assert auth_login_v1("email@qq", "1234")    # test without '.com'

def test_login_inexistent_email():
    with pytest.raises(InputError):
        assert auth_login_v1("z5374604@ad.unsw.edu.au", "1234") # a valid email but inexistent
                   
def test_login_empty_password():
    with pytest.raises(InputError):
        assert auth_login_v1("z5374603@ad.unsw.edu.au", "") # test empty password
        
def test_login_correct_email_wrong_password():
    with pytest.raises(InputError):
        assert auth_login_v1("z5374603@ad.unsw.edu.au", "Ymc123")   # correct email but wrong password
    with pytest. raises(InputError):
        assert auth_login_v1("z5201314@ad.unsw.edu.au", "bojin123")
    with pytest. raises(InputError):
        assert auth_login_v1("13579@gmail.com", "Lebron")
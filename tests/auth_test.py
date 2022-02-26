from unicodedata import name
import pytest
from src.auth import auth_login_v1, auth_register_v1
from src.other import clear_v1
from src.error import InputError

# @pytest.fixture()
# def clean():
    # clear_v1()
    
@pytest.fixture(name = "user_list")
def create_users():
    """
    This function is to pre_register 4 users for tests
    
    Return a list of user_id (type: dict)

    """
    user_list = list()
    user_list.append(auth_register_v1("z5374603@ad.unsw.edu.au", "Ymc123", "Steve", "Yang"))
    user_list.append(auth_register_v1("z5201314@ad.unsw.edu.au", "Bojin123", "Bojin", "Li"))
    user_list.append(auth_register_v1("12345678@qq.com", "Cicy123", "Cicy", "Zhou"))
    user_list.append(auth_register_v1("13579@gmail.com", "Lebron123", "Lebron", "James"))
    return user_list

# @pytest.mark.usefixtures("clear")
class TestLogin:
    @pytest.mark.usefixtures("user_list")
    def test_login_user_id(self, user_list):
        clear_v1()
        assert auth_login_v1("z5374603@ad.unsw.edu.au", "Ymc123") == user_list[0]
        assert auth_login_v1("z5201314@ad.unsw.edu.au", "Bojin123") == user_list[1]
        assert auth_login_v1("12345678@qq.com", "Cicy123") == user_list[2]
        assert auth_login_v1("13579@gmail.com", "Lebron123") == user_list[3]
    
    @pytest.mark.usefixtures("user_list")
    def test_login_inexistent_email(self):
        with pytest.raises(InputError):
            assert auth_login_v1("", "asdfg")   # test empty email
        with pytest.raises(InputError):
            assert auth_login_v1("email", "123456") # test string
        with pytest.raises(InputError):
            assert auth_login_v1("email.com", "1234")   # test without '@'
        with pytest.raises(InputError):
            assert auth_login_v1("email@qq", "1234")    # test without '.com'
        with pytest.raises(InputError):
            assert auth_login_v1("z5374604@ad.unsw.edu.au", "1234") # a valid email but inexistent
           
    @pytest.mark.usefixtures("user_list")        
    def test_login_wrong_password(self):
        with pytest.raises(InputError):
            assert auth_login_v1("z5374603@ad.unsw.edu.au", "") # test empty password
        with pytest.raises(InputError):
            assert auth_login_v1("z5374603@ad.unsw.edu.au", "Ymc123")   # correct email but wrong password
        with pytest. raises(InputError):
            assert auth_login_v1("z5201314@ad.unsw.edu.au", "bojin123")
        with pytest. raises(InputError):
            assert auth_login_v1("13579@gmail.com", "Lebron")
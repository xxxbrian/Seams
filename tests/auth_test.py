'''
import pytest

from src.auth import auth_login_v2, auth_register_v2
from src.other import clear_v1
from src.error import InputError

@pytest.fixture(name = "user_list")
def create_users():
    """
    This function is to pre_register 4 users for tests
    Return a list of user_id (type: dict)
    """

    clear_v1()
    user_list = []
    user_list.append(auth_register_v2("z5374603@ad.unsw.edu.au",
                                    "Ymc123", "Steve", "Yang"))
    user_list.append(auth_register_v2("z5201314@ad.unsw.edu.au",
                                    "Bojin123", "Bojin", "Li"))
    user_list.append(auth_register_v2("12345678@qq.com",
                                    "Cicy123", "Cicy", "Zhou"))
    user_list.append(auth_register_v2("13579@gmail.com",
                                    "Lebron123", "Lebron", "James"))
    return user_list

def test_login_return_type(user_list):
    for login in user_list:
        assert isinstance(login, dict)
        assert isinstance(login["auth_user_id"], int)

def test_login_user_id(user_list):
    assert auth_login_v2("z5374603@ad.unsw.edu.au", "Ymc123")['auth_user_id'] == user_list[0]['auth_user_id'] 
    assert auth_login_v2("z5201314@ad.unsw.edu.au", "Bojin123")['auth_user_id']  == user_list[1]['auth_user_id'] 
    assert auth_login_v2("12345678@qq.com", "Cicy123")['auth_user_id']  == user_list[2]['auth_user_id'] 
    assert auth_login_v2("13579@gmail.com", "Lebron123")['auth_user_id']  == user_list[3]['auth_user_id'] 

def test_login_empty_email():
    with pytest.raises(InputError):
        auth_login_v2("", "asdfg")

def test_login_string_email():
    """test email with plain string"""
    with pytest.raises(InputError):
        auth_login_v2("email", "123456")

def test_login_without_at_email():
    """test email without @"""
    with pytest.raises(InputError):
        auth_login_v2("email.com", "1234")

def test_login_without_com_email():
    """test without '.com'"""
    with pytest.raises(InputError):
        auth_login_v2("email@qq", "1234")

def test_login_inexistent_email():
    """test with valid email format but not in user list"""
    with pytest.raises(InputError):
        auth_login_v2("z5374604@ad.unsw.edu.au", "1234")

def test_login_empty_password():
    with pytest.raises(InputError):
        auth_login_v2("z5374603@ad.unsw.edu.au", "")

def test_login_correct_email_wrong_password():
    with pytest.raises(InputError):
        auth_login_v2("z5374603@ad.unsw.edu.au", "Ymc1234")
    with pytest. raises(InputError):
        auth_login_v2("z5201314@ad.unsw.edu.au", "bojin123")
    with pytest. raises(InputError):
        auth_login_v2("13579@gmail.com", "Lebron")

def test_register_type_and_return_unique_id(user_list):
    user_id = []
    for user in user_list:
        # user type must be dictionary
        assert isinstance(user, dict)
        # auth_user_id type must be integer
        assert isinstance(user["auth_user_id"], int)
        user_id.append(user["auth_user_id"])

    # check each id is unique
    assert len(user_id) == len(set(user_id))

def test_register_empty_email():
    with pytest.raises(InputError):
        auth_register_v2("", "123456", "Steven", "Curry")
    with pytest.raises(InputError):
        auth_register_v2(" ", "123456", "Kobe", "Bryant")

def test_register_without_both_at_and_com_email():
    with pytest.raises(InputError):
        auth_register_v2("12345", "123456", "Hayden", "Smith")
    with pytest.raises(InputError):
        auth_register_v2("email", "123456", "Cicy", "Zhou")

def test_register_without_at_email():
    with pytest.raises(InputError):
        auth_register_v2("1234.com", "123456", "Steve", "Yang")
    with pytest.raises(InputError):
        auth_register_v2("steve.com", "123456", "Allen", "Lee")

def test_register_without_com_email():
    with pytest.raises(InputError):
        auth_register_v2("steve@yang", "123456", "Steve", "Yang")
    with pytest.raises(InputError):
        auth_register_v2("123@456", "123456", "Haha", "Xixi")

def test_register_been_used_email():
    with pytest.raises(InputError):
        auth_register_v2("z5374603@ad.unsw.edu.au", "Ymc1232", "Steve", "Yang")
    with pytest.raises(InputError):
        auth_register_v2("z5201314@ad.unsw.edu.au", "Bojin1232", "Bojin", "Li")
    with pytest.raises(InputError):
        auth_register_v2("12345678@qq.com", "Cicy1232", "Cicy", "Zhou")
    with pytest.raises(InputError):
        auth_register_v2("13579@gmail.com", "Lebron1232", "Lebron", "James")

def test_register_empty_password():
    with pytest.raises(InputError):
        auth_register_v2("1981686549@qq.com", "", "Steve", "Young")
    with pytest.raises(InputError):
        auth_register_v2("1982686549@qq.com", " ", "Steven", "Young")

def test_register_short_password():
    with pytest.raises(InputError):
        auth_register_v2("123456@qq.com", "12345", "John", "byden")
    with pytest.raises(InputError):
        auth_register_v2("1357911@gmail.com", "wsxc", "Harden", "James")
    with pytest.raises(InputError):
        auth_register_v2("2468@cc.com", "12fas", "Keven", "Durent")

def test_register_empty_first_name():
    with pytest.raises(InputError):
        auth_register_v2("imurfather@unsw.com", "123456KK", "", "Harden")
    with pytest.raises(InputError):
        auth_register_v2("imyourmother@unsw.com", "12345dd", "", "James")

def test_register_too_long_first_name():
    too_long_first_name_1 = ""
    while len(too_long_first_name_1) < 51:
        too_long_first_name_1 += 'a'
    too_long_first_name_2 = ""
    while len(too_long_first_name_2) < 100:
        too_long_first_name_2 += 'b'
    with pytest.raises(InputError):
        auth_register_v2("imyourgrangpa1@unsw.com","1234567", too_long_first_name_1, "Haa")
    with pytest.raises(InputError):
        auth_register_v2("imyourgrangpa2@unsw.com","1234567", too_long_first_name_2, "Xia")

def test_register_too_long_last_name():
    too_long_last_name_1 = ""
    while len(too_long_last_name_1) < 51:
        too_long_last_name_1 += 'c'
    too_long_last_name_2 = ""
    while len(too_long_last_name_2) < 100:
        too_long_last_name_2 += 'd'
    with pytest.raises(InputError):
        auth_register_v2("imyourgrangpa3@unsw.com","1234567", "Haa", too_long_last_name_1)
    with pytest.raises(InputError):
        auth_register_v2("imyourgrangpa4@unsw.com","1234567", "Xia", too_long_last_name_2)

def test_register_too_long_name():
    too_long_last_name_1 = ""
    while len(too_long_last_name_1) < 51:
        too_long_last_name_1 += 'c'
    too_long_last_name_2 = ""
    while len(too_long_last_name_2) < 100:
        too_long_last_name_2 += 'd'
        too_long_first_name_1 = ""
    while len(too_long_first_name_1) < 51:
        too_long_first_name_1 += 'a'
    too_long_first_name_2 = ""
    while len(too_long_first_name_2) < 100:
        too_long_first_name_2 += 'b'
    with pytest.raises(InputError):
        auth_register_v2("imyourgrangpa3@unsw.com",
                        "1234567",
                        too_long_first_name_1,
                        too_long_last_name_1
                        )
    with pytest.raises(InputError):
        auth_register_v2("imyourgrangpa4@unsw.com",
                        "1234567",
                        too_long_first_name_2,
                        too_long_last_name_2
                        )
'''
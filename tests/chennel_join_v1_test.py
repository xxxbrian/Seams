import pytest

from src.channel import channel_join_v1, channel_invite_v1
from src.channels import channels_create_v1, channels_list_v1
from src.auth import auth_register_v1, auth_login_v1
from src.error import InputError, AccessError
from src.other import clear_v1

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

@pytest.fixture(name = "channel_id_1")
def creat_public_channel():
    """
    This function is to pre_creat a public channel for tests
    
    Return channel_id (type: dict)

    """
    user_1 = auth_login_v1("z5374603@ad.unsw.edu.au", "Ymc123")['auth_user_id'] 
    channel_id_1 = channels_create_v1(user_1, "Channel_1", True)['channel_id']  
    return channel_id_1                                                               # public channel_id

@pytest.fixture(name = "channel_id_2")
def creat_private_channel():
    """
    This function is to pre_creat a private channel for tests
    
    Return channel_id_2 (type: dict)

    """
    user_2 = auth_login_v1("z5201314@ad.unsw.edu.au", "Bojin123")['auth_user_id']
    channel_id_2 = channels_create_v1(user_2, "Channel_2", False)['channel_id']
    return channel_id_2                                                             # private channel_id
    
def test_channel_join_invalid_channel_id(user_list):
    user_1 = auth_login_v1("z5374603@ad.unsw.edu.au", "Ymc123")['auth_user_id']
    with pytest.raises(InputError):
        channel_join_v1(user_1, -1)
    with pytest.raises(InputError):
        channel_join_v1(user_1, -2)


def test_channel_join_user_is_already_a_member_of_public_channel(user_list, channel_id_1):
    user_2 = auth_login_v1("z5201314@ad.unsw.edu.au", "Bojin123")['auth_user_id']
    channel_join_v1(user_2, channel_id_1)
    with pytest.raises(InputError):
        channel_join_v1(user_2, channel_id_1)
    
def test_channel_join_user_is_already_a_member_of_private_channel(user_list, channel_id_2):
    user_1 = auth_login_v1("z5374603@ad.unsw.edu.au", "Ymc123")['auth_user_id']
    user_2 = auth_login_v1("z5201314@ad.unsw.edu.au", "Bojin123")['auth_user_id']
    channel_invite_v1(user_2, channel_id_2, user_1)
    with pytest.raises(InputError):
        channel_join_v1(user_1, channel_id_2)


def test_channel_join_private_channel(user_list, channel_id_2):
    user_3 = auth_login_v1("12345678@qq.com", "Cicy123")['auth_user_id']
    user_4 = auth_login_v1("13579@gmail.com", "Lebron123")['auth_user_id']
    with pytest.raises(AccessError):
        channel_join_v1(user_3, channel_id_2)
    with pytest.raises(AccessError):
        channel_join_v1(user_4, channel_id_2)


   

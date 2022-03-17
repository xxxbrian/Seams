'''
import pytest

from src.channel import channel_messages_v2
from src.channels import channels_create_v2
from src.auth import auth_register_v2, auth_login_v2
from src.error import InputError, AccessError
from src.other import clear_v1

@pytest.fixture(name = "user_list")
def create_users():
    """
    This function is to pre_register 4 users for tests
    Return a list of user_id (type: dict)
    """

    clear_v1()
    user_list = []
    user_list.append(auth_register_v2("z5270202@ad.unsw.edu.au",
                                        "Pet123",  "Weihou", "Zeng"))
    user_list.append(auth_register_v2("z5374603@ad.unsw.edu.au",
                                        "Ymc123", "Steve", "Yang"))
    user_list.append(auth_register_v2("z5201314@ad.unsw.edu.au",
                                        "Bojin123", "Bojin", "Li"))
    user_list.append(auth_register_v2("12345678@qq.com", "Cicy123",
                                        "Cicy", "Zhou"))
    return user_list

@pytest.fixture(name = 'channel_id')
def creat_public_channel():
    """
    This function is to pre_creat a public channel for tests
    Return channel_id (type: dict)
    """
    user_1 = auth_login_v2("z5374603@ad.unsw.edu.au", "Ymc123")['token']
    channel_id = channels_create_v2(user_1, "Channel_1", True)['channel_id']
    return channel_id

def test_channel_message_invalid_channel_id(user_list):
    """InputError: channel_id does not refer to a valid channel for public"""
    user_1 = auth_login_v2("z5374603@ad.unsw.edu.au", "Ymc123")['token']

    with pytest.raises(InputError):
        channel_messages_v2(user_1, -1, 0)

def test_channel_message_invalid_index(user_list, channel_id):
    """InputError: start is greater than the total number of messages
        in the channel for public
    """
    user_1 = auth_login_v2("z5374603@ad.unsw.edu.au", "Ymc123")['token']

    with pytest.raises(InputError):
        channel_messages_v2(user_1, channel_id, 100)
    with pytest.raises(InputError):
        channel_messages_v2(user_1, channel_id, 1)
    with pytest.raises(InputError):
        channel_messages_v2(user_1, channel_id, 10)

def test_invalid_user(user_list, channel_id):
    """AccessError: channel_id is valid and the
    authorised user is not a member of the channel for public
    """

    user_2 = auth_login_v2("z5270202@ad.unsw.edu.au", "Pet123")['token']
    user_3 = auth_login_v2("z5201314@ad.unsw.edu.au", "Bojin123")['token']
    user_4 = auth_login_v2("12345678@qq.com", "Cicy123")['token']

    with pytest.raises(AccessError):
        channel_messages_v2(user_2, channel_id, 0)
    with pytest.raises(AccessError):
        channel_messages_v2(user_3, channel_id, 0)
    with pytest.raises(AccessError):
        channel_messages_v2(user_4, channel_id, 0)
'''
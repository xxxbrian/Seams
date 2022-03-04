import pytest

from src.channel import channel_invite_v1
from src.channels import channels_create_v1
from src.auth import auth_register_v1, auth_login_v1
from src.error import InputError, AccessError
from src.other import clear_v1

###################################################################### SET UP ######################################################################

@pytest.fixture(name = "user_list")
def create_users():
    """
    This function is to pre_register 4 users for tests
    
    Return a list of user_id (type: dict)

    """
    clear_v1()
    user_list = list()
    user_list.append(auth_register_v1("z5270202@ad.unsw.edu.au", "Pet123", "Weihou", "Zeng"))
    user_list.append(auth_register_v1("z5374603@ad.unsw.edu.au", "Ymc123", "Steve", "Yang"))
    user_list.append(auth_register_v1("z5201314@ad.unsw.edu.au", "Bojin123", "Bojin", "Li"))
    user_list.append(auth_register_v1("12345678@qq.com", "Cicy123", "Cicy", "Zhou"))
    return user_list

@pytest.fixture(name = 'channel_id')                                                    # creat a public channel
def creat_public_channel():
    """
    This function is to pre_creat a public channel for tests
    
    Return channel_id (type: dict)

    """
    user_1 = auth_login_v1("z5374603@ad.unsw.edu.au", "Ymc123")['auth_user_id']
    channel_id = channels_create_v1(user_1, "Channel_1", True)['channel_id'] 
    return channel_id

@pytest.fixture(name = 'channel_id_2')                                                  # creat a private channel
def create_private_channel():
    """
    This function is to pre_creat a private channel for tests
    
    Return channel_id (type: dict)

    """
    user_2 = auth_login_v1("z5201314@ad.unsw.edu.au", "Bojin123")['auth_user_id']
    channel_id_2 = channels_create_v1(user_2, "Channel_2", False)['channel_id'] 
    return channel_id_2

##################################################################  P U B L I C  ##################################################################

# InputError: channel_id does not refer to a valid channel for public
def test_invalid_channel_id(user_list, channel_id):
    user_1 = auth_login_v1("z5374603@ad.unsw.edu.au", "Ymc123")['auth_user_id']
    user_2 = auth_login_v1("z5270202@ad.unsw.edu.au", "Pet123")['auth_user_id']

    with pytest.raises(InputError):
        channel_invite_v1(user_1, -1, user_2)


# InputError: u_id does not refer to a valid user for public
def test_invalid_u_id(user_list, channel_id):
    user_1 = auth_login_v1("z5374603@ad.unsw.edu.au", "Ymc123")['auth_user_id']

    with pytest.raises(InputError):
        channel_invite_v1(user_1, channel_id, -1)


# InputError: u_id refers to a user who is already a member of the channel for public
def test_user_already_in_channel(user_list, channel_id):
    user_1 = auth_login_v1("z5374603@ad.unsw.edu.au", "Ymc123")['auth_user_id']
    user_2 = auth_login_v1("z5270202@ad.unsw.edu.au", "Pet123")['auth_user_id']
    channel_invite_v1(user_1, channel_id, user_2)

    with pytest.raises(InputError):
        channel_invite_v1(user_1, channel_id, user_2)

# AccessError: channel_id is valid and the authorised user is not a member of the channel for public
def test_unknown_channel_id(user_list, channel_id):
    user_2 = auth_login_v1("z5270202@ad.unsw.edu.au", "Pet123")['auth_user_id']
    user_3 = auth_login_v1("12345678@qq.com", "Cicy123")['auth_user_id']

    with pytest.raises(AccessError):
        channel_invite_v1(user_3, channel_id, user_2)

##################################################################  P R I V A T E  ##################################################################

# InputError: channel_id does not refer to a valid channel for private
def test_invalid_channel_id_2(user_list, channel_id_2):
    user_1 = auth_login_v1("z5201314@ad.unsw.edu.au", "Bojin123")['auth_user_id']
    user_2 = auth_login_v1("z5270202@ad.unsw.edu.au", "Pet123")['auth_user_id']

    with pytest.raises(InputError):
        channel_invite_v1(user_1, -1, user_2)

# InputError: u_id does not refer to a valid user for private
def test_invalid_u_id_private_channel(user_list, channel_id_2):
    user_1 = auth_login_v1("z5201314@ad.unsw.edu.au", "Bojin123")['auth_user_id']

    with pytest.raises(InputError):
        channel_invite_v1(user_1, channel_id_2, -1)

# InputError: u_id refers to a user who is already a member of the channel for private
def test_user_already_in_private_channel(user_list, channel_id_2):
    user_1 = auth_login_v1("z5201314@ad.unsw.edu.au", "Bojin123")['auth_user_id']
    user_2 = auth_login_v1("z5270202@ad.unsw.edu.au", "Pet123")['auth_user_id']
    channel_invite_v1(user_1, channel_id_2, user_2)

    with pytest.raises(InputError):
        channel_invite_v1(user_1, channel_id_2, user_2)

# AccessError: channel_id is valid and the authorised user is not a member of the channel for private
def test_unknown_privatte_channel_id(user_list, channel_id_2):
    user_2 = auth_login_v1("z5270202@ad.unsw.edu.au", "Pet123")['auth_user_id']
    user_3 = auth_login_v1("12345678@qq.com", "Cicy123")['auth_user_id']

    with pytest.raises(AccessError):
        channel_invite_v1(user_3, channel_id_2, user_2)


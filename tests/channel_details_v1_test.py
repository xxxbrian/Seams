import pytest

from src.other import clear_v1
from src.error import InputError, AccessError
from src.channel import channel_details_v1, channel_join_v1, channel_invite_v1
from src.channels import channels_create_v1
from src.auth import auth_login_v1, auth_register_v1

@pytest.fixture(name = "user_list")
def create_users():
    """
    This function is to pre_register 4 users for tests
    Return a list of user_id (type: dict)
    """

    clear_v1()
    user_list = list()
    user_list.append(auth_register_v1("z5374603@ad.unsw.edu.au",
                                        "Ymc123",  "Steve", "Yang"))
    user_list.append(auth_register_v1("z5201314@ad.unsw.edu.au",
                                        "Bojin123", "Bojin", "Li"))
    user_list.append(auth_register_v1("12345678@qq.com",
                                        "Cicy123", "Cicy", "Zhou"))
    user_list.append(auth_register_v1("13579@gmail.com", "Lebron123",
                                        "Steve", "Yang"))
    user_list.append(auth_register_v1("135798@gmail.com", "James123",
                                        "Steve", "Yang"))
    return user_list

@pytest.fixture(name = "channel_id")
def creat_public_channel():
    """
    This function is to pre_creat a public channel for tests
    Return channel_id (type: dict)
    """

    user_1 = auth_login_v1("z5374603@ad.unsw.edu.au", "Ymc123")['auth_user_id']
    channel_id = channels_create_v1(user_1, "Channel_1", True)['channel_id']

    return channel_id

def test_channel_details_invalid_channel_id():
    user_1 = auth_login_v1("z5374603@ad.unsw.edu.au", "Ymc123")['auth_user_id']
    with pytest.raises(InputError):
        channel_details_v1(user_1, -1)
    with pytest.raises(InputError):
        channel_details_v1(user_1, -2)

def test_channel_details_user_not_in_channel(channel_id):
    user_2 = auth_login_v1("z5201314@ad.unsw.edu.au", "Bojin123")['auth_user_id']
    with pytest.raises(AccessError):
        channel_details_v1(user_2, channel_id)
    user_3 = auth_login_v1("12345678@qq.com", "Cicy123")['auth_user_id']
    with pytest.raises(AccessError):
        channel_details_v1(user_3, channel_id)

def test_channel_details_one_owner(channel_id):
    user_1 = auth_login_v1("z5374603@ad.unsw.edu.au", "Ymc123")['auth_user_id']

    assert channel_details_v1(user_1, channel_id) == {
        "name": "Channel_1",
        "is_public": True,
        "owner_members": [{
            'u_id': user_1,
            'name_first': 'Steve',
            'name_last': 'Yang',
            'email': 'z5374603@ad.unsw.edu.au',
            'handle_str': "steveyang",
        }],
        "all_members": [{
            'u_id': user_1,
            'name_first': 'Steve',
            'name_last': 'Yang',
            'email': 'z5374603@ad.unsw.edu.au',
            'handle_str': "steveyang",
        }]
    }

def test_channel_details_one_join_member(channel_id):
    user_1 = auth_login_v1("z5374603@ad.unsw.edu.au", "Ymc123")["auth_user_id"]
    user_2 = auth_login_v1("z5201314@ad.unsw.edu.au", "Bojin123")["auth_user_id"]
    channel_join_v1(user_2, channel_id)

    assert channel_details_v1(user_1, channel_id) == {
        'name': 'Channel_1',
        "is_public": True,
        'owner_members': [
            {
                'u_id': user_1,
                'name_first': 'Steve',
                'name_last': 'Yang',
                'email': 'z5374603@ad.unsw.edu.au',
                'handle_str': "steveyang",
            }
        ],
        'all_members': [
            {
                'u_id': user_1,
                'name_first': 'Steve',
                'name_last': 'Yang',
                'email': 'z5374603@ad.unsw.edu.au',
                'handle_str': "steveyang",
            },
            {
                'u_id': user_2,
                'name_first': 'Bojin',
                'name_last': 'Li',
                'email': 'z5201314@ad.unsw.edu.au',
                'handle_str': "bojinli",
            },
        ],
    }

def test_channel_details_two_join_member(user_list, channel_id):
    user_1 = auth_login_v1("z5374603@ad.unsw.edu.au", "Ymc123")["auth_user_id"]
    user_2 = auth_login_v1("z5201314@ad.unsw.edu.au", "Bojin123")["auth_user_id"]
    user_3 = auth_login_v1("12345678@qq.com", "Cicy123")['auth_user_id']
    channel_join_v1(user_2, channel_id)
    channel_join_v1(user_3, channel_id)

    assert channel_details_v1(user_1, channel_id) == {
        'name': 'Channel_1',
        "is_public": True,
        'owner_members': [
            {
                'u_id': user_1,
                'name_first': 'Steve',
                'name_last': 'Yang',
                'email': 'z5374603@ad.unsw.edu.au',
                'handle_str': "steveyang",
            }
        ],
        'all_members': [
            {
                'u_id': user_1,
                'name_first': 'Steve',
                'name_last': 'Yang',
                'email': 'z5374603@ad.unsw.edu.au',
                'handle_str': "steveyang",
            },
            {
                'u_id': user_2,
                'name_first': 'Bojin',
                'name_last': 'Li',
                'email': 'z5201314@ad.unsw.edu.au',
                'handle_str': "bojinli",
            },
            {
                'u_id': user_3,
                'name_first': 'Cicy',
                'name_last': 'Zhou',
                'email': '12345678@qq.com',
                'handle_str': 'cicyzhou',
            },
        ],
    }

def test_channel_details_invite_one_members(user_list, channel_id):
    user_1 = auth_login_v1("z5374603@ad.unsw.edu.au", "Ymc123")['auth_user_id']
    user_2 = auth_login_v1("z5201314@ad.unsw.edu.au", "Bojin123")['auth_user_id']
    channel_invite_v1(user_1, channel_id, user_2)

    assert channel_details_v1(user_1, channel_id) == {
        'name': 'Channel_1',
        "is_public": True,
        'owner_members': [
            {
                'u_id': user_1,
                'name_first': 'Steve',
                'name_last': 'Yang',
                'email': 'z5374603@ad.unsw.edu.au',
                'handle_str': "steveyang",
            }
        ],
        'all_members': [
            {
                'u_id': user_1,
                'name_first': 'Steve',
                'name_last': 'Yang',
                'email': 'z5374603@ad.unsw.edu.au',
                'handle_str': "steveyang",
            },
            {
                'u_id': user_2,
                'name_first': 'Bojin',
                'name_last': 'Li',
                'email': 'z5201314@ad.unsw.edu.au',
                'handle_str': "bojinli",
            },
        ],
    }

def test_channel_details_invite_two_members(user_list, channel_id):
    user_1 = auth_login_v1("z5374603@ad.unsw.edu.au", "Ymc123")['auth_user_id']
    user_2 = auth_login_v1("z5201314@ad.unsw.edu.au", "Bojin123")['auth_user_id']
    user_3 = auth_login_v1("12345678@qq.com", "Cicy123")['auth_user_id']
    channel_invite_v1(user_1, channel_id, user_2)
    channel_invite_v1(user_1, channel_id, user_3)

    assert channel_details_v1(user_1, channel_id) == {
        'name': 'Channel_1',
        "is_public": True,
        'owner_members': [
            {
                'u_id': user_1,
                'name_first': 'Steve',
                'name_last': 'Yang',
                'email': 'z5374603@ad.unsw.edu.au',
                'handle_str': "steveyang",
            }
        ],
        'all_members': [
            {
                'u_id': user_1,
                'name_first': 'Steve',
                'name_last': 'Yang',
                'email': 'z5374603@ad.unsw.edu.au',
                'handle_str': "steveyang",
            },
            {
                'u_id': user_2,
                'name_first': 'Bojin',
                'name_last': 'Li',
                'email': 'z5201314@ad.unsw.edu.au',
                'handle_str': "bojinli",
            },
            {
                'u_id': user_3,
                'name_first': 'Cicy',
                'name_last': 'Zhou',
                'email': '12345678@qq.com',
                'handle_str': 'cicyzhou',
            },
        ],
    }
    
############################## Test for handle ####################################
def test_channel_details_three_members_cotain_the_same_name(user_list, channel_id):
    user_1 = auth_login_v1("z5374603@ad.unsw.edu.au", "Ymc123")['auth_user_id']
    user_2 = auth_login_v1("z5201314@ad.unsw.edu.au", "Bojin123")['auth_user_id']
    user_3 = auth_login_v1("13579@gmail.com", "Lebron123")['auth_user_id']
    user_4 = auth_login_v1("135798@gmail.com", "James123")['auth_user_id']
    
    channel_invite_v1(user_1, channel_id, user_2)
    channel_invite_v1(user_1, channel_id, user_3)
    channel_invite_v1(user_1, channel_id, user_4)

    assert channel_details_v1(user_1, channel_id) == {
        'name': 'Channel_1',
        "is_public": True,
        'owner_members': [
            {
                'u_id': user_1,
                'name_first': 'Steve',
                'name_last': 'Yang',
                'email': 'z5374603@ad.unsw.edu.au',
                'handle_str': "steveyang",
            }
        ],
        'all_members': [
            {
                'u_id': user_1,
                'name_first': 'Steve',
                'name_last': 'Yang',
                'email': 'z5374603@ad.unsw.edu.au',
                'handle_str': "steveyang",
            },
            {
                'u_id': user_2,
                'name_first': 'Bojin',
                'name_last': 'Li',
                'email': 'z5201314@ad.unsw.edu.au',
                'handle_str': "bojinli",
            },
            {
                'u_id': user_3,
                'name_first': 'Steve',
                'name_last': 'Yang',
                'email': '13579@gmail.com',
                'handle_str': 'steveyang0',
            },
            {
                'u_id': user_4,
                'name_first': 'Steve',
                'name_last': 'Yang',
                'email': '135798@gmail.com',
                'handle_str': 'steveyang1',
            },
        ],
    }
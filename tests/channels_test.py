import pytest

from src.channels import channels_create_v1
from src.auth import auth_register_v1
from src.error import InputError
from src.other import clear_v1

import random, string


@pytest.fixture
def clear():
    clear_v1()


@pytest.fixture
def create_user():
    user_list = list()
    user_list.append(
        auth_register_v1('elon.mask@spacex.com', 'Password', 'Elon', 'Musk'))
    user_list.append(
        auth_register_v1('mark.zuckerberg@meta.com', 'Password', 'Mark',
                         'Zuckerberg'))
    user_list.append(
        auth_register_v1('tim.cook@icloud.com', 'Password', 'Tim', 'Cook'))
    user_list.append(
        auth_register_v1('bill.gates@outlook.com', 'Password', 'Bill',
                         'Gates'))
    return user_list


def test_channels_create_name_too_short(clear, create_user):
    with pytest.raises(InputError):
        for user in create_user:
            channels_create_v1(user['auth_user_id'], '', True)


def test_channels_create_name_too_long(clear, create_user):
    name = random.sample(string.ascii_letters + string.digits, 21)
    with pytest.raises(InputError):
        for user in create_user:
            channels_create_v1(user['auth_user_id'], name, True)


def test_channels_create_all_normal(clear, create_user):
    channel_list = list()
    for user in create_user:
        channel_list.append(
            channels_create_v1(user['auth_user_id'], 'Tesla', True))
        # different channel name
        channel_list.append(
            channels_create_v1(user['auth_user_id'], 'SpaceX', True))
        # different channel type
        channel_list.append(
            channels_create_v1(user['auth_user_id'], 'SpaceX', False))
        # same channel name
        channel_list.append(
            channels_create_v1(user['auth_user_id'], 'SpaceX', False))
    for channel in channel_list:
        assert type(channel) == dict
        assert type(channel['channel_id']) == int

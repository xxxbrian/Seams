import random
import string
import pytest

from src.channels import channels_create_v1, channels_list_v1, channels_listall_v1
from src.auth import auth_register_v1
from src.error import InputError
from src.other import clear_v1

@pytest.fixture
def clear():
    clear_v1()

@pytest.fixture
def create_user():
    user_list = list()
    user_list.append(
                    auth_register_v1(
                                    'elon.mask@spacex.com',
                                    'Password',
                                    'Elon',
                                    'Musk'
                                    )
                    )
    user_list.append(
                    auth_register_v1(
                                    'mark.zuckerberg@meta.com',
                                    'Password',
                                    'Mark',
                                    'Zuckerberg'
                                    )
                    )
    user_list.append(
                    auth_register_v1(
                                    'tim.cook@icloud.com',
                                    'Password',
                                    'Tim',
                                    'Cook'
                                    )
                    )
    user_list.append(
                    auth_register_v1(
                                    'bill.gates@outlook.com',
                                    'Password',
                                    'Bill',
                                    'Gates'
                                    )
                    )
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
        assert isinstance(channel, dict)
        assert isinstance(channel['channel_id'], int)

def test_channels_list(clear, create_user):
    elon_group = {'id': [], 'list': []}  #elon's channel
    zuck_group = {'id': [], 'list': []}  #zuck's channel
    elon_group['id'].append(
        channels_create_v1(create_user[0]['auth_user_id'], 'Tesla',
                           True)['channel_id'])
    elon_group['id'].append(
        channels_create_v1(create_user[0]['auth_user_id'], 'SpaceX',
                           True)['channel_id'])
    elon_group['id'].append(
        channels_create_v1(create_user[0]['auth_user_id'], 'Dogecoin',
                           False)['channel_id'])
    zuck_group['id'].append(
        channels_create_v1(create_user[1]['auth_user_id'], 'Facebook',
                           True)['channel_id'])
    zuck_group['id'].append(
        channels_create_v1(create_user[1]['auth_user_id'], 'Metaverse',
                           False)['channel_id'])

    elon_group['list'] = channels_list_v1(
        create_user[0]['auth_user_id'])['channels']
    zuck_group['list'] = channels_list_v1(
        create_user[1]['auth_user_id'])['channels']

    for channel in elon_group['list']:
        assert channel['channel_id'] in elon_group['id']
        assert isinstance(channel['name'], str)
    for channel in zuck_group['list']:
        assert channel['channel_id'] in zuck_group['id']
        assert isinstance(channel['name'], str)


def test_channels_listall_v1(clear, create_user):
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

    assert len(channel_list) == len(
        channels_listall_v1(create_user[0]['auth_user_id'])['channels'])
    assert len(channel_list) == len(
        channels_listall_v1(create_user[1]['auth_user_id'])['channels'])

    for detial in channels_listall_v1(
            create_user[0]['auth_user_id'])['channels']:
        assert isinstance(detial['channel_id'], int)
        assert isinstance(detial['name'], str)

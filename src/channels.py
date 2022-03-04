from src.error import InputError
from src.type import User, Channel


def channels_list_v1(auth_user_id):
    return {
        'channels': [{
            'channel_id': 1,
            'name': 'My Channel',
        }],
    }


def channels_listall_v1(auth_user_id):
    return {
        'channels': [{
            'channel_id': 1,
            'name': 'My Channel',
        }],
    }


def channels_create_v1(auth_user_id, name, is_public):
    if Channel.check_name_invalid(name):
        raise InputError
    new_channel = Channel(auth_user_id, name, is_public)
    new_channel.add_to_store()
    return {
        'channel_id': new_channel.channel_id,
    }

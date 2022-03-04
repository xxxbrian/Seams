from src.error import AccessError, InputError
from src.type import User, Channel


def channels_list_v1(auth_user_id):
    user = User.find_by_id(auth_user_id)
    if user is None:
        raise AccessError
    channels_list = Channel.get_allchannel()
    info = list()
    for channel in channels_list:
        if user in channel.members:
            info.append(channel.todict({'channel_id', 'name'}))
    return {
        'channels': info,
    }


def channels_listall_v1(auth_user_id):
    if User.find_by_id(auth_user_id) is None:
        raise AccessError
    channels_list = Channel.get_allchannel()
    info = list()
    for channel in channels_list:
        info.append(channel.todict({'channel_id', 'name'}))
    return {
        'channels': info,
    }


def channels_create_v1(auth_user_id, name, is_public):
    if Channel.check_name_invalid(name):
        raise InputError
    new_channel = Channel(auth_user_id, name, is_public)
    new_channel.add_to_store()
    return {
        'channel_id': new_channel.channel_id,
    }

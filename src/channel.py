from src.error import InputError, AccessError
from src.type import User, Channel


def channel_invite_v1(auth_user_id, channel_id, u_id):
    user = User.find_by_id(u_id)
    channel = Channel.find_by_id(channel_id)
    if channel is None:
        raise InputError
    if user is None:
        raise InputError
    if channel.has_user(u_id) is True:
        raise InputError
    if Channel.find_by_id(channel_id) is not None and channel.has_user(auth_user_id) is False:
        raise AccessError

    channel.join(user)
    return {}


def channel_details_v1(auth_user_id, channel_id):
    channel = Channel.find_by_id(channel_id)
    if channel is None:
        raise InputError
    if channel.has_user(auth_user_id) == False:
        raise AccessError
    
    channel_info = channel.todict(
        {'name', 'is_public', 'owner_members', 'all_members'})
    return channel_info


def channel_messages_v1(auth_user_id, channel_id, start):
    channel = Channel.find_by_id(channel_id)
    if channel is None:
        raise InputError
    
    return {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
        'start': 0,
        'end': 50,
    }


def channel_join_v1(auth_user_id, channel_id):
    channel = Channel.find_by_id(channel_id)
    if channel is None:
        raise InputError
    if Channel.has_user(channel, auth_user_id) is True:
        raise InputError
    if channel.is_public is False and channel.has_user(auth_user_id) is False:
        raise AccessError
    
    user = User.find_by_id(auth_user_id)
    channel.join(user)
    return {}

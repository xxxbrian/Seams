from src.type import User, Channel, Message
from src.error import InputError, AccessError
import threading
from src.type import pickelsave


@pickelsave
def standup_start_v1(token: str, channel_id: int, length: int):
    user = User.find_by_token(token)
    channel = Channel.find_by_id(channel_id)
    if user is None:
        raise AccessError(description='Permission denied')
    if channel is None:
        raise InputError(description='Channel not found')
    if length < 0:
        raise InputError(description='Length invalid')
    if not channel.has_user(user):
        raise AccessError(description='Permission denied: Not member')
    if channel.standup['is_active']:
        raise InputError(description='Already active standup')
    finish_time = int(Message.utc_timestamp() + length)
    channel.standup_set(user, finish_time)
    standup_do = pickelsave(channel.standup_do)
    standup = threading.Timer(length, standup_do)
    standup.start()
    return {'time_finish': finish_time}


def standup_active_v1(token, channel_id):
    user = User.find_by_token(token)
    channel = Channel.find_by_id(channel_id)
    if user is None:
        raise AccessError(description='Permission denied')
    if channel is None:
        raise InputError(description='Channel not found')
    if not channel.has_user(user):
        raise AccessError(description='Permission denied: Not member')
    return {
        key: value
        for key, value in channel.standup.items()
        if key in {'is_active', 'time_finish'}
    }


@pickelsave
def standup_send_v1(token, channel_id, message):
    user = User.find_by_token(token)
    channel = Channel.find_by_id(channel_id)
    if user is None:
        raise AccessError(description='Permission denied')
    if channel is None:
        raise InputError(description='Channel not found')
    if len(message) > 1000:
        raise InputError(description='Message length invalid')
    if not channel.has_user(user):
        raise AccessError(description='Permission denied: Not member')
    if not channel.standup['is_active']:
        raise InputError(description='Standup not running')
    channel.standup_add(user, message)
    return {}

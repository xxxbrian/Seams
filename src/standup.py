from src.type import User, Channel, Message
from src.error import InputError, AccessError
import threading
from src.type import pickelsave


@pickelsave
def standup_start_v1(token: str, channel_id: int, length: int):
    """For a given channel, start the standup period whereby for the 
    next "length" seconds if someone calls "standup/send" with a message, 
    it is buffered during the X second window then at the end of the X 
    second window a message will be added to the message queue in the 
    channel from the user who started the standup. "length" is an integer 
    that denotes the number of seconds that the standup occurs for. If no 
    standup messages were sent during the duration of the standup, no message 
    should be sent at the end.

    Args:
        token (str): user's token
        channel_id (int): channel's id
        length (int): length of standup

    Raises:
        AccessError: token invalid
        InputError: channel_id does not refer to a valid channel
        InputError: length is a negative integer
        AccessError: channel_id is valid and the authorised user is not a member of the channel
        InputError: an active standup is currently running in the channel

    Returns:
        dict: dictionary of time_finish
    """
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
    """For a given channel, return whether a standup is active in it, 
    and what time the standup finishes. If no standup is active, then 
    time_finish returns None.

    Args:
        token (str): user's token
        channel_id (int): channel's id

    Raises:
        AccessError: token invalid
        InputError: channel_id does not refer to a valid channel
        AccessError: channel_id is valid and the authorised user 
                    is not a member of the channel

    Returns:
        _type_: _description_
    """
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
    """Sending a message to get buffered in the standup queue, assuming a 
    standup is currently active. Note: @ tags should not be parsed as proper 
    tags when sending to standup/send

    Args:
        token (str): _description_
        channel_id (int): _description_
        message (str): _description_

    Raises:
        AccessError: token invalid
        InputError: channel_id does not refer to a valid channel
        InputError: length of message is over 1000 characters
        AccessError: channel_id is valid and the authorised user is not a member of the channel
        InputError: an active standup is not currently running in the channel

    Returns:
        dict: empty dictionary
    """
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

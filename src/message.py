from src.type import User, Channel, DM, Message
from src.error import AccessError, InputError

from datetime import timezone
import datetime


def message_send_v1(token, channel_id, message):
    dt = datetime.datetime.now(timezone.utc)
    utc_time = dt.replace(tzinfo=timezone.utc)
    utc_timestamp = utc_time.timestamp()
    user = User.find_by_token(token)
    channel = Channel.find_by_id(channel_id)
    if user is None:
        raise AccessError(description='Permission denied')
    if channel is None:
        raise InputError(description='Channel not found')
    if not channel.has_user(user):
        raise AccessError(description='Permission denied: Not member')
    if Message.check_length_invalid(message):
        raise InputError('Message lenght invalid')
    new_msg = Message(user.u_id, message, utc_timestamp)
    new_msg.add_to_store()
    new_msg.add_to_channel(channel)
    return {}


def message_edit_v1(token, message_id, message):
    return {}


def message_remove_v1(token, message_id):
    return {}


def message_senddm_v1(token, dm_id, message):
    return {}

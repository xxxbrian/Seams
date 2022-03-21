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
    new_msg = Message(user.u_id, message, utc_timestamp, channel)
    new_msg.add_to_store()
    return {'message_id': new_msg.message_id}


def message_edit_v1(token, message_id, message):
    user = User.find_by_token(token)
    msg = Message.find_by_id(message_id)
    if user is None:
        raise AccessError(description='Permission denied')
    if msg is None:
        raise InputError(description='Message not found')
    if not msg.sub.has_user(user):
        raise InputError(description='Message not found')
    if user.u_id != msg.u_id and not user.is_admin():
        raise AccessError(description='Permission denied: Not sender')
    if len(message) == 0:
        msg.remove()
        return {}
    elif Message.check_length_invalid(message):
        raise InputError('Message lenght invalid')
    msg.content = message
    return {}


def message_remove_v1(token, message_id):
    return message_edit_v1(token, message_id, '')


def message_senddm_v1(token, dm_id, message):
    dt = datetime.datetime.now(timezone.utc)
    utc_time = dt.replace(tzinfo=timezone.utc)
    utc_timestamp = utc_time.timestamp()
    user = User.find_by_token(token)
    dm = DM.find_by_id(dm_id)
    if user is None:
        raise AccessError(description='Permission denied')
    if dm is None:
        raise InputError(description='DM not found')
    if not dm.has_user(user):
        raise AccessError(description='Permission denied: Not member')
    if Message.check_length_invalid(message):
        raise InputError('Message lenght invalid')
    new_msg = Message(user.u_id, message, utc_timestamp, dm)
    new_msg.add_to_store()
    return {'message_id': new_msg.message_id}

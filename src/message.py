from src.type import User, Channel, DM, Message, Notification
from src.error import AccessError, InputError
from src.type import pickelsave

from datetime import timezone
import datetime


@pickelsave
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


@pickelsave
def message_edit_v1(token, message_id, message):
    user = User.find_by_token(token)
    msg = Message.find_by_id(message_id)
    if user is None:
        raise AccessError(description='Permission denied')
    if msg is None:
        raise InputError(description='Message not found')
    if not msg.sup.has_user(user):
        raise InputError(description='Message not found')
    if user.u_id != msg.u_id and not msg.sup.has_owner(user):
        raise AccessError(description='Permission denied: Not sender')
    if len(message) == 0:
        msg.remove()
        return {}
    elif Message.check_length_invalid(message):
        raise InputError('Message lenght invalid')
    msg.content = message
    return {}


@pickelsave
def message_remove_v1(token, message_id):
    return message_edit_v1(token, message_id, '')


@pickelsave
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
        raise InputError(description='Message length invalid')
    new_msg = Message(user.u_id, message, utc_timestamp, dm)
    new_msg.add_to_store()
    return {'message_id': new_msg.message_id}


@pickelsave
def message_share_v1(token, og_message_id, message, channel_id, dm_id):
    dt = datetime.datetime.now(timezone.utc)
    utc_time = dt.replace(tzinfo=timezone.utc)
    utc_timestamp = utc_time.timestamp()
    user = User.find_by_token(token)
    ogmsg = Message.find_by_id(og_message_id)
    if user is None:
        raise AccessError(description='Permission denied')
    if ogmsg is None:
        raise InputError(description='Message not found')
    if channel_id != -1 and dm_id != -1:
        raise InputError(description='Takes exactly one target (2 given)')
    channel = Channel.find_by_id(channel_id)
    dm = DM.find_by_id(dm_id)
    if channel is None and dm is None:
        raise InputError(description='Channel/DM id invaild')
    if Message.check_length_invalid(message):
        raise InputError(description='Message length invalid')
    sup = channel if dm is None else dm
    if not sup.has_user(user):
        raise AccessError(
            description='Permission denied: Join channel/dm first')
    content = f'{message}\n>>>{ogmsg.content}'
    new_msg = Message(user.u_id, content, utc_timestamp, sup)
    new_msg.add_to_store()
    return {'message_id': new_msg.message_id}


@pickelsave
def message_react_v1(token, message_id, react_id):
    user = User.find_by_token(token)
    msg = Message.find_by_id(message_id)
    if user is None:
        raise AccessError(description='Permission denied')
    if msg is None:
        raise InputError(description='Message not found')
    if not msg.sup.has_user(user):
        raise InputError(description='Message not found')
    if not react_id in msg.react.keys():
        raise InputError(description='Invaild react type')
    if user in msg.react[react_id]:
        raise InputError(description='Already reacting')
    msg.react[react_id].append(user)
    if msg.sup.has_user(msg.sender):
        new_nf = Notification(
            msg.sup,
            f'{user.handle_str} reacted to your message in {msg.sup.name}')
        msg.sender.add_notification(new_nf)
    return {}
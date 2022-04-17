from src.type import User, Channel, DM, Message, Notification
from src.error import AccessError, InputError
from src.type import pickelsave


@pickelsave
def message_send_v1(token, channel_id, message):
    utc_timestamp = Message.utc_timestamp()
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
    print(new_msg.todict({}))
    tagged_user_list = Message.get_tagged_user(message)
    for tagged_user in tagged_user_list:
        if channel.has_user(tagged_user):
            new_nf = Notification(
                channel,
                f'{user.handle_str} tagged you in {channel.name}: {message[0:20]}'
            )
            tagged_user.add_notification(new_nf)
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
    utc_timestamp = Message.utc_timestamp()
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
    tagged_user_list = Message.get_tagged_user(message)
    for tagged_user in tagged_user_list:
        if dm.has_user(tagged_user):
            new_nf = Notification(
                dm,
                f'{user.handle_str} tagged you in {dm.name}: {message[0:20]}')
            tagged_user.add_notification(new_nf)
    return {'message_id': new_msg.message_id}


@pickelsave
def message_share_v1(token, og_message_id, message, channel_id, dm_id):
    utc_timestamp = Message.utc_timestamp()
    user = User.find_by_token(token)
    ogmsg = Message.find_by_id(og_message_id)
    if user is None:
        raise AccessError(description='Permission denied')
    if ogmsg is None:
        raise InputError(description='Message not found')
    if not ogmsg.sup.has_user(user):
        raise InputError(description='Message not found')
    channel = Channel.find_by_id(channel_id)
    dm = DM.find_by_id(dm_id)
    if channel is None and dm is None:
        raise InputError(description='Channel/DM id invaild')
    if channel_id != -1 and dm_id != -1:
        raise InputError(description='Takes exactly one target (2 given)')
    if len(message) > 1000:
        raise InputError(description='Message length invalid')
    sup = channel if dm is None else dm
    if not sup.has_user(user):
        raise AccessError(
            description='Permission denied: Join channel/dm first')
    content = f'{message}\n>>>{ogmsg.content}'
    new_msg = Message(user.u_id, content, utc_timestamp, sup)
    new_msg.add_to_store()
    tagged_user_list = Message.get_tagged_user(message)
    for tagged_user in tagged_user_list:
        if sup.has_user(tagged_user):
            new_nf = Notification(
                channel,
                f'{user.handle_str} tagged you in {sup.name}: {message[0:20]}')
            tagged_user.add_notification(new_nf)
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
    if not react_id in msg.react_dict.keys():
        raise InputError(description='Invalid react type')
    if user in msg.react_dict[react_id]:
        raise InputError(description='Already reacting')
    msg.react_dict[react_id].append(user)
    if msg.sup.has_user(msg.sender):
        new_nf = Notification(
            msg.sup,
            f'{user.handle_str} reacted to your message in {msg.sup.name}')
        msg.sender.add_notification(new_nf)
    return {}


@pickelsave
def message_unreact_v1(token, message_id, react_id):
    user = User.find_by_token(token)
    msg = Message.find_by_id(message_id)
    if user is None:
        raise AccessError(description='Permission denied')
    if msg is None:
        raise InputError(description='Message not found')
    if not msg.sup.has_user(user):
        raise InputError(description='Message not found')
    if not react_id in msg.react_dict.keys():
        raise InputError(description='Invalid react type')
    if not user in msg.react_dict[react_id]:
        raise InputError(description='No reacting')
    msg.react_dict[react_id].remove(user)
    return {}


@pickelsave
def message_pin_v1(token, message_id):
    user = User.find_by_token(token)
    msg = Message.find_by_id(message_id)
    if user is None:
        raise AccessError(description='Permission denied')
    if msg is None:
        raise InputError(description='Message not found')
    if not msg.sup.has_user(user):
        raise InputError(description='Message not found')
    if not msg.sup.has_owner(user):
        raise AccessError(description='Permission denied')
    if msg.is_pinned:
        raise InputError(description='Already pinned')
    msg.is_pinned = True
    return {}


@pickelsave
def message_unpin_v1(token, message_id):
    user = User.find_by_token(token)
    msg = Message.find_by_id(message_id)
    if user is None:
        raise AccessError(description='Permission denied')
    if msg is None:
        raise InputError(description='Message not found')
    if not msg.sup.has_user(user):
        raise InputError(description='Message not found')
    if not msg.sup.has_owner(user):
        raise AccessError(description='Permission denied')
    if not msg.is_pinned:
        raise InputError(description='Not pinned')
    msg.is_pinned = False
    return {}


@pickelsave
def message_sendlater_v1(token, channel_id, message, time_sent):
    utc_timestamp = Message.utc_timestamp()
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
    if time_sent < utc_timestamp:
        raise InputError(description='Time in the past')
    new_msg = Message(user.u_id, message, time_sent, channel)
    new_msg.add_to_store()
    tagged_user_list = Message.get_tagged_user(message)
    for tagged_user in tagged_user_list:
        if channel.has_user(tagged_user):
            new_nf = Notification(
                channel,
                f'{user.handle_str} tagged you in {channel.name}: {message[0:20]}',
                time_sent)
            tagged_user.add_notification(new_nf)

    return {'message_id': new_msg.message_id}


@pickelsave
def message_sendlaterdm_v1(token, dm_id, message, time_sent):
    utc_timestamp = Message.utc_timestamp()
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
    if time_sent < utc_timestamp:
        raise InputError(description='Time in the past')
    new_msg = Message(user.u_id, message, time_sent, dm)
    new_msg.add_to_store()
    tagged_user_list = Message.get_tagged_user(message)
    for tagged_user in tagged_user_list:
        if dm.has_user(tagged_user):
            new_nf = Notification(
                dm,
                f'{user.handle_str} tagged you in {dm.name}: {message[0:20]}',
                time_sent)
            tagged_user.add_notification(new_nf)
    return {'message_id': new_msg.message_id}

from src.type import User, Channel, DM, Message, Notification
from src.error import AccessError, InputError
from src.type import pickelsave


@pickelsave
def message_send_v1(token, channel_id, message):
    """Send a message from the authorised user to the channel 
    specified by channel_id. Note: Each message should have its 
    own unique ID, i.e. no messages should share an ID with 
    another message, even if that other message is in a different 
    channel.

    Args:
        token (str): user's token
        channel_id (int): channel's id
        message (str): message

    Raises:
        AccessError: if token is invalid
        InputError: if channel_id does not refer to a valid channel
        AccessError: if channel_id refers to a channel that is private 
                    and the authorised user is not already a channel 
                    member and is not a global owner
        InputError: if message is empty

    Returns:
        dict: dictionary of message_id
    """
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
    """Given a message, update its text with new text. 
    If the new message is an empty string, the message 
    is deleted. If a shared/standup message is edited, 
    the entire contents will be edited as if it was a 
    normal message.

    Args:
        token (str): user's token
        message_id (int): message's id
        message (str): message content

    Raises:
        AccessError: if token is invalid
        InputError: length of message is over 1000 characters
        InputError: message_id does not refer to a valid message 
                    within a channel/DM that the authorised user has joined
        AccessError: message_id refers to a valid message in a joined 
                    channel/DM and none of the following are true:
                    a. the message was sent by the authorised user making this request
                    b. the authorised user has owner permissions in the channel/DM

    Returns:
        dict: empty dictionary
    """
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
    """Given a message_id for a message, this message is removed from the channel/DM"""
    return message_edit_v1(token, message_id, '')


@pickelsave
def message_senddm_v1(token, dm_id, message):
    """Send a message from authorised_user to the DM 
    specified by dm_id. Note: Each message should have 
    it's own unique ID, i.e. no messages should share 
    an ID with another message, even if that other message 
    is in a different channel or DM.

    Args:
        token (str): user's token
        message_id (int): message's id
        message (str): new message content

    Raises:
        AccessError: if token is invalid
        InputError: dm_id does not refer to a valid DM
        InputError: length of message is less than 1 or over 1000 characters
        AccessError: dm_id is valid and the authorised user is not a member of the DM

    Returns:
        dict: empty dict
    """
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
    """og_message_id is the ID of the original message. channel_id is 
    the channel that the message is being shared to, and is -1 if it 
    is being sent to a DM. dm_id is the DM that the message is being 
    shared to, and is -1 if it is being sent to a channel. message is 
    the optional message in addition to the shared message, and will 
    be an empty string '' if no message is given.

    A new message should be sent to the channel/DM identified by the 
    channel_id/dm_id that contains the contents of both the original 
    message and the optional message. The format does not matter as 
    long as both the original and optional message exist as a substring 
    within the new message. Once sent, this new message has no link to 
    the original message, so if the original message is edited/deleted, 
    no change will occur for the new message.

    Args:
        token (str): user's token
        og_message_id (int): original message's id
        message (str): content of share message
        channel_id (int): channel's id
        dm_id (int): DM's id

    Raises:
        AccessError: if token is invalid
        InputError: both channel_id and dm_id are invalid
        InputError: neither channel_id nor dm_id are -1
        InputError: og_message_id does not refer to a valid message within 
                    a channel/DM that the authorised user has joined
        InputError: length of message is more than 1000 characters
        AccessError: the pair of channel_id and dm_id are valid (i.e. one 
                    is -1, the other is valid) and the authorised user has 
                    not joined the channel or DM they are trying to share 
                    the message to

    Returns:
        dict: dictionary of message_id
    """
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
    """Given a message within a channel or DM the authorised 
    user is part of, add a "react" to that particular message.

    Args:
        token (str): user's token
        message_id (int): message's id
        react_id (int): react's id

    Raises:
        AccessError: if token is invalid
        InputError: message_id is not a valid message within a 
                    channel or DM that the authorised user has joined
        InputError: react_id is not a valid react ID - currently, the 
                    only valid react ID the frontend has is 1
        InputError: the message already contains a react with ID react_id 
                    from the authorised user

    Returns:
        dict: empty dict
    """
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
    """Given a message within a channel or DM the authorised user 
    is part of, remove a "react" to that particular message.

    Args:
        token (str): token of user
        message_id (int): message's id
        react_id (int): react's id

    Raises:
        AccessError: if token is invalid
        InputError: message_id is not a valid message within a channel 
                    or DM that the authorised user has joined
        InputError: react_id is not a valid react ID
        InputError: the message does not contain a react with ID react_id 
                    from the authorised user

    Returns:
        dict: empty dict
    """
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
    """Given a message within a channel or DM, mark it as "pinned".

    Args:
        token (str): user's token
        message_id (int): message's id

    Raises:
        AccessError: if token is invalid
        InputError: message_id is not a valid message within a 
                    channel or DM that the authorised user has joined
        InputError: the message is already pinned
        AccessError: message_id refers to a valid message in a joined 
                    channel/DM and the authorised user does not have 
                    owner permissions in the channel/DM

    Returns:
        dict: empty dict
    """
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
    """Given a message within a channel or DM, remove its mark as pinned.

    Args:
        token (str): user's token
        message_id (int): message's id

    Raises:
        AccessError: if token is invalid
        InputError: message_id is not a valid message within a channel 
                    or DM that the authorised user has joined
        InputError: the message is not already pinned
        AccessError: message_id refers to a valid message in a joined 
                    channel/DM and the authorised user does not have 
                    owner permissions in the channel/DM

    Returns:
        dict: empty dict
    """
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
    """Send a message from the authorised user to the channel specified 
    by channel_id automatically at a specified time in the future. The 
    returned message_id will only be considered valid for other actions 
    (editing/deleting/reacting/etc) once it has been sent (i.e. after time_sent). 
    You do not need to consider cases where a user's token is invalidated 
    or a user leaves before the message is scheduled to be sent.

    Args:
        token (str): user's token
        channel_id (int): channel's id
        message (str): message to be sent
        time_sent (int): time of message to be sent

    Raises:
        AccessError: if token is invalid
        InputError: channel_id does not refer to a valid channel
        AccessError: channel_id is valid and the authorised user 
                    is not a member of the channel they are trying 
                    to post to
        InputError: length of message is less than 1 or over 1000 characters
        InputError: time_sent is a time in the past

    Returns:
        dict: dict of message_id
    """
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
    """Send a message from the authorised user to the DM specified by dm_id 
    automatically at a specified time in the future. The returned message_id 
    will only be considered valid for other actions (editing/deleting/reacting/etc) 
    once it has been sent (i.e. after time_sent). If the DM is removed before the 
    message has sent, the message will not be sent. You do not need to consider cases 
    where a user's token is invalidated or a user leaves before the message is 
    scheduled to be sent.

    Args:
        token (str): user's token
        dm_id (int): dm's id
        message (str): message to be sent
        time_sent (str): time of message to be sent

    Raises:
        AccessError: if token is invalid
        InputError: dm_id does not refer to a valid DM
        AccessError: dm_id is valid and the authorised user is not a member of the DM 
                    they are trying to post to
        InputError: time_sent is a time in the past
        InputError: length of message is less than 1 or over 1000 characters

    Returns:
        dict: dict of message_id
    """
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

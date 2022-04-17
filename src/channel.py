from src.error import InputError, AccessError
from src.type import User, Channel, Notification
from src.type import pickelsave


@pickelsave
def channel_invite_v2(token, channel_id, u_id):
    """Invites a user with ID u_id to join a channel with ID channel_id. Once invited, the user is added to the channel immediately. In both public and private channels, all members are able to invite users.

    Args:
        token (string): token of user
        channel_id (integer): channel's id
        u_id (integer): user's id

    Raises:
        AccessError: channel_id is valid and the authorised user is not a member of the channel
        InputError: channel_id does not refer to a valid channel
        AccessError: u_id does not refer to a valid user
        InputError: u_id refers to a user who is already a member of the channel

    Returns:
        dictionary: {}
    """

    auth_user = User.find_by_token(token)
    user = User.find_by_id(u_id)
    channel = Channel.find_by_id(channel_id)
    if auth_user is None:
        raise AccessError(description='Permission denied')
    if channel is None:
        raise InputError(description='Channel not found')
    if not channel.has_user(auth_user):
        raise AccessError(description='Permission denied')
    if user is None:
        raise InputError(description='User not found')
    if channel.has_user(user):
        raise InputError(description='Already in channel')

    channel.join(user)
    new_nf = Notification(
        channel, f'{auth_user.handle_str} added you to {channel.name}')
    user.add_notification(new_nf)
    return {}


def channel_details_v2(token, channel_id):
    """Given a channel with ID channel_id that the authorised user is a member of, provide basic details about the channel.

    Args:
        token (string): token of user
        channel_id (integer): channel's id

    Raises:
        AccessError: token invalid
        InputError: channel_id does not refer to a valid channel
        AccessError: channel_id is valid and the authorised user is not a member of the channel

    Returns:
        dictionary: { name, is_public, owner_members, all_members }
    """

    user = User.find_by_token(token)
    channel = Channel.find_by_id(channel_id)
    if user is None:
        raise AccessError(description='Permission denied')
    if channel is None:
        raise InputError(description='Channel not found')
    if not channel.has_user(user):
        raise AccessError(description='Permission denied: Join channel first')
    print(f'cov-{channel.todict({})}')
    channel_info = channel.todict(
        {'name', 'is_public', 'owner_members', 'all_members'})
    return channel_info


def channel_messages_v2(token, channel_id, start):
    """Given a channel with ID channel_id that the authorised user is a member of, return up to 50 messages between index "start" and "start + 50". Message with index 0 is the most recent message in the channel. This function returns a new index "end" which is the value of "start + 50", or, if this function has returned the least recent messages in the channel, returns -1 in "end" to indicate there are no more messages to load after this return.

    Args:
        token (string): token of user
        channel_id (integer): channel's id
        start (integer): index of message

    Raises:
        AccessError: token invalid
        InputError: channel_id does not refer to a valid channel
        AccessError: channel_id is valid and the authorised user is not a member of the channel
        InputError: start is greater than the total number of messages in the channel

    Returns:
        dictionary: {}
    """

    user = User.find_by_token(token)
    channel = Channel.find_by_id(channel_id)
    if user is None:
        raise AccessError(description='Permission denied')
    if channel is None:
        raise InputError(description='Channel not found')
    if not channel.has_user(user):
        raise AccessError(description='Permission denied: Join channel first')
    message_amount = len(channel.get_messages())
    if start > message_amount:
        raise InputError(description='Message not found')

    # Message with index 0 is the most recent message in the channel.
    end = start + 50 if start + 50 <= message_amount else -1
    msg_list = [
        msg.todict(auth_user=user) for msg in channel.get_messages(start, end)
    ]
    return {
        'messages': msg_list,
        'start': start,
        'end': end,
    }


@pickelsave
def channel_join_v2(token, channel_id):
    """Given a channel_id of a channel that the authorised user can join, adds them to that channel.

    Args:
        token (string): token of user
        channel_id (integer): channel's id

    Raises:
        AccessError: token invalid
        InputError: channel_id does not refer to a valid channel
        InputError: the authorised user is already a member of the channel
        AccessError: channel_id refers to a channel that is private and the authorised user is not already a channel member and is not a global owner

    Returns:
        dictionary: {}
    """

    user = User.find_by_token(token)
    channel = Channel.find_by_id(channel_id)

    if user is None:
        raise AccessError(description='Permission denied')
    if channel is None:
        raise InputError(description='Channel not found')
    if channel.has_user(user):
        raise InputError(description='Already in channel')
    if not channel.is_public and user.group_id != 0:
        raise AccessError(
            description='Permission denied: Channel not available')

    channel.join(user)
    return {}


@pickelsave
def channel_leave_v1(token, channel_id):
    """Given a channel with ID channel_id that the authorised user is a member of, remove them as a member of the channel. Their messages should remain in the channel. If the only channel owner leaves, the channel will remain.

    Args:
        token (string): token of user
        channel_id (_type_): channel's id

    Raises:
        AccessError: token invalid
        InputError: channel_id does not refer to a valid channel
        AccessError: channel_id is valid and the authorised user is not a member of the channel

    Returns:
        dictionary: {}
    """
    user = User.find_by_token(token)
    channel = Channel.find_by_id(channel_id)
    if user is None:
        raise AccessError(description='Permission denied')
    if channel is None:
        raise InputError(description='Channel not found')
    if not channel.has_user(user):
        raise AccessError(description='Permission denied: Not member')
    if user is channel.standup['auth_user']:
        raise InputError(description='Standup starter can not leave')
    if user in channel.owners:
        channel.removeowner(user)
    channel.leave(user)
    return {}


@pickelsave
def channel_addowner_v1(token, channel_id, u_id):
    """Make user with user id u_id an owner of the channel.

    Args:
        token (string): token of user
        channel_id (integer): channel's id
        u_id (integer): user's id

    Raises:
        AccessError: token invalid
        InputError: channel_id does not refer to a valid channel
        AccessError: channel_id is valid and the authorised user does not have owner permissions in the channel
        InputError: u_id does not refer to a valid user
        InputError: u_id refers to a user who is not a member of the channel
        InputError: u_id refers to a user who is already an owner of the channel

    Returns:
        dictionary: {}
    """
    auth_user = User.find_by_token(token)
    channel = Channel.find_by_id(channel_id)
    user = User.find_by_id(u_id)
    if auth_user is None:
        raise AccessError(description='Permission denied')
    if channel is None:
        raise InputError(description='Channel not found')
    if not channel.has_owner(auth_user):
        raise AccessError(description='Permission denied: Not owner')
    if user is None:
        raise InputError(description='User not found')
    if not channel.has_user(user):
        raise InputError(description='Invite user join first')
    if user in channel.owners:
        raise InputError(description='Already a owner')
    channel.addowner(user)
    return {}


@pickelsave
def channel_removeowner_v1(token, channel_id, u_id):
    """Remove user with user id u_id as an owner of the channel.

    Args:
        token (string): token of user
        channel_id (integer): channel's id
        u_id (integer): user's id

    Raises:
        AccessError: token invalid
        InputError: channel_id does not refer to a valid channel
        AccessError: channel_id is valid and the authorised user does not have owner permissions in the channel
        InputError: u_id does not refer to a valid user
        InputError: u_id refers to a user who is not an owner of the channel
        InputError: u_id refers to a user who is currently the only owner of the channel

    Returns:
        dictionary: {}
    """
    auth_user = User.find_by_token(token)
    channel = Channel.find_by_id(channel_id)
    user = User.find_by_id(u_id)
    if auth_user is None:
        raise AccessError(description='Permission denied')
    if channel is None:
        raise InputError(description='Channel not found')
    if not channel.has_owner(auth_user):
        raise AccessError(description='Permission denied: Not owner')
    if user is None:
        raise InputError(description='User not found')
    if not user in channel.owners:
        raise InputError(description='Not a owner')
    if len(channel.owners) < 2:
        raise InputError(description='Cannot remove last owner')
    channel.removeowner(user)
    return {}

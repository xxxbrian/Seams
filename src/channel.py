from src.error import InputError, AccessError
from src.type import User, Channel


def channel_invite_v1(auth_user_id, channel_id, u_id):
    """Invites a user with ID u_id to join a channel with ID channel_id.
    Once invited, the user is added to the channel immediately."""

    auth_user = User.find_by_id(auth_user_id)
    user = User.find_by_id(u_id)
    channel = Channel.find_by_id(channel_id)
    if channel is None:
        raise InputError
    if user is None:
        raise InputError
    if channel.has_user(user):
        raise InputError
    if not channel.has_user(auth_user):
        raise AccessError

    channel.join(user)
    return {}


def channel_details_v1(auth_user_id, channel_id):
    """Given channel_id that the authorised user is a member of,
    provide basic details about the channel."""

    user = User.find_by_id(auth_user_id)
    channel = Channel.find_by_id(channel_id)
    if channel is None:
        raise InputError
    if not channel.has_user(user):
        raise AccessError

    channel_info = channel.todict(
        {'name', 'is_public', 'owner_members', 'all_members'})
    return channel_info


def channel_messages_v1(auth_user_id, channel_id, start):
    """given a channel that the user is a part of,
        return up to 50 messages between index
        start" and "start + 50"""

    channel = Channel.find_by_id(channel_id)
    if channel is None:
        raise InputError
    if start > len(channel.messages):
        raise InputError
    if not channel.has_user(User):
        raise AccessError

    # Message with index 0 is the most recent message in the channel.
    end = start + 50 if start + 50 <= len(channel.messages) else -1
    msg_list = list(msg.todict() for msg in channel.get_message(start, end))
    return {
        'messages': msg_list,
        'start': start,
        'end': end,
    }


def channel_join_v1(auth_user_id, channel_id):
    """Given a channel that the authorised user can join,
    adds them to that channel."""

    channel = Channel.find_by_id(channel_id)
    user = User.find_by_id(auth_user_id)

    if channel is None:
        raise InputError
    if channel.has_user(user):
        raise InputError
    if not channel.is_public:
        raise AccessError

    channel.join(user)
    return {}

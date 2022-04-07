from src.error import AccessError, InputError
from src.type import User, Channel
from src.type import pickelsave


def channels_list_v2(token):
    """Invites a user with u_id to join a channel with channel_id.
    Once invited, the user is added to the channel immediately."""

    user = User.find_by_token(token)
    if user is None:
        raise AccessError(description='Permission denied')

    channels_list = Channel.get_all()
    info = []

    for channel in channels_list:
        if user in channel.members:
            info.append(channel.todict({'channel_id', 'name'}))

    return {
        'channels': info,
    }


def channels_listall_v2(token):
    """Provide a list of all channels, including private channels,
        and their associated details"""

    if User.find_by_token(token) is None:
        raise AccessError(description='Permission denied')
    channels_list = Channel.get_all()
    info = []
    for channel in channels_list:
        info.append(channel.todict({'channel_id', 'name'}))

    return {
        'channels': info,
    }


@pickelsave
def channels_create_v2(token, name, is_public):
    """Creates a new channel with 'name' (either public or private).
        The user who created it automatically joins the channel"""

    user = User.find_by_token(token)
    if user is None:
        raise AccessError(description='Permission denied')
    if Channel.check_name_invalid(name):
        raise InputError(description='Channel name invalid')
    new_channel = Channel(user.u_id, name, is_public)
    new_channel.add_to_store()

    return {
        'channel_id': new_channel.channel_id,
    }

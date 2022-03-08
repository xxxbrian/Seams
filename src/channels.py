from src.error import AccessError, InputError
from src.type import User, Channel


def channels_list_v1(auth_user_id):
    """Invites a user with u_id to join a channel with channel_id.
        Once invited, the user is added to the channel immediately."""

    user = User.find_by_id(auth_user_id)
    channels_list = Channel.get_allchannel()
    info = list()

    for channel in channels_list:
        if user in channel.members:
            info.append(channel.todict({'channel_id', 'name'}))

    return {
        'channels': info,
    }


def channels_listall_v1(auth_user_id):
    """Provide a list of all channels, including private channels,
        and their associated details"""

    channels_list = Channel.get_allchannel()
    info = list()
    for channel in channels_list:
        info.append(channel.todict({'channel_id', 'name'}))

    return {
        'channels': info,
    }


def channels_create_v1(auth_user_id, name, is_public):
    """Creates a new channel with 'name' (either public or private).
        The user who created it automatically joins the channel"""

    if Channel.check_name_invalid(name):
        raise InputError
    new_channel = Channel(auth_user_id, name, is_public)
    new_channel.add_to_store()

    return {
        'channel_id': new_channel.channel_id,
    }

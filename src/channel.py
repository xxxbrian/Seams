from src.type import User, Channel


def channel_invite_v1(auth_user_id, channel_id, u_id):
    # Example for add someone in channel
    channel = Channel.find_by_id(channel_id)
    user = User.find_by_id(u_id)
    channel.join(user)
    return {}


def channel_details_v1(auth_user_id, channel_id):
    # Example for get channel details
    channel = Channel.find_by_id(channel_id)
    channel_info = channel.todict(
        {'name', 'is_public', 'owner_members', 'all_members'})
    return channel_info


def channel_messages_v1(auth_user_id, channel_id, start):
    # Wait for new methods provide in src.type
    return {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
        'start': 0,
        'end': 50,
    }


def channel_join_v1(auth_user_id, channel_id):
    # Example is same in channel_intive_v1
    return {}

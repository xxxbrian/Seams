from src.type import User, DM, Notification
from src.error import InputError, AccessError
from src.type import pickelsave


@pickelsave
def dm_create_v1(token, u_ids):
    auth_user = User.find_by_token(token)
    users_list = [User.find_by_id(u_id) for u_id in u_ids]
    users_list.append(auth_user)
    if auth_user is None:
        raise AccessError(description='Permission denied')
    if any(u is None for u in users_list):
        raise InputError(description='User not found')
    if len(users_list) != len(set(users_list)):
        raise InputError(description='Duplicate u_id')
    new_dm = DM(auth_user.u_id, [u.u_id for u in users_list])
    new_dm.add_to_store()
    for user in [User.find_by_id(u_id) for u_id in u_ids]:
        new_nf = Notification(
            new_dm, f'{auth_user.handle_str} added you to {new_dm.name}')
        user.add_notification(new_nf)
    return {'dm_id': new_dm.dm_id}


def dm_list_v1(token):
    user = User.find_by_token(token)
    if user is None:
        raise AccessError(description='Permission denied')
    dm_list = DM.get_all()
    info = []
    for dm in dm_list:
        if user in dm.members:
            info.append(dm.todict())
    return {
        'dms': info,
    }


@pickelsave
def dm_remove_v1(token, dm_id):
    user = User.find_by_token(token)
    dm = DM.find_by_id(dm_id)
    if user is None:
        raise AccessError(description='Permission denied')
    if dm is None:
        raise InputError(description='DM not found')
    if not dm.has_user(user):
        raise AccessError(description='Permission denied: Not member')
    if not user is dm.owner:
        raise AccessError(description='Permission denied: Not owner')
    dm.remove()
    return {}


def dm_details_v1(token, dm_id):
    user = User.find_by_token(token)
    dm = DM.find_by_id(dm_id)
    if user is None:
        raise AccessError(description='Permission denied')
    if dm is None:
        raise InputError(description='DM not found')
    if not dm.has_user(user):
        raise AccessError(description='Permission denied: Not member')
    print(dm.todict({'owner'}))
    return dm.todict({'name', 'members'})


@pickelsave
def dm_leave_v1(token, dm_id):
    user = User.find_by_token(token)
    dm = DM.find_by_id(dm_id)
    if user is None:
        raise AccessError(description='Permission denied')
    if dm is None:
        raise InputError(description='DM not found')
    if not dm.has_user(user):
        raise AccessError(description='Permission denied: Not member')
    dm.leave(user)
    return {}


def dm_messages_v1(token, dm_id, start):
    user = User.find_by_token(token)
    dm = DM.find_by_id(dm_id)
    if user is None:
        raise AccessError(description='Permission denied')
    if dm is None:
        raise InputError(description='DM not found')
    if not dm.has_user(user):
        raise AccessError(description='Permission denied: Not member')
    message_amount = len(dm.get_messages())
    if start > message_amount:
        raise InputError(description='Message not found')

    end = start + 50 if start + 50 <= message_amount else -1
    msg_list = [
        msg.todict(auth_user=user) for msg in dm.get_messages(start, end)
    ]
    return {
        'messages': msg_list,
        'start': start,
        'end': end,
    }

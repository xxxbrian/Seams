from src.type import User, DM, Message
from src.error import InputError, AccessError


def dm_create_v1(token, u_ids):
    user = User.find_by_token(token)
    input_users = [User.find_by_id(u_id) for u_id in u_ids]
    if user is None:
        raise AccessError(description='Permission denied')
    if all(users) is None:
        raise InputError(description='All user not found')
    users = [u for u in input_users if u is not None]
    if len(users) != len(set(users)):
        raise InputError(description='Duplicate u_id')
    new_dm = DM(user.u_id, [u.u_id for u in users])
    new_dm.add_to_store()
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
    for dm_user in dm.member:
        dm.leave(dm_user)
    return {}


def dm_details_v1(token, dm_id):
    return {}


def dm_leave_v1(token, dm_id):
    return {}


def dm_messages_v1(token, dm_id, start):
    return {}

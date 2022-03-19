from src.type import User
from src.error import AccessError, InputError


def admin_user_remove_v1(token, u_id):
    auth_user = User.find_by_token(token)
    user = User.find_by_id(u_id)
    if auth_user is None or auth_user.group_id != 0:
        raise AccessError(description='Permission denied')
    if user is None:
        raise InputError(description='User not found')
    allusers = User.find_all()
    global_owners = [u for u in allusers if u.group_id == 0]
    if user.group_id == 0 and len(global_owners) == 0:
        raise InputError(description='Unable to remove the last owner')
    user.del_account()
    return {}


def admin_userpermission_change_v1(token, u_id, permission_id):
    return {}

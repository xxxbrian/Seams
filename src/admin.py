from src.type import User
from src.error import AccessError, InputError


def admin_user_remove_v1(token, u_id):
    auth_user = User.find_by_token(token)
    user = User.find_by_id(u_id)
    if auth_user is None or not auth_user.is_admin():
        raise AccessError(description='Permission denied')
    if user is None:
        raise InputError(description='User not found')
    allusers = User.find_all()
    global_owners = [u for u in allusers if u.is_admin()]
    if user.is_admin() and len(global_owners) == 1:
        raise InputError(description='Unable to remove the last owner')
    user.del_account()
    return {}


def admin_userpermission_change_v1(token, u_id, permission_id):
    auth_user = User.find_by_token(token)
    user = User.find_by_id(u_id)
    if auth_user is None or auth_user.group_id != 0:
        raise AccessError(description='Permission denied')
    if user is None:
        raise InputError(description='User not found')
    if permission_id == 1:
        if user.is_admin():
            raise InputError(
                description=
                'User already has the permissions level of permission_id')
        user.group_id = 0
    elif permission_id == 2:
        if not user.is_admin():
            raise InputError(
                description=
                'User already has the permissions level of permission_id')
        if len([u for u in User.find_all() if u.is_admin()]) == 1:
            raise InputError(description='Unable to remove the last owner')
        user.group_id = 500
    else:
        raise InputError(description='Permission_id invalid')
    return {}

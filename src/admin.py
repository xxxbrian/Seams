from src.type import User
from src.error import AccessError, InputError
from src.type import pickelsave


@pickelsave
def admin_user_remove_v1(token, u_id):
    """Given a user by their u_id, remove them from the Seams.

    Args:
        token (string): token of auth user
        u_id (integer): u_id of target user

    Raises:
        AccessError: the authorised user is not a global owner
        InputError: u_id does not refer to a valid user
        InputError: u_id refers to a user who is the only global owner

    Returns:
        dictionary: {}
    """
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


@pickelsave
def admin_userpermission_change_v1(token, u_id, permission_id):
    """Given a user by their user ID, set their permissions to new permissions described by permission_id.

    Args:
        token (string): token of auth user
        u_id (integer): u_id of target user
        permission_id (integer): Owners (permission id 1), Members (permission id 2)

    Raises:
        AccessError: the authorised user is not a global owner
        InputError: u_id does not refer to a valid user
        InputError: u_id refers to a user who is the only global owner and they are being demoted to a user
        InputError: permission_id is invalid
        InputError: the user already has the permissions level of permission_id

    Returns:
        dictionary: {}
    """
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

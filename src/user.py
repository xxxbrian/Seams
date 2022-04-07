from src.type import User
from src.error import AccessError, InputError
from src.type import pickelsave


def users_all_v1(token):
    auth_user = User.find_by_token(token)
    if auth_user is None:
        raise AccessError(description='Permission denied')
    return {'users': [user.todict() for user in User.find_all()]}


def user_profile_v1(token, u_id):
    auth_user = User.find_by_token(token)
    if auth_user is None:
        raise AccessError(description='Permission denied')
    user = User.find_by_id(u_id, False)
    if user is None:
        raise InputError(description='User not exist')
    return {'user': user.todict()}


@pickelsave
def user_profile_setname_v1(token, name_first, name_last):
    user = User.find_by_token(token)
    if user is None:
        raise AccessError(description='Permission denied')
    if User.check_name_invalid(name_first):
        raise InputError(description='Name invalid')
    if User.check_name_invalid(name_last):
        raise InputError(description='Name invalid')
    user.name_first = name_first
    user.name_last = name_last
    return {}


@pickelsave
def user_profile_setemail_v1(token, email):
    user = User.find_by_token(token)
    if user is None:
        raise AccessError(description='Permission denied')
    if User.check_email_invalid(email):
        raise InputError(description='Email invalid')
    if User.check_email_been_used(email):
        raise InputError(description='Email has been used')
    user.email = email
    return {}


@pickelsave
def user_profile_sethandle_v1(token, handle_str):
    user = User.find_by_token(token)
    if user is None:
        raise AccessError(description='Permission denied')
    if User.check_handle_length_invalid(handle_str):
        raise InputError(description='Handle length invalid')
    if User.check_handle_content_invalid(handle_str):
        raise InputError(description='Handle character invalid')
    if User.check_handle_been_used(handle_str):
        raise InputError(description='Handle has been used')
    user.handle_str = handle_str
    return {}

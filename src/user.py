from src.type import User
from src.error import AccessError, InputError


def users_all_v1(token):
    auth_user = User.find_by_token(token)
    if auth_user is None:
        raise AccessError
    return {'users': [user.todict() for user in User.find_all()]}


def user_profile_v1(token, u_id):
    auth_user = User.find_by_token(token)
    if auth_user is None:
        raise AccessError
    user = User.find_by_id(u_id)
    if user is None:
        raise InputError
    return {'user': user.todict()}


def user_profile_setname_v1(token, name_first, name_last):
    user = User.find_by_token(token)
    if user is None:
        raise AccessError
    if User.check_name_invalid(name_first):
        raise InputError
    if User.check_name_invalid(name_last):
        raise InputError
    user.name_first = name_first
    user.name_last = name_last
    return {}


def user_profile_setemail_v1(token, email):
    user = User.find_by_token(token)
    if user is None:
        raise AccessError
    if User.check_email_invalid(email):
        raise InputError
    if User.check_email_been_used(email):
        raise InputError
    user.email = email
    return {}


def user_profile_sethandle_v1(token, handle_str):
    user = User.find_by_token(token)
    if user is None:
        raise AccessError
    if User.check_handle_length_invalid(handle_str):
        raise InputError
    if User.check_handle_content_invalid(handle_str):
        raise InputError
    if User.check_handle_been_used(handle_str):
        raise InputError
    user.handle_str = handle_str
    return {}

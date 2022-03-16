from src.type import User
from src.error import AccessError, InputError


def users_all_v1(token):
    user = User.find_by_token(token)
    if user is None:
        raise AccessError
    return {'users': [user.todict() for user in User.find_all()]}


def user_profile_v1(token, u_id):
    pass


def user_profile_setname_v1(token, name_first, name_last):
    pass


def user_profile_setemail_v1(token, email):
    pass


def user_profile_sethandle_v1(token, handle_str):
    pass

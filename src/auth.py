from ast import In
from src.data_store import data_store
from src.error import InputError
from src.type import User

def auth_login_v1(email, password):
    # email entered does not belong to a user
    if not User.check_email_been_used(email):
        raise InputError
    # password is not correct
    if not User.match_email_password(email,password):
        raise InputError
    user = User.find_by_email(email)
    return {
        'auth_user_id': user.u_id,
    }

def auth_register_v1(email, password, name_first, name_last):
    if User.check_email_invalid(email):
        raise InputError
    if User.check_email_been_used(email):
        raise InputError
    if User.check_password_invalid(password):
        raise InputError
    if User.check_name_invalid(name_first):
        raise InputError
    if User.check_name_invalid(name_last):
        raise InputError
    
    new_user = User(email, password, name_first, name_last)
    new_user.add_to_store()

    return {
        'auth_user_id': new_user.u_id,
    }

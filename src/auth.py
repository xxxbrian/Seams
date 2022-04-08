from src.error import AccessError, InputError
from src.type import User
from src.type import pickelsave
from flask_mail import Message as Flask_Message
from src.config import MAIL_USERNAME


@pickelsave
def auth_login_v2(email, password):
    """Given a registered user's email and password, returns their `auth_user_id` value and a new `token`.

    Args:
        email (string): email of login user
        password (string): password of login user
    
    Raises:
        InputError: email entered does not belong to a user
        InputError: password is not correct

    Returns:
        dictionary: { token, auth_user_id }
    """
    # email entered does not belong to a user
    if not User.check_email_been_used(email):
        raise InputError(description='Account not found')
    # password is not correct
    if not User.match_email_password(email, password):
        raise InputError(description='Incorrect password')
    user = User.find_by_email(email)
    token = user.generat_token()
    return {
        'token': token,
        'auth_user_id': user.u_id,
    }


@pickelsave
def auth_register_v2(email, password, name_first, name_last):
    """Given a user's first and last name, email address, and password, create a new account for them and return a new `auth_user_id` and `token`.

    Args:
        email (string):  email of login user
        password (string): password of login user
        name_first (string): first name of login user
        name_last (string): last name of login user

    Raises:
        InputError: email entered is not a valid email (more in section 6.4)
        InputError: email address is already being used by another user
        InputError: length of password is less than 6 characters
        InputError: length of name_first is not between 1 and 50 characters inclusive
        InputError: length of name_last is not between 1 and 50 characters inclusive

    Returns:
        dictionary: { token, auth_user_id }
    """
    if User.check_email_invalid(email):
        raise InputError(description='Email invalid')
    if User.check_email_been_used(email):
        raise InputError(description='Email has been used')
    if User.check_password_invalid(password):
        raise InputError(description='Password invalid')
    if User.check_name_invalid(name_first):
        raise InputError(description='Name invalid')
    if User.check_name_invalid(name_last):
        raise InputError(description='Name invalid')

    new_user = User(email, password, name_first, name_last)
    new_user.add_to_store()

    return auth_login_v2(email, password)


@pickelsave
def auth_logout_v1(token):
    """Given an active token, invalidates the token to log the user out.

    Args:
        token (string): token of logout user

    Raises:
        InputError: Token invalid

    Returns:
        dictionary: {}
    """
    user = User.find_by_token(token)
    if user is None:
        raise AccessError(description='Token invalid')
    User.remove_token(token)
    return {}


@pickelsave
def auth_passwordreset_request_v1(email, mailobj):
    user = User.find_by_email(email)
    if user is None:
        return {}
    code = user.generat_reset_code()
    msg = Flask_Message('UNSW-COMP1531',
                        sender=MAIL_USERNAME,
                        recipients=[email])
    msg.body = code
    mailobj.send(msg)
    return {}


@pickelsave
def auth_passwordreset_reset_v1(reset_code: str, new_password: str):
    user = User.find_by_reset_code(reset_code)
    if user is None:
        raise InputError(description='Reset_code invalid')
    if User.check_password_invalid(new_password):
        raise InputError(description='Password length invalid')
    user.password_set(new_password)
    user.remove_reset_code()
    return {}

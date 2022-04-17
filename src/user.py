from src.type import User, Seams
from src.error import AccessError, InputError
from src.type import pickelsave

import requests
from PIL import Image
from io import BytesIO
import secrets


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
    print(f'cov-{user.todict({})}')
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


@pickelsave
def user_profile_uploadphoto_v1(token, img_url, x_start, y_start, x_end,
                                y_end):
    user = User.find_by_token(token)
    if user is None:
        raise AccessError(description='Permission denied')
    if x_end <= x_start or y_end <= y_start:
        raise InputError(description='Invalid bounds')
    try:
        res = requests.get(img_url)
    except Exception as e:
        raise InputError(description=f'{e}') from InputError
    if res.status_code != 200:
        raise InputError(description='Invalid img_url')
    if not res.headers['Content-Type'] in ('image/jpeg', 'image/jpg'):
        raise InputError(description='Not JPG')
    img = Image.open(BytesIO(res.content))
    width, height = img.size
    if x_start < 0 or y_start < 0 or x_end > width or y_end > height:
        raise InputError(description='Bounds out of range')
    img_name = f'{secrets.token_urlsafe()}.jpg'
    new_img = img.crop((x_start, y_start, x_end, y_end))
    new_img.save(f'static/profile_img/{img_name}')
    user.set_profile_img(img_name)
    return {}


def user_stats_v1(token):
    user = User.find_by_token(token)
    if user is None:
        raise AccessError(description='Permission denied')
    return {'user_stats': user.get_analytics()}


def users_stats_v1(token):
    user = User.find_by_token(token)
    if user is None:
        raise AccessError(description='Permission denied')
    return {'workspace_stats': Seams.get_workspace_stats()}

import pytest

from src.channels import channels_create_v1
from src.auth import auth_register_v1
from src.error import InputError
from src.other import clear_v1

import random, string


@pytest.fixture
def clear():
    clear_v1


@pytest.fixture
def create_user():
    user_list = list()
    return user_list


def test_channels_create_name_too_short(clear, create_user):
    with pytest.raises(InputError):
        for user in create_user:
            channels_create_v1(user['auth_user_id'], '', True)


def test_channels_create_name_too_long(clear, create_user):
    name = random.sample(string.ascii_letters + string.digits, 21)
    with pytest.raises(InputError):
        for user in create_user:
            channels_create_v1(user['auth_user_id'], name, True)

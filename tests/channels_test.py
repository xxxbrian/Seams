import pytest

from src.channels import channels_create_v1
from src.auth import auth_register_v1
from src.error import InputError
from src.other import clear_v1

import random, string


@pytest.fixture
def clear():
    clear_v1

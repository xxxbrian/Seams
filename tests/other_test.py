import pytest

from src.error import InputError
from src.other import clear_v1
from src.auth import auth_register_v1, auth_login_v1
from src.channels import channels_create_v1, channels_listall_v1

def test_clear_v1():
    """adding user and channel and test if clear_v1 resets it"""
    user1 = auth_register_v1('tesla@space.com', 'Password',
                            'Elon', 'Musk')['auth_user_id']
    user2 = auth_register_v1('zuckerberg@meta.com', 'Password',
                            'Mark', 'Zuckerberg')['auth_user_id']
    channels_create_v1(user1, 'spaceX', True)
    channels_create_v1(user2, 'Meta', False)

    clear_v1()
    # test users clear
    with pytest.raises(InputError):
        auth_login_v1('tesla@space.com', 'Password')
    with pytest.raises(InputError):
        auth_login_v1('zuckerberg@meta.com', 'Password')

    # test channels clear
    user1 = auth_register_v1('tesla@space.com', 'Password', 'Elon',
                             'Musk')['auth_user_id']
    assert len(channels_listall_v1(user1)['channels']) == 0

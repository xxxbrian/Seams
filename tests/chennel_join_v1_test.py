import pytest

from src import data_store
from src.channel import channel_join_v1, channel_invite_v1
from src.channels import channels_create_v1, channels_list_v1
from src.auth import auth_register_v1, auth_login_v1
from src.error import InputError, AccessError
from src.other import clear_v1


def test_channels_list_after_join():
    clear_v1()

    user_list = list()
    user_list.append(
        auth_register_v1('elon.mask@spacex.com', 'Password', 'Elon', 'Musk'))
    user_list.append(
        auth_register_v1('mark.zuckerberg@meta.com', 'Password', 'Mark',
                         'Zuckerberg'))
    user_list.append(
        auth_register_v1('tim.cook@icloud.com', 'Password', 'Tim', 'Cook'))
    user_list.append(
        auth_register_v1('bill.gates@outlook.com', 'Password', 'Bill',
                         'Gates'))

    channels_create_v1(user_list[0]['auth_user_id'], 'channel1', True)
    channels_create_v1(user_list[0]['auth_user_id'], 'channel2', True)
    channels_create_v1(user_list[0]['auth_user_id'], 'channel3', True)
    channels_create_v1(user_list[0]['auth_user_id'], 'channel4', True)

    channels_create_v1(user_list[1]['auth_user_id'], 'channel5', True)
    channels_create_v1(user_list[1]['auth_user_id'], 'channel6', True)
    channels_create_v1(user_list[1]['auth_user_id'], 'channel7', True)
    channels_create_v1(user_list[1]['auth_user_id'], 'channel8', True)

    store = data_store.get()
    channels = store['channels']

    channel_join_v1(user_list[0]['auth_user_id'], 5)
    channel_join_v1(user_list[0]['auth_user_id'], 6)
    channel_join_v1(user_list[0]['auth_user_id'], 7)
    channel_join_v1(user_list[0]['auth_user_id'], 8)

    channels_dict1 = channels_list_v1(user_list[0]['auth_user_id'])
    channels_list1 = channels_dict1['channels']

    assert len(channels_list1) == 8

    for channel in channels_list1:
        exist = False
        for i in range(0, len(channels)):
            if channel['channel_id'] == channels[i]['channel_id'] and channel['name'] == channels[i]['name']:
                exist = True
        assert exist == True

def test_channel_join_v1():
    clear_v1()

    user_list = list()
    user_list.append(
        auth_register_v1('elon.mask@spacex.com', 'Password', 'Elon', 'Musk'))
    user_list.append(
        auth_register_v1('mark.zuckerberg@meta.com', 'Password', 'Mark',
                         'Zuckerberg'))
    user_list.append(
        auth_register_v1('tim.cook@icloud.com', 'Password', 'Tim', 'Cook'))
    user_list.append(
        auth_register_v1('bill.gates@outlook.com', 'Password', 'Bill',
                         'Gates'))
    channel1 = channels_create_v1(user_list[0]['auth_user_id'], "example_channel1", True)
    channel_invite_v1(user_list[0]['auth_user_id'], channel1['channel_id'], user_list[1]['auth_user_id'])
    ret_val = channel_join_v1(user_list[2]['auth_user_id'], channel1['channel_id'])
    assert ret_val == {}

def test_channel_join_v1_except():
    clear_v1()
    user_list = list()
    user_list.append(
        auth_register_v1('elon.mask@spacex.com', 'Password', 'Elon', 'Musk'))
    user_list.append(
        auth_register_v1('mark.zuckerberg@meta.com', 'Password', 'Mark',
                         'Zuckerberg'))
    user_list.append(
        auth_register_v1('tim.cook@icloud.com', 'Password', 'Tim', 'Cook'))
    user_list.append(
        auth_register_v1('bill.gates@outlook.com', 'Password', 'Bill',
                         'Gates'))
    no_exist1 = 200000
    no_exist2 = 200001
    channel1 = channels_create_v1(user_list[0]['auth_user_id'], "example_channel1", True)
    channel2 = channels_create_v1(user_list[0]['auth_user_id'], "example_channel2", False)
    channel_invite_v1(user_list[0]['auth_user_id'], channel1['channel_id'], user_list[1]['auth_user_id'])
    with pytest.raises(AccessError):
        channel_join_v1(no_exist1, channel1['channel_id'])
    with pytest.raises(InputError):
        assert channel_join_v1(user_list[2]['auth_user_id'], no_exist2)
    with pytest.raises(InputError):
        assert channel_join_v1(user_list[0]['auth_user_id'], channel1['channel_id'])
    with pytest.raises(AccessError):
        assert channel_join_v1(user_list[2]['auth_user_id'], channel2['channel_id'])
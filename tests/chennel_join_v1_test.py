import pytest

from src import data_store
from src.channel import channel_join_v1, channel_invite_v1
from src.channels import channels_create_v1, channels_list_v1
from src.auth import auth_register_v1, auth_login_v1
from src.error import InputError, AccessError
from src.other import clear_v1


def test_channels_list_after_join():
    clear_v1()  # Initialization

    # create users
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

    # create 8 channels
    channels_create_v1(user_list[0]['auth_user_id'], 'channel1', True)
    channels_create_v1(user_list[0]['auth_user_id'], 'channel2', True)
    channels_create_v1(user_list[0]['auth_user_id'], 'channel3', True)
    channels_create_v1(user_list[0]['auth_user_id'], 'channel4', True)

    channels_create_v1(user_list[1]['auth_user_id'], 'channel5', True)
    channels_create_v1(user_list[1]['auth_user_id'], 'channel6', True)
    channels_create_v1(user_list[1]['auth_user_id'], 'channel7', True)
    channels_create_v1(user_list[1]['auth_user_id'], 'channel8', True)

    # get all channels
    store = data_store.get()
    channels = store['channels']

    # connect to first user if the first 4 channels are not
    channel_join_v1(user_list[0]['auth_user_id'], 5)
    channel_join_v1(user_list[0]['auth_user_id'], 6)
    channel_join_v1(user_list[0]['auth_user_id'], 7)
    channel_join_v1(user_list[0]['auth_user_id'], 8)

    # get first user's channel 
    channels_dict1 = channels_list_v1(user_list[0]['auth_user_id'])
    channels_list1 = channels_dict1['channels']

    # test if 8 channels included 
    assert len(channels_list1) == 8

    for channel in channels_list1:
        exist = False
        for i in range(0, len(channels)):
            if channel['channel_id'] == channels[i]['channel_id'] and channel['name'] == channels[i]['name']:
                exist = True
        assert exist == True

def test_channel_join_v1():
    clear_v1()  # 

    # create users
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

    # create channel 
    channel1 = channels_create_v1(user_list[0]['auth_user_id'], "example_channel1", True)
    # invite second user
    channel_invite_v1(user_list[0]['auth_user_id'], channel1['channel_id'], user_list[1]['auth_user_id'])
    # connect to third user
    ret_val = channel_join_v1(user_list[2]['auth_user_id'], channel1['channel_id'])
    # return {}
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

    # no exist 2 IDs
    no_exist1 = 200000
    no_exist2 = 200001
    # create two channels
    channel1 = channels_create_v1(user_list[0]['auth_user_id'], "example_channel1", True)
    channel2 = channels_create_v1(user_list[0]['auth_user_id'], "example_channel2", False)
    # invite the first channel 
    channel_invite_v1(user_list[0]['auth_user_id'], channel1['channel_id'], user_list[1]['auth_user_id'])

    # connect to user if the user does not exist AccessError
    with pytest.raises(AccessError):
        channel_join_v1(no_exist1, channel1['channel_id'])
    # connect to channel if the channel does not exist InputError
    with pytest.raises(InputError):
        assert channel_join_v1(user_list[2]['auth_user_id'], no_exist2)
    # connect existed user InputError
    with pytest.raises(InputError):
        assert channel_join_v1(user_list[0]['auth_user_id'], channel1['channel_id'])
    # connect to private channel AccessError
    with pytest.raises(AccessError):
        assert channel_join_v1(user_list[2]['auth_user_id'], channel2['channel_id'])
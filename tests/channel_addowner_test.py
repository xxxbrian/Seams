import pytest
from src.auth import auth_register_v2, channels_create_v2
from src.channel import channel_addowner_v1
from src.error import InputError, AccessError
from src.other import clear_v1

# InputError: channel_id does not refer to 
# a valid channel
def test_invalid_channel():
    clear_v1()

    user_2 = auth_register_v2("z12352023@ad.unsw.edu.au",
                                "412123",  
                                "Wick", 
                                "John")['token']

    user_1 = auth_register_v2("weihouzeng@gmail.com", 
                                "ptr123",
                                "Peter", 
                                "Zeng")

    channel_id = channels_create_v2(user_1, False)

    with pytest.raises(InputError):
        channel_addowner_v1(user_1, channel_id['channel_id'] + 1, user_2)

# InputError: u_id does not refer to a valid user
def test_invalid_user_u_id():

    clear_v1()

    user_1 = auth_register_v2("weihouzeng@gmail.com", 
                                "ptr123",
                                "Peter", 
                                "Zeng")

    channel = channels_create_v2(user_1['token'], 'channelName', True)

    with pytest.raises(InputError):
        channel_addowner_v1(user_1['token'], channel['channel_id'], -42) 

# InputError: u_id refers to a user who is already an owner of the channel
def test_channel_addowner_already_owner():
    clear_v1()

    user_2 = auth_register_v2("z12352023@ad.unsw.edu.au",
                                "412123",  
                                "Wick", 
                                "John")['token']

    user_1 = auth_register_v2("weihouzeng@gmail.com", 
                                "ptr123",
                                "Peter", 
                                "Zeng")

    channel_id = channels_create_v2(user_1, 'dankmemechannel', False)

    channel_addowner_v1(user_1, channel_id['channel_id'], user_2['auth_user_id'])

    with pytest.raises(InputError):
        channel_addowner_v1(user_1, channel_id['channel_id'], user_2['auth_user_id']) 

# AccessError: channel_id is valid and the authorised user does not have owner permissions in the channel
def test_invalid_authorised_user():
    clear_v1()

    user_1 = auth_register_v2("z5374603@ad.unsw.edu.au",
                                "Ymc123",  
                                "Steve", 
                                "Yang")['token']

    user_2 = auth_register_v2("z5201314@ad.unsw.edu.au",
                                "Bojin123", 
                                "Bojin", 
                                "Li")['token']

    user_3 = auth_register_v2("weihouzeng@gmail.com", 
                                "ptr123",
                                "Peter", 
                                "Zeng")

    channelID = channels_create_v2(user_1, 'dankmemechannel', False)

    with pytest.raises(AccessError):
        channel_addowner_v1(user_2, channelID['channel_id'], user_3['auth_user_id'])
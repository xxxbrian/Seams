import pytest
from src.auth import auth_register_v2, channels_create_v2, channel_join_v2
from src.channel import channel_leave_v1
from src.error import InputError, AccessError
from src.other import clear_v1

# InputError: channel_id does not refer to a valid channel
def test_invalid_channel_id():
    clear_v1()

    user_1 = auth_register_v2("z12352023@ad.unsw.edu.au",
                                "412123",  
                                "Wick", 
                                "John")['token']

    user_2 = auth_register_v2("weihouzeng@gmail.com", 
                                "ptr123",
                                "Peter", 
                                "Zeng")

    c_id = channels_create_v2(user_1, True)

    channel_join_v2(user_2['token'], c_id['channel_id'])

    with pytest.raises(InputError):
        channel_leave_v1(user_2['token'], c_id['channel_id'] + 1)


#AccessError: channel_id is valid and the authorised user is not a member of the channel
def test_user_is_not_in_channel():
    clear_v1()

    user_1 = auth_register_v2("z12352023@ad.unsw.edu.au",
                                "412123",  
                                "Wick", 
                                "John")['token']

    user_2 = auth_register_v2("weihouzeng@gmail.com", 
                                "ptr123",
                                "Peter", 
                                "Zeng")

    c_id = channels_create_v2(user_1, True)

    with pytest.raises(AccessError):
        channel_leave_v1(user_2['token'], c_id['channel_id'])
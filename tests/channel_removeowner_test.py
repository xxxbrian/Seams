import pytest
from src.auth import auth_register_v2, channels_create_v2, channel_join_v2
from src.channel import channel_removeowner_v1, channel_addowner_v1
from src.error import InputError, AccessError
from src.other import clear_v1

# InputError: channel_id does not refer to a valid channel
def test__invalid_channel_id():
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

    channel_addowner_v1(user_1, c_id['channel_id'], user_2['auth_user_id'])

    with pytest.raises(InputError):
        channel_removeowner_v1(user_1, c_id['channel_id'] + 1, user_2['auth_user_id'])

# InputError: u_id does not refer to a valid user
def test_invalid_user():
    clear_v1()
    user_1 = auth_register_v2("z12352023@ad.unsw.edu.au",
                                "412123",  
                                "Wick", 
                                "John")['token']

    user_2 = auth_register_v2("weihouzeng@gmail.com", 
                                "ptr123",
                                "Peter", 
                                "Zeng")
    
    user_3 = auth_register_v2("z5201314@ad.unsw.edu.au",
                                "Bojin123", 
                                "Bojin", 
                                "Li")

    c_id = channels_create_v2(user_1, False)

    channel_addowner_v1(user_1, c_id['channel_id'], user_2['auth_user_id'])

    with pytest.raises(InputError):
        channel_removeowner_v1(user_1, c_id['channel_id'], user_3['auth_user_id'])

# InputError: u_id refers to a user who is currently the only owner of the channel
def test_unique_owner():
    clear_v1()

    user_1 = auth_register_v2("weihouzeng@gmail.com", 
                                "ptr123",
                                "Peter", 
                                "Zeng")

    c_id = channels_create_v2(user_1['token'], False)

    with pytest.raises(InputError):
        channel_removeowner_v1(user_1['token'], c_id['channel_id'], user_1['auth_user_id'])

# InputError: u_id refers to a user who is not an owner of the channel
def test_uid_is_not_from_owner():
    clear_v1()
    user_1 = auth_register_v2("z12352023@ad.unsw.edu.au",
                                "412123",  
                                "Wick", 
                                "John")['token']

    user_2 = auth_register_v2("z5374603@ad.unsw.edu.au",
                                "Ymc123",  
                                "Steve", 
                                "Yang")
    
    user_3 = auth_register_v2("z5201314@ad.unsw.edu.au",
                                "Bojin123", 
                                "Bojin", 
                                "Li")

    c_id = channels_create_v2(user_1, False)

    channel_addowner_v1(user_1, c_id['channel_id'], user_2['auth_user_id'])

    with pytest.raises(InputError):
        channel_removeowner_v1(user_1, c_id['channel_id'], user_3['auth_user_id'])

# AccessError: channel_id is valid and the authorised user does not have owner permissions in the channel
def test_channel_removeowner_invalid_remover():
    '''
    Tests channel_removeowner_v1 where the person removing someone else as owner is not an owner
    '''
    clear_v1()

    user_1 = auth_register_v2("z12352023@ad.unsw.edu.au",
                                "412123",  
                                "Wick", 
                                "John")['token']

    user_2 = auth_register_v2("z5374603@ad.unsw.edu.au",
                                "Ymc123",  
                                "Steve", 
                                "Yang")
    
    user_3 = auth_register_v2("z5201314@ad.unsw.edu.au",
                                "Bojin123", 
                                "Bojin", 
                                "Li")

    c_id = channels_create_v2(user_1, False)

    channel_addowner_v1(user_1, c_id['channel_id'], user_3['auth_user_id'])
    
    with pytest.raises(AccessError):
        channel_removeowner_v1(user_2['token'], c_id['channel_id'], user_3['auth_user_id'])
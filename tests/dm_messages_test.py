import pytest
from src.error import InputError, AccessError
from src.auth import auth_register_v1
from src.other import clear_v1
from src.dm import dm_create_v1, dm_messages_v1
# InputError: dm_id does not refer to a valid DM
def test_dm_messages_invalid_dm_id():
    clear_v1()
    
    user_1 = auth_register_v1("z5374603@ad.unsw.edu.au",
                                "Ymc123",  
                                "Steve", 
                                "Yang")

    user_2 = auth_register_v1("z5201314@ad.unsw.edu.au",
                                "Bojin123", 
                                "Bojin", 
                                "Li")

    dm_create_v1(user_1['token'], [user_2['auth_user_id']])

    with pytest.raises(InputError):
        assert dm_messages_v1(user_1['token'], -1, 0)

# InputError: start is greater than the total number of messages in the channel
def test_dm_messages_invalid_start():
    clear_v1()

    user_1 = auth_register_v1("z5374603@ad.unsw.edu.au",
                                "Ymc123",  
                                "Steve", 
                                "Yang")

    
    user_2 = auth_register_v1("z5201314@ad.unsw.edu.au",
                                "Bojin123", 
                                "Bojin", 
                                "Li")

    dm_messages = dm_create_v1(user_1['token'], [user_2['auth_user_id']])

    with pytest.raises(AccessError):
        assert dm_messages_v1(user_1['token'], dm_messages['dm_id'], 50)

# AccessError: start is greater than 
# the total number of messages in the channel
def test_dm_messages_unauthorised_user():
    clear_v1()

    user_1 = auth_register_v1("z5374603@ad.unsw.edu.au",
                                "Ymc123",  
                                "Steve", 
                                "Yang")

    user_2 = auth_register_v1("z5201314@ad.unsw.edu.au",
                                "Bojin123", 
                                "Bojin", 
                                "Li")

    user_3 = auth_register_v1("weihouzeng@gmail.com", 
                                "ptr123",
                                "Peter", 
                                "Zeng")

    dm_messages = dm_create_v1(user_1['token'], [user_2['auth_user_id']])

    with pytest.raises(AccessError):
        assert dm_messages_v1(user_3['token'], dm_messages['dm_id'], 0)
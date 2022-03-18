import pytest
from src.error import InputError, AccessError
from src.auth import auth_register_v1
from src.other import clear_v1
from src.dm import dm_create_v1


# AccessError: dm_id is valid and the authorised 
# user is not a member of the DM
def test_invalid_token():
    clear_v1()

    user_1 = auth_register_v1("weihouzeng@gmail.com", 
                                "ptr123",
                                "Peter", 
                                "Zeng")

    u_id_1 = user_1['auth_user_id']

    dm_leave = dm_create_v1(user_1['token'], [u_id_1])

    with pytest.raises(AccessError):
        assert dm_create_v1(user_1['token'], dm_leave['dm_id'])


# InputError: dm_id does not refer to a valid DM
def test_ivalid_dm_id():
    clear_v1()

    user_1 = auth_register_v1("z5374603@ad.unsw.edu.au",
                                "Ymc123",  
                                "Steve", 
                                "Yang")

    with pytest.raises(InputError):
        assert dm_create_v1(user_1['token'], 1)


    
    
                                
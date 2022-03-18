import pytest
from src.error import InputError, AccessError
from src.auth import auth_register_v1
from src.other import clear_v1
from src.dm import dm_create_v1, dm_details_v1

# InputError: dm_id does not refer to a valid DM
def test_invalid_dm_id():

    clear_v1()

    user_1 = auth_register_v1("weihouzeng@gmail.com", 
                                "ptr123",
                                "Peter", 
                                "Zeng")

    with pytest.raises(InputError):
        assert dm_details_v1(user_1['token'], 1)

# AccessError: dm_id is valid and the authorised user 
# is not a member of the DM
def test_invalid_token():

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
    user_4 = auth_register_v1("12345678@qq.com", 
                                "Cicy123",
                                "Cicy", 
                                "Zhou")

    u_id_1 = user_1['auth_user_id']
    u_id_2 = user_4['auth_user_id']

    dm_details = dm_create_v1(user_2['token'], 
                        [u_id_1, u_id_2])
    
    with pytest.raises(AccessError):
        assert dm_details_v1(user_3['token'], dm_details['dm_id'])
    
        

    
    
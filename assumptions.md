# Test assumptions:
# 1. test_auth_login:
    We assume auth_register_v1 and clear_v1 are working well. Because we nned to regiser some users at first so that we have users in our data base. We run auth_register_v1 as set up program. And we need to clear everything when we finish a test.

# 2. channel_invite_v1_test:
    We assume auth_register_v1, clear_v1 and channels_creat_v1 are working well. Because we have to register some users to creat channels first. And we need to clear everything when we finish a test.
    And in some of these tests, we assume auth_login_v1 is working well. Because we wanna these users' u_id, we login them at first.

# 3. channel_join_v1_test:
    We assume auth_register_v1, auth_login_v1, clear_v1 and channels_creat_v1 are working well. We need some users to creat channels first for our tests. And we need to clear everything when we finish a test. In some tests, we assume channel_invite_v1 is working well. Because we want to test the situation when users are already in a channel. We use channel_invite_v1 to let them in.

# 4. channel_details_v1_test:
    We assume auth_register_v1, auth_login_v1, clear_v1 and channels_creat_v1 are working well. The reasons are all the same as above. 
    P.S. we think we can also test whether channel_join_v1 and channel_invite_v1 are working or not. Because we need to check a channel's details with one or two users who are invited or joined in this channel. At the same time, by the changes of channel's details, we can test both invite and join programs.
    
# 5. channels_test:
    We assume auth_register_v1 amd clear_v1 are both working well. Because we need to have some users at first. So that we can let these users creat channels.

# 6. handle_test:
    About handle test, because we can't return handle in any function, we decide to test it in channel_details_v1_test. We can check if handles are right when we check all informations in a channel. And we do test the situation that 2 users names are the same.

# 7. auth_logout_test:
    We assume channels_listall is working well in this test. Because we need to test the logout token is invalid. We use channels_listall and assert there will be 
    an AccessError when we input a logout_user's token.
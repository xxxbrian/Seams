# Users 

# 1. auth/login/v2:
   **Parameters:{email, password}**

   **Return Type:{token, auth_user_id}**

   password must be correct 

   email is **unique**
   
   User token: a string encoding the user's authorization using the hash function 256


# 2. auth/register/v2:
   **Parameters:{email, password, name_first, name_last}**

   **Return Type:{token, auth_user_id}**

   length of password is more than **6 characters**

   A valid email should match the following regular expression: **'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'**

   Email is **unique** and not yet used by others

   Both the name_first and name_last name length ranges from **1 to 50 characters inclusive**.

   Handle: **first name and last name in lowercase**

        The concatenation is **20 characters or less**
        
        if the handle "'abcdefghijklmnopqrst' is already taken, Then the handle 'abcdefghijklmnopqrst0' is allowed

# 3. user/profile/v1:
   **Parameters:{token, u_id}**

   **Return Type:{user}**

   u_id should match a vaild user 

# 4. user/profile/setname/v1:
   **Parameters:{token, name_first, name_last}**

   **Return Type:{}**

   The lengths of name_first and name_last should be between 1 and 50 characters inclusive

# 5. user/profile/setemail/v1:
   **Parameters:{token, email}**

   **Return Type:{}**

   email entered should be a vaild email, which match the following regular expression: **'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'**

   Email is **unique** and not yet used by others

# 6. user/profile/sethandle/v1:
   **Parameters:{token, handle_str}**

   **Return Type:{}**

   The length of handle_str should be in range from 3 to 20 characters inclusive

   handle_str contains characters that are alphanumeric

   Handle has not been used by others

# 7. auth/passwordreset/reset/v1:
   **Parameters:{reset_code, new_password}**

   **Return Type:{}**

   Reset_code is a vaild reset code

   The length of password entered should be greater than 6 characters long

# 8. user/profile/uploadphoto/v1:
   **Parameters:{token, img_url, x_start, y_start, x_end, y_end}**

   **Return Type:{}**

   Raise inputError when: 
    "img_url returns an HTTP status other than 200, or any other errors occur when attempting to retrieve the image"
    "any of x_start, y_start, x_end, y_end are not within the dimensions of the image at the URL"
    "x_end is less than or equal to x_start or y_end is less than or equal to y_start"
    "image uploaded is not a JPG"




# Channels
  channel_id is created from 0, and each channel_id is unique

  channel_id will not be deleted and will not be used more than once

# 1. channels/create/v2:
   **Parameters:{token, name, is_public}**

   **Return Type:{channel_id}**

   channel_id: Created with the given name either public or private and added when the user creates

   The length of a name should be between **1 and 20 characters**

   
# 2. channel/details/v2:
   **Parameters:{token, channel_id}**

   **Return Type:{name, is_public, owner_members, all_members}**

   Raise inputError when: 
    "The channel_id does not match a valid channel"

   Raise AccessError when:
    "channel_id is valid and the authorised user does not belong to the channel"

    
# 3. channel/join/v2:
   **Parameters:{token, channel_id}**

   **Return Type:{}**

   Raise inputError when: 
    "The channel_id does not match a valid channel"
    "The authorized user is already yet a member of the channel"

   Raise AccessError when:
    "Channel_id refers to a private channel for which the authorised user is not already a member or global owner"


# 4. channel/invite/v2:
   **Parameters:{token, channel_id, u_id}**

   **Return Type:{}**
   
   Raise inputError when: 
    "The channel_id does not match a valid channel"
    "u_id does not match a valid user"
    "u_id refers to a user who is not yet a member of the channel"

   Raise AccessError when:
    "The channel_id is valid and the authorised user does not belong to the channel"


# 5. channel/messages/v2:
   **Parameters:{token, channel_id, start}**

   **Return Type:{messages, start, end}**

   Raise inputError when: 
    "The channel_id does not match a valid channel"
    "Start with greater than the total number of messages in the channel"

   Raise AccessError when:
    "The channel_id is valid and the authorised user does not belong to the channel"

# 6. channel/leave/v1:
   **Parameters:{token, channel_id}**

   **Return Type:{}**

   Members of the channel who have been authorized are deleted. The channel should retain their information. If the unique channel owner leaves, the channel will remain.

   Raise inputError when: 
    "The channel_id does not match a valid channel"
    "A channel activity is initiated by the authorized user"

   Raise AccessError when:
    "The channel_id is valid and the authorised user does not belong to the channel"

# 7. channel/addowner/v1:
   **Parameters:{token, channel_id, u_id}**

   **Return Type:{}**

   The user with ID u_id will become the channel owner

   Raise inputError when: 
    "The channel_id does not match a valid channel"
    "u_id does not match a valid user"
    "u_id refers to a user who is not a member of the channel"
    "u_id refers to a user who is already an owner of the channel"

   Raise AccessError when:
    "The channel_id is valid and the authorised user does not belong to the channel"    

# 8. channel/removeowner/v1:
   **Parameters:{token, channel_id, u_id}**

   **Return Type:{}**

   The channel owner can remove himself in case he is not the only channel owner

   Raise inputError when: 
    "The channel_id does not match a valid channel"
    "u_id does not match a valid user"
    "u_id refers to a user who is not a member of owning the channel"
    "u_id refers to a user who is the sole owner of the channel"
    
   Raise AccessError when:
    "The channel_id is valid and the authorised user does not have owner permissions in the channel"   


# Messages

# 1. message/send/v1:
   **Parameters:{token, channel_id, message}**

   **Return Type:{message_id}**

   Each message has its unique ID, even if it is in a different channel.

   Raise inputError when: 
    "The channel_id does not match a valid channel"
    "length of message is less than 1 or over 1000 characters"
    
   Raise AccessError when:
    "The channel_id is valid and the authorised user does not belong to the channel"   

# 2. message/edit/v1:
   **Parameters:{token, message_id, message}**

   **Return Type:{}**

   Empty messages will not be edited, shared messages and stand-up messages will be edited as normal messages


# 3. message/remove/v1:
   **Parameters:{token, message_id}**

   **Return Type:{}**

   deleted messages does not remove the messages that forwarded the particular message

# 4. message/share/v1:
   **Parameters:{token, og_message_id, message, channel_id, dm_id}**

   **Return Type:{shared_message_id }**

   Once a message is shared, the specific information of the shared message will be displayed and notified.
   

# 5. message/react/v1:
   **Parameters:{token, message_id, react_id}**

   **Return Type:{}**

   reacting twice is unreact

# 6. message/unreact/v1:
   **Parameters:{token, message_id, react_id}**

   **Return Type:{}**

   unreacting can only happen when the user has reacted previously
   
# 7. message/pin/v1:
   **Parameters:{token, message_id}**

   **Return Type:{}**

   The first pinned message stays at the front of pinned message, it follows a chronological order.

# 8. message/unpin/v1:
   **Parameters:{token, message_id}**

   **Return Type:{}**

   Unpin can happen from message selection and pinned messages selection.

# 9. message/sendlater/v1:
   **Parameters:{token, channel_id, message, time_sent}**

   **Return Type:{message_id}**

   - Setting the time to the current minute of sending message is valid.
   - Muliple send later messages can be sent while the previous send later messages isn't sent yet.

# 10. message/sendlaterdm/v1:
   **Parameters:{token, dm_id, message, time_sent}**

   **Return Type:{message_id}**

   - Setting the time to the current minute of sending message is valid.
   - Muliple send later messages can be sent while the previous send later messages isn't sent yet.

# DM

# 1. dm/create/v1:
   **Parameters:{token, u_ids}**

   **Return Type:{dm_id}**

   DM is created by the user and contains the user u_id specified by the creator.The name is a list sorted alphabetically by user handles like **'ahandle1, bhandle2, chandle3'**

   any u_id in u_ids should be match a vaild user 

   There is no duplicate 'u_id' in u_ids.

# 2. dm/remove/v1:
   **Parameters:{token, dm_id}**

   **Return Type:{}**

   The DM creator can delete the DMs they created, and at the same time, all users are kicked out.


# 3. dm/details/v1:
   **Parameters:{token, dm_id}**

   **Return Type:{ name, members }**

   The DM creator can delete the DMs they created, and at the same time, all users are kicked out.
    
# 4. dm/leave/v1:
   **Parameters:{token, dm_id}**

   **Return Type:{ name, members }**

   When all users in the DM leave, the DM does not disappear and does not change in any way.

# Admin

# 1. admin/user/remove/v1:
   **Parameters:{token, u_id}**

   **Return Type:{}**

    After the user is deleted, the name displayed in messages are "Removed user". All information is reset and the name and handle can be reused.


# 2. admin/userpermission/change/v1:
   **Parameters:{token, u_id,permission_id}**

   **Return Type:{}**

   Permission owners can transfer their permissions to others unless there is only one owner

# Others
# 1. clear/v1:
   **Parameters:{}**

   **Return Type:{}**

   Clear all internal information to return it to the initialized state



# 2. search/v1:
   **Parameters:{token, query_str}**

   **Return Type:{messages}**

   The set of all messages will be displayed in unpredictable order
   
   The length of query_str should be ranged from 1 to 1000 characters inclusive
    
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


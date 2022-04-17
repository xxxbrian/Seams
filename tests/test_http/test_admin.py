import pytest
import requests
import random
from src.config import url
from src.error import InputError, AccessError

@pytest.fixture(name = 'user_list')
def create_user_list():
    '''
    This function is to pre-register 4 users for further tests
    
    returns:
    user_list (dictionary), contains 4 pre-register users' information
    '''
    requests.delete(f"{url}clear/v1", json = {})    # clear all info in server
    user_list = []
    user_list.append(requests.post(f"{url}auth/register/v2",
                                   json = { 'email': 'z5374603@unsw.com',
                                            'password': '123456',
                                            'name_first': 'Steve',
                                            'name_last': 'Yang'}))
    user_list.append(requests.post(f"{url}auth/register/v2",
                                   json = { 'email': 'z5374602@unsw.com',
                                            'password': '123456',
                                            'name_first': 'Brian',
                                            'name_last': 'Lee'}))
    user_list.append(requests.post(f"{url}auth/register/v2",
                                   json = { 'email': 'z5374601@unsw.com',
                                            'password': '123456',
                                            'name_first': 'Bojin',
                                            'name_last': 'Li'}))
    user_list.append(requests.post(f"{url}auth/register/v2",
                                   json = {  'email': 'z5374600@unsw.com',
                                            'password': '123456',
                                            'name_first':'Cicy',
                                            'name_last': 'Zhou'}))
    return user_list

@pytest.fixture(name = 'login_list')
def login_users():
    '''
    
    This function is to pre-login 4 users for further tests
    
    returns:
        login_list, contains 4 pre-register users' information
        
    '''
    login_list = []
    login_list.append(requests.post(url + "auth/login/v2",
                                    json = {"email": "z5374603@unsw.com",
                                            "password": "123456"}).json())
    login_list.append(requests.post(url + "auth/login/v2",
                                    json = {"email": "z5374602@unsw.com",
                                            "password": "123456"}).json())
    login_list.append(requests.post(url + "auth/login/v2",
                                    json = {"email": "z5374601@unsw.com",
                                            "password": "123456"}).json())
    login_list.append(requests.post(url + "auth/login/v2",
                                    json = {"email": "z5374600@unsw.com",
                                            "password": "123456"}).json())
    return login_list

@pytest.fixture(name = 'channel_list')
def channel_create(login_list):
    '''
    This function is to pre-create 4 channels for further tests
    
    Steve and Brian's channels are public channels. Bojin and Cicy's channels are private channels
    
    returns:
        channel_list, contains 4 channels' channel_id
    '''
    channel_list = []
    channel_list.append(requests.post(url + 'channels/create/v2',
                                      json = {'token': login_list[0]['token'],
                                              'name': "Steve's channel",
                                              'is_public': True}).json())
    channel_list.append(requests.post(url + 'channels/create/v2',
                                      json = {'token': login_list[1]['token'],
                                              'name': "Brian's channel",
                                              'is_public': True}).json())
    channel_list.append(requests.post(url + 'channels/create/v2',
                                      json = {'token': login_list[2]['token'],
                                              'name': "Bojin's channel",
                                              'is_public': True}).json())
    channel_list.append(requests.post(url + 'channels/create/v2',
                                      json = {'token': login_list[3]['token'],
                                              'name': "Cicy's channel",
                                              'is_public': False}).json())
    return channel_list

@pytest.fixture(name = 'dm_list')
def create_dm(login_list):
    '''
    This function is to pre-create some dms for further tests
    
    Return:
        dm_list, contain dm_id and name
    '''
    dm_list = []
    # dm_list[0]: user[0], user[1], user[2]
    dm_list.append(requests.post(url + "dm/create/v1",
                                 json = {'token': login_list[0]['token'],
                                         'u_ids': [login_list[1]['auth_user_id'], 
                                                   login_list[2]['auth_user_id']]}).json())
    
    # dm_list[1]: user[0], user[2]. user[3]
    dm_list.append(requests.post(url + "dm/create/v1",
                                 json = {'token': login_list[0]['token'],
                                         'u_ids': [login_list[3]['auth_user_id'], 
                                                   login_list[2]['auth_user_id']]}).json())
    
    # dm_list[2]: user[1], user[2]. user[3]
    dm_list.append(requests.post(url + "dm/create/v1",
                                 json = {'token': login_list[1]['token'],
                                         'u_ids': [login_list[2]['auth_user_id'], 
                                                   login_list[3]['auth_user_id']]}).json())
    return dm_list

######################################## Test_admin/user/remove/v1 ########################################

def test_admin_user_remove_normal(user_list, login_list, channel_list, dm_list):
    '''
    
    This test is to test when a user be removed successfully from seams
    
    Assumption:
        channel/join/v2 is working well
        channel/details/v2 is working well
        dm/details/v1 is working well
        users/all is working well
        dm/messages/v1 is working well
        channel/messages/v2 is working well
        user/profile/v1 is working well
        auth/register/v2 is working well
    '''
    # We will remove user[1] in this test #
    users = [
        {
            'u_id': login_list[0]['auth_user_id'],
            'email': 'z5374603@unsw.com',
            'name_first': 'Steve',
            'name_last': 'Yang',
            'handle_str': 'steveyang'
        },
        {
            'u_id': login_list[2]['auth_user_id'],
            'email': 'z5374601@unsw.com',
            'name_first': 'Bojin',
            'name_last': 'Li',
            'handle_str': 'bojinli'
        },
        {
            'u_id': login_list[3]['auth_user_id'],
            'email': 'z5374600@unsw.com',
            'name_first':'Cicy',
            'name_last': 'Zhou',
            'handle_str': 'cicyzhou'
        }
    ]
    removed_user = {
            'u_id': login_list[1]['auth_user_id'],
            'email': 'z5374602@unsw.com',
            'name_first': 'Removed',
            'name_last': 'user',
            'handle_str': 'brianlee'
        }
    # user[0] joins channel[1]
    requests.post(url + 'channel/join/v2',
                  json = {'token': login_list[0]['token'],
                          'channel_id': channel_list[1]['channel_id']})
    # user[0] becomse a owner of channel[1]
    requests.post(url + "channel/addowner/v1",
                  json = {'token': login_list[1]['token'],
                          'channel_id': channel_list[1]['channel_id'],
                          'u_id': login_list[0]['auth_user_id']})
    # user[1] send a message in channel[1]
    requests.post(url + 'message/send/v1',
                  json = {'token': login_list[1]['token'],
                          'channel_id': channel_list[1]['channel_id'],
                          'message': 'Hello world!'}).json()
     # user[1] send a message in dm[0]]
    requests.post(url + 'message/senddm/v1',
                  json = {'token': login_list[1]['token'],
                          'dm_id': dm_list[0]['dm_id'],
                          'message': 'Hi hi'})
    ## remove user[1] ##
    requests.delete(url + 'admin/user/remove/v1',
                    json = {'token': login_list[0]['token'],
                            'u_id': login_list[1]['auth_user_id']})
    
    response_1 = requests.get(url + 'channel/details/v2',
                              params = {'token': login_list[0]['token'],
                                        'channel_id': channel_list[1]['channel_id']}).json()
    response_2 = requests.get(url + 'dm/details/v1',
                              params = {'token': login_list[0]['token'],
                                        'dm_id': dm_list[0]['dm_id']}).json()
    response_3 = requests.get(url + "users/all/v1", 
                              params = {'token': login_list[0]['token']}).json()
    response_4 = requests.get(url + 'channel/messages/v2',
                              params = {'token': login_list[0]['token'],
                                        'channel_id': channel_list[1]['channel_id'],
                                        'start': 0}).json()
    response_5 = requests.get(url + 'dm/messages/v1',
                              params = {'token': login_list[0]['token'],
                                        'dm_id': dm_list[0]['dm_id'],
                                        'start': 0}).json()
    response_6 = requests.get(url + "user/profile/v1", 
                              params = {'token': login_list[0]['token'],
                                        'u_id': login_list[1]['auth_user_id']}).json()
    response_7 = requests.post(f"{url}auth/register/v2",
                                 json = { 'email': 'z5374602@unsw.com',
                                          'password': '123456',
                                          'name_first': 'Brian',
                                          'name_last': 'Lee'})
    response_8 = requests.get(url + "user/profile/v1", 
                              params = {'token': login_list[0]['token'],
                                        'u_id': response_7.json()['auth_user_id']}).json()
    response_9 = requests.post(url + 'auth/logout/v1',
                               json={'token': login_list[1]['token']})
    
    assert response_1['name'] == "Brian's channel"
    assert response_1['is_public'] == True
    assert response_1['owner_members'][0]['u_id'] == login_list[0]['auth_user_id']
    assert response_1['owner_members'][0]['email'] == "z5374603@unsw.com"
    assert response_1['owner_members'][0]['name_first'] == 'Steve'
    assert response_1['owner_members'][0]['name_last'] == 'Yang'
    assert response_1['owner_members'][0]['handle_str'] == 'steveyang'
    assert response_1['all_members'][0]['u_id'] == login_list[0]['auth_user_id']
    assert response_1['all_members'][0]['email'] == "z5374603@unsw.com"
    assert response_1['all_members'][0]['name_first'] == 'Steve'
    assert response_1['all_members'][0]['name_last'] == 'Yang'
    assert response_1['all_members'][0]['handle_str'] == 'steveyang'
    
    dm_0 = 'bojinli, brianlee, steveyang'
    assert response_2['name'] == dm_0
    assert response_2['members'][0]['u_id'] == login_list[2]['auth_user_id']
    assert response_2['members'][0]['email'] == "z5374601@unsw.com"
    assert response_2['members'][0]['name_first'] == 'Bojin'
    assert response_2['members'][0]['name_last'] == 'Li'
    assert response_2['members'][0]['handle_str'] == 'bojinli'
    assert response_2['members'][1]['u_id'] == login_list[0]['auth_user_id']
    assert response_2['members'][1]['email'] == "z5374603@unsw.com"
    assert response_2['members'][1]['name_first'] == 'Steve'
    assert response_2['members'][1]['name_last'] == 'Yang'
    assert response_2['members'][1]['handle_str'] == 'steveyang'
    
    # assert user[1] is not in users all
    for i in range(3):
        assert users[i]['u_id'] == response_3['users'][i]['u_id']
        assert users[i]['email'] == response_3['users'][i]['email']
        assert users[i]['name_first'] == response_3['users'][i]['name_first']
        assert users[i]['name_last'] == response_3['users'][i]['name_last']
        assert users[i]['handle_str'] == response_3['users'][i]['handle_str']
    assert response_4['messages'][0]['message'] == 'Removed user'
    assert response_5['messages'][0]['message'] == 'Removed user'
    assert removed_user['u_id'] == response_6['user']['u_id']
    assert removed_user['email'] == response_6['user']['email']
    assert removed_user['name_first'] == response_6['user']['name_first']
    assert removed_user['name_last'] == response_6['user']['name_last']
    assert removed_user['handle_str'] == response_6['user']['handle_str']
    assert response_7.status_code == 200
    
    assert response_8['user']['u_id'] == response_7.json()['auth_user_id']
    assert response_8['user']['email'] == 'z5374602@unsw.com'
    assert response_8['user']['name_first'] == 'Brian'
    assert response_8['user']['name_last'] == 'Lee'
    assert response_8['user']['handle_str'] == 'brianlee'
    assert response_9.status_code == AccessError.code
    
def test_admin_user_remove_invalid_u_id(user_list, login_list):
    '''
    
    This test is to test when u_id does not refer to a valid user
    
    Raises:
        InputError
        
    '''
    new_id = random.randint(-65535, 65535)
    invalid_u_id = []
    while len(invalid_u_id) < 1:
        if not new_id in [login_list[i]['auth_user_id'] for i in range(0,4)]:
            invalid_u_id.append(new_id)
    
    response_1  = requests.delete(url + 'admin/user/remove/v1',
                                  json = {'token': login_list[0]['token'],
                                          'u_id': invalid_u_id})
    assert response_1.status_code == InputError.code
    
def test_admin_user_remove_global_owner_u_id(user_list, login_list):
    '''
    
    This test is to test when u_id refers to a user who is the only global owner
    
    Raises:
        InputError
        
    '''
    response_1  = requests.delete(url + 'admin/user/remove/v1',
                                  json = {'token': login_list[0]['token'],
                                          'u_id': login_list[0]['auth_user_id']})
    assert response_1.status_code == InputError.code
    
def test_admin_user_remove_not_global_owner(user_list, login_list):
    '''
    
    This test is to test when the authorised user is not a global owner
    
    Raises:
        AccessError
        
    '''
    response_1  = requests.delete(url + 'admin/user/remove/v1',
                                  json = {'token': login_list[1]['token'],
                                          'u_id': login_list[2]['auth_user_id']})
    assert response_1.status_code == AccessError.code
    
######################################## Test_admin/userpermission/change/v1 ########################################

def test_admin_userpermission_change_to_1(user_list, login_list, channel_list):
    '''
    
    This test is to test change user's permission to 1 successfully
    
    '''
    # set user[1] as an owner
    requests.post(url + 'admin/userpermission/change/v1',
                  json = {'token': login_list[0]['token'],
                          'u_id': login_list[1]['auth_user_id'],
                          'permission_id': 1})
    # user[1] should able to remove user[3]
    response_1  = requests.delete(url + 'admin/user/remove/v1',
                                  json = {'token': login_list[1]['token'],
                                          'u_id': login_list[3]['auth_user_id']})
    # user[1] join channel[2]
    requests.post(f"{url}channel/join/v2",
                    json= {'token': login_list[1]['token'],
                           'channel_id': channel_list[2]['channel_id']})
    # As a global owner, user[1] can add himself as an channel_owner
    response_2 = requests.post(url + "channel/addowner/v1",
                               json = {'token': login_list[1]['token'],
                               'channel_id': channel_list[2]['channel_id'],
                               'u_id': login_list[1]['auth_user_id']})
    # As a global owner, user[1] can remove user[2] as a user in channel
    response_3 = requests.post(url + "channel/removeowner/v1",
                               json = {'token': login_list[1]['token'],
                                       'channel_id': channel_list[2]['channel_id'],
                                       'u_id': login_list[2]['auth_user_id']})
    # As a global owner, user[1] cannot remove the last owner in channel
    response_4 = requests.post(url + "channel/removeowner/v1",
                               json = {'token': login_list[1]['token'],
                                       'channel_id': channel_list[1]['channel_id'],
                                       'u_id': login_list[1]['auth_user_id']})
    assert response_1.status_code == 200
    assert response_2.status_code == 200
    assert response_3.status_code == 200
    assert response_4.status_code == InputError.code
    
def test_admin_userpermission_change_to_2(user_list, login_list):
    '''
    
    This test is to test change user's permission to 2 successfully
    
    '''
    # set user[1] as a owner
    requests.post(url + 'admin/userpermission/change/v1',
                  json = {'token': login_list[0]['token'],
                          'u_id': login_list[1]['auth_user_id'],
                          'permission_id': 1})
    # set user[0] as a user
    requests.post(url + 'admin/userpermission/change/v1',
                  json = {'token': login_list[1]['token'],
                          'u_id': login_list[0]['auth_user_id'],
                          'permission_id': 2})
    response_1  = requests.delete(url + 'admin/user/remove/v1',
                                  json = {'token': login_list[0]['token'],
                                          'u_id': login_list[2]['auth_user_id']})
    assert response_1.status_code == AccessError.code
    
def test_admin_userpermission_change_invalid_u_id(user_list, login_list):
    '''
    
    This test is to test when u_id does not refer to a valid user
    
    Raises:
        InputError
        
    '''
    new_id = random.randint(-65535, 65535)
    invalid_u_id = []
    while len(invalid_u_id) < 1:
        if not new_id in [login_list[i]['auth_user_id'] for i in range(0,4)]:
            invalid_u_id.append(new_id)
    
    response_1 = requests.post(url + 'admin/userpermission/change/v1',
                               json = {'token': login_list[0]['token'],
                                       'u_id': invalid_u_id[0],
                                       'permission_id': 1})
    assert response_1.status_code == InputError.code
    
def test_admin_userpermission_change_the_only_owner(user_list, login_list):
    '''
    
    This test is to test when u_id refers to a user who is the only global 
    owner and they are being demoted to a user
    
    Raises:
        InputError
    
    '''
    response_1 = requests.post(url + 'admin/userpermission/change/v1',
                               json = {'token': login_list[0]['token'],
                                       'u_id': login_list[0]['auth_user_id'],
                                       'permission_id': 2})
    assert response_1.status_code == InputError.code
    
def test_admin_userpermission_change_invalid_permission_id(user_list, login_list):
    '''
    
    This test is to test when permission_id is invalid
    
    Raises:
        InputError
    
    '''
    response_1 = requests.post(url + 'admin/userpermission/change/v1',
                               json = {'token': login_list[0]['token'],
                                       'u_id': login_list[1]['auth_user_id'],
                                       'permission_id': 10})
    assert response_1.status_code == InputError.code
    
def test_admin_userpermission_change_already_owner(user_list, login_list):
    '''
    
    This test is to test when the user already has the permissions level of permission_id
    
    Raises:
        InputError
    
    '''
    response_1 = requests.post(url + 'admin/userpermission/change/v1',
                               json = {'token': login_list[0]['token'],
                                       'u_id': login_list[0]['auth_user_id'],
                                       'permission_id': 1})
    assert response_1.status_code == InputError.code
    response_2 = requests.post(url + 'admin/userpermission/change/v1',
                               json = {'token': login_list[0]['token'],
                                       'u_id': login_list[1]['auth_user_id'],
                                       'permission_id': 2})
    assert response_2.status_code == InputError.code
    
def test_admin_userpermission_change_invalid_auth_user(user_list, login_list):
    '''
    
    This test is to test when the authorised user is not a global owner
    
    Raises:
        AccessError
    
    '''
    response_1 = requests.post(url + 'admin/userpermission/change/v1',
                               json = {'token': login_list[1]['token'],
                                       'u_id': login_list[2]['auth_user_id'],
                                       'permission_id': 1})
    assert response_1.status_code == AccessError.code
    response_2 = requests.post(url + 'admin/userpermission/change/v1',
                               json = {'token': login_list[1]['token'],
                                       'u_id': login_list[2]['auth_user_id'],
                                       'permission_id': 2})
    assert response_2.status_code == AccessError.code
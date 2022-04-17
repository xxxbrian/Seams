from cgitb import reset
from pickle import TRUE
import pytest
import requests
from src.config import url
from src.error import InputError, AccessError
from src.server import channels_list
import random

@pytest.fixture(name = 'login_list')
def login_users():
    '''
    
    This function is to pre-login 4 users for further tests
    
    returns:
        login_list, contains 4 pre-register users' information
        
    '''
    login_list = []
    requests.delete(f"{url}clear/v1", json = {})    # clear all info in server
    requests.post(f"{url}auth/register/v2",
                                   json = { 'email': 'z5374603@unsw.com',
                                            'password': '123456',
                                            'name_first': 'Steve',
                                            'name_last': 'Yang'})
    requests.post(f"{url}auth/register/v2",
                                   json = { 'email': 'z5374602@unsw.com',
                                            'password': '123456',
                                            'name_first': 'Brian',
                                            'name_last': 'Lee'})
    requests.post(f"{url}auth/register/v2",
                                   json = { 'email': 'z5374601@unsw.com',
                                            'password': '123456',
                                            'name_first': 'Bojin',
                                            'name_last': 'Li'})
    requests.post(f"{url}auth/register/v2",
                                   json = {  'email': 'z5374600@unsw.com',
                                            'password': '123456',
                                            'name_first':'Cicy',
                                            'name_last': 'Zhou'})
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
                                              'is_public': False}).json())
    return channel_list

######################################## Test_channel/leave/v1 ########################################

def test_channel_leave_normal(login_list, channel_list):
    '''
    
    This test is to test user leaves channel successfully
    
    Assumption: 
        channel/join/v2 is working well
        channel/details/v2 is working well
        
    '''
    # user[1] joins channel[0]
    requests.post(url + 'channel/join/v2',
                  json = {'token': login_list[1]['token'],
                          'channel_id': channel_list[0]['channel_id']})
    # user[1] leaves channel[0]
    requests.post(url + 'channel/leave/v1',
                  json = {'token': login_list[1]['token'],
                          'channel_id': channel_list[0]['channel_id']})
    response_1 = requests.get(url + 'channel/details/v2',
                              params = {'token': login_list[0]['token'],
                                        'channel_id': channel_list[0]['channel_id']}).json()
    assert response_1['name'] == "Steve's channel"
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
    
def test_channel_leave_owner_leave(login_list, channel_list):
    '''
    
    This test is to test the owner leaves the channel but the channel remain
    
    Assumption: 
        channels/listall/v2 is working well
        
    '''
    # user[0] leaves channel[0]
    requests.post(url + 'channel/leave/v1',
                  json = {'token': login_list[0]['token'],
                          'channel_id': channel_list[0]['channel_id']})
    response_1 = requests.get(url + 'channels/listall/v2',
                              params = {'token': login_list[0]['token'],}).json()
    assert response_1 == {
        'channels':[
    {
        'channel_id': channel_list[0]['channel_id'],
        'name': "Steve's channel"
    },
    {
        'channel_id': channel_list[1]['channel_id'],
        'name': "Brian's channel"
    }]}
    
def test_channel_leave_invalid_channel_id(login_list, channel_list):
    '''
    
    This test is to test when channel id does not refer to a valid channel
    
    Raises:
        InputError
        
    '''
    new_id = random.randint(-65535, 65535)
    invalid_channel_id = []
    while len(invalid_channel_id) < 1:
        if not new_id in [channel_list[i]['channel_id'] for i in range(0,2)]:
            invalid_channel_id.append(new_id)
    response_1 = requests.post(url + 'channel/leave/v1',
                               json = {'token': login_list[0]['token'],
                                       'channel_id': invalid_channel_id[0]})
    assert response_1.status_code == InputError.code
    
def test_channel_leave_invalid_user(login_list, channel_list):
    '''
    
    This test is to test when user who isn't in the channel but want to leave
    
    Raises: 
        AccessError
        
    '''
    response_1 = requests.post(url + 'channel/leave/v1',
                               json = {'token': login_list[3]['token'],
                                       'channel_id': channel_list[0]['channel_id']})
    assert response_1.status_code == AccessError.code
    
def test_channel_leave_invalid_token(login_list, channel_list):
    '''
    
    This test is to test when input invalid token
    
    Raises: 
        AccessError
        
    '''
    # user[1] joins channel[0]
    requests.post(url + 'channel/join/v2',
                  json = {'token': login_list[1]['token'],
                          'channel_id': channel_list[0]['channel_id']})
    # user[1] leaves channel[0]
    response_1 = requests.post(url + 'channel/leave/v1',
                  json = {'token': -1,
                          'channel_id': channel_list[0]['channel_id']})
    assert response_1.status_code == AccessError.code
    
    # user[0] leaves channel[0]
    response_2 = requests.post(url + 'channel/leave/v1',
                  json = {'token': -1,
                          'channel_id': channel_list[0]['channel_id']})
    assert response_2.status_code == AccessError.code
    
    new_id = random.randint(-65535, 65535)
    invalid_channel_id = []
    while len(invalid_channel_id) < 1:
        if not new_id in [channel_list[i]['channel_id'] for i in range(0,2)]:
            invalid_channel_id.append(new_id)
    response_3 = requests.post(url + 'channel/leave/v1',
                               json = {'token': -1,
                                       'channel_id': invalid_channel_id[0]})
    assert response_3.status_code == AccessError.code
    
######################################## Test_channel/addowner/v1 ########################################

def test_channel_add_owner_normal(login_list, channel_list):
    '''
    
    This test is to test when add an user as a owner successfully
    
    Assumption:
        channel/join/v2 is working well
        channel/details/v2 is working well
        
    '''
    requests.post(url + "channel/join/v2",
                  json = {'token': login_list[1]['token'],
                          'channel_id': channel_list[0]['channel_id']})
    requests.post(url + "channel/addowner/v1",
                  json = {'token': login_list[0]['token'],
                          'channel_id': channel_list[0]['channel_id'],
                          'u_id': login_list[1]['auth_user_id']})
    response_1 = requests.get(url + 'channel/details/v2',
                              params = {'token': login_list[0]['token'],
                                        'channel_id': channel_list[0]['channel_id']}).json()
    assert response_1['name'] == "Steve's channel"
    assert response_1['is_public'] == True
    assert response_1['owner_members'][0]['u_id'] == login_list[0]['auth_user_id']
    assert response_1['owner_members'][0]['email'] == "z5374603@unsw.com"
    assert response_1['owner_members'][0]['name_first'] == 'Steve'
    assert response_1['owner_members'][0]['name_last'] == 'Yang'
    assert response_1['owner_members'][0]['handle_str'] == 'steveyang'
    assert response_1['owner_members'][1]['u_id'] == login_list[1]['auth_user_id']
    assert response_1['owner_members'][1]['email'] == "z5374602@unsw.com"
    assert response_1['owner_members'][1]['name_first'] == 'Brian'
    assert response_1['owner_members'][1]['name_last'] == 'Lee'
    assert response_1['owner_members'][1]['handle_str'] == 'brianlee'
    assert response_1['all_members'][0]['u_id'] == login_list[0]['auth_user_id']
    assert response_1['all_members'][0]['email'] == "z5374603@unsw.com"
    assert response_1['all_members'][0]['name_first'] == 'Steve'
    assert response_1['all_members'][0]['name_last'] == 'Yang'
    assert response_1['all_members'][0]['handle_str'] == 'steveyang'
    assert response_1['all_members'][1]['u_id'] == login_list[1]['auth_user_id']
    assert response_1['all_members'][1]['email'] == "z5374602@unsw.com"
    assert response_1['all_members'][1]['name_first'] == 'Brian'
    assert response_1['all_members'][1]['name_last'] == 'Lee'
    assert response_1['all_members'][1]['handle_str'] == 'brianlee'

def test_channel_add_owner_invalid_channel_id(login_list, channel_list):
    '''
    
    This test is to test when channel_id does not refer to a valid channel
        
    Raises:
        InputError
        
    Assumption:
        channel/join/v2 is working well
        
    '''
    new_id = random.randint(-65535, 65535)
    invalid_channel_id = []
    while len(invalid_channel_id) < 1:
        if not new_id in [channel_list[i]['channel_id'] for i in range(0,2)]:
            invalid_channel_id.append(new_id)
            
    requests.post(url + "channel/join/v2",
                  json = {'token': login_list[1]['token'],
                          'channel_id': channel_list[0]['channel_id']})
    response_1 = requests.post(url + "channel/addowner/v1",
                               json = {'token': login_list[0]['token'],
                                       'channel_id': invalid_channel_id[0],
                                       'u_id': login_list[1]['auth_user_id']})
    assert response_1.status_code == InputError.code

def test_channel_add_owner_invalid_u_id(login_list, channel_list):
    '''
    
    This test is to test when u_id does not refer to a valid user
        
    Raises:
        InputError
        
    Assumption:
        channel/join/v2 is working well
        
    '''
    new_id = random.randint(-65535, 65535)
    invalid_u_id = []
    while len(invalid_u_id) < 1:
        if not new_id in [login_list[i]['auth_user_id'] for i in range(0,4)]:
            invalid_u_id.append(new_id)
            
    requests.post(url + "channel/join/v2",
                  json = {'token': login_list[1]['token'],
                          'channel_id': channel_list[0]['channel_id']})
    response_1 = requests.post(url + "channel/addowner/v1",
                               json = {'token': login_list[0]['token'],
                                       'channel_id': channel_list[0]['channel_id'],
                                       'u_id': invalid_u_id[0]})
    assert response_1.status_code == InputError.code

def test_channel_add_owner_wrong_u_id(login_list, channel_list):
    '''
    
    This test is to test when u_id refers to a user who is not a member of the channel
        
    Raises:
        InputError
        
    '''
            
    response_1 = requests.post(url + "channel/addowner/v1",
                               json = {'token': login_list[0]['token'],
                                       'channel_id': channel_list[0]['channel_id'],
                                       'u_id': login_list[1]['auth_user_id']})
    assert response_1.status_code == InputError.code
    
def test_channel_add_owner_add_owner_u_id(login_list, channel_list):
    '''
    
    This test is to test when u_id refers to a user who is already an owner of the channel
        
    Raises:
        InputError
        
    '''
            
    response_1 = requests.post(url + "channel/addowner/v1",
                               json = {'token': login_list[0]['token'],
                                       'channel_id': channel_list[0]['channel_id'],
                                       'u_id': login_list[0]['auth_user_id']})
    assert response_1.status_code == InputError.code
    
def test_channel_add_owner_no_permissions(login_list, channel_list):
    '''
    
    This test is to test when channel_id is valid and the authorised user does not 
    have owner permissions in the channel
    
    Assumption:
        channel/join/v2 is working well
        
    '''
    # user[1] and user[2] join the channel[0]
    requests.post(url + "channel/join/v2",
                  json = {'token': login_list[1]['token'],
                          'channel_id': channel_list[0]['channel_id']})
    requests.post(url + "channel/join/v2",
                  json = {'token': login_list[2]['token'],
                          'channel_id': channel_list[0]['channel_id']})
    
    response_1 = requests.post(url + "channel/addowner/v1",
                               json = {'token': login_list[1]['token'],
                                       'channel_id': channel_list[0]['channel_id'],
                                       'u_id': login_list[2]['auth_user_id']})
    assert response_1.status_code == AccessError.code
    
def test_channel_add_owner_invalid_token(login_list, channel_list):
    '''
    
    This test is to test when input invalid token
    
    Raises: 
        AccessError
        
    '''
    requests.post(url + "channel/join/v2",
                  json = {'token': login_list[1]['token'],
                          'channel_id': channel_list[0]['channel_id']})
    response_1 = requests.post(url + "channel/addowner/v1",
                  json = {'token': -1,
                          'channel_id': channel_list[0]['channel_id'],
                          'u_id': login_list[1]['auth_user_id']})
    assert response_1.status_code == AccessError.code
    
    new_id = random.randint(-65535, 65535)
    invalid_channel_id = []
    while len(invalid_channel_id) < 1:
        if not new_id in [channel_list[i]['channel_id'] for i in range(0,2)]:
            invalid_channel_id.append(new_id)
            
    requests.post(url + "channel/join/v2",
                  json = {'token': login_list[1]['token'],
                          'channel_id': channel_list[0]['channel_id']})
    response_2 = requests.post(url + "channel/addowner/v1",
                               json = {'token': -1,
                                       'channel_id': invalid_channel_id[0],
                                       'u_id': login_list[1]['auth_user_id']})
    assert response_2.status_code == AccessError.code
    
    new_id = random.randint(-65535, 65535)
    invalid_u_id = []
    while len(invalid_u_id) < 1:
        if not new_id in [login_list[i]['auth_user_id'] for i in range(0,4)]:
            invalid_u_id.append(new_id)
            
    requests.post(url + "channel/join/v2",
                  json = {'token': login_list[1]['token'],
                          'channel_id': channel_list[0]['channel_id']})
    response_3 = requests.post(url + "channel/addowner/v1",
                               json = {'token': -1,
                                       'channel_id': channel_list[0]['channel_id'],
                                       'u_id': invalid_u_id[0]})
    assert response_3.status_code == AccessError.code
    
    response_4 = requests.post(url + "channel/addowner/v1",
                               json = {'token': -1,
                                       'channel_id': channel_list[0]['channel_id'],
                                       'u_id': login_list[1]['auth_user_id']})
    assert response_4.status_code == AccessError.code
    
    response_5 = requests.post(url + "channel/addowner/v1",
                               json = {'token': -1,
                                       'channel_id': channel_list[0]['channel_id'],
                                       'u_id': login_list[0]['auth_user_id']})
    assert response_5.status_code == AccessError.code
    
######################################## Test_channel/removeowner/v1 ########################################
    
def test_channel_remove_owner_normal(login_list, channel_list):
    '''
    
    This test is to test when remove an user as a owner successfully
    
    Assumption:
        channel/join/v2 is working well
        channel/details/v2 is working well
        channel/addowner/v1 is working well
        
    '''
    requests.post(url + "channel/join/v2",
                  json = {'token': login_list[1]['token'],
                          'channel_id': channel_list[0]['channel_id']})
    requests.post(url + "channel/addowner/v1",
                  json = {'token': login_list[0]['token'],
                          'channel_id': channel_list[0]['channel_id'],
                          'u_id': login_list[1]['auth_user_id']})
    requests.post(url + "channel/removeowner/v1",
                  json = {'token': login_list[0]['token'],
                          'channel_id': channel_list[0]['channel_id'],
                          'u_id': login_list[1]['auth_user_id']})
    response_1 = requests.get(url + 'channel/details/v2',
                              params = {'token': login_list[0]['token'],
                                        'channel_id': channel_list[0]['channel_id']}).json()
    assert response_1['name'] == "Steve's channel"
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
    assert response_1['all_members'][1]['u_id'] == login_list[1]['auth_user_id']
    assert response_1['all_members'][1]['email'] == "z5374602@unsw.com"
    assert response_1['all_members'][1]['name_first'] == 'Brian'
    assert response_1['all_members'][1]['name_last'] == 'Lee'
    assert response_1['all_members'][1]['handle_str'] == 'brianlee'
    
def test_channel_remove_owner_invalid_channel_id(login_list, channel_list):
    '''
    
    This test is to test when channel_id does not refer to a valid channel
        
    Raises:
        InputError
        
    Assumption:
        channel/join/v2 is working well
        channel/addowner/v1 is working well
        
    '''
    new_id = random.randint(-65535, 65535)
    invalid_channel_id = []
    while len(invalid_channel_id) < 1:
        if not new_id in [channel_list[i]['channel_id'] for i in range(0,2)]:
            invalid_channel_id.append(new_id)
            
    requests.post(url + "channel/join/v2",
                  json = {'token': login_list[1]['token'],
                          'channel_id': channel_list[0]['channel_id']})
    requests.post(url + "channel/addowner/v1",
                  json = {'token': login_list[0]['token'],
                          'channel_id': channel_list[0]['channel_id'],
                          'u_id': login_list[1]['auth_user_id']})
    response_1 = requests.post(url + "channel/removeowner/v1",
                               json = {'token': login_list[0]['token'],
                                       'channel_id': invalid_channel_id[0],
                                       'u_id': login_list[1]['auth_user_id']})
    assert response_1.status_code == InputError.code
    
def test_channel_remove_owner_invalid_u_id(login_list, channel_list):
    '''
    
    This test is to test when u_id does not refer to a valid user
        
    Raises:
        InputError
        
    Assumption:
        channel/join/v2 is working well
        channel/addowner/v1 is working well
        
    '''
    new_id = random.randint(-65535, 65535)
    invalid_u_id = []
    while len(invalid_u_id) < 1:
        if not new_id in [login_list[i]['auth_user_id'] for i in range(0,4)]:
            invalid_u_id.append(new_id)
            
    requests.post(url + "channel/join/v2",
                  json = {'token': login_list[1]['token'],
                          'channel_id': channel_list[0]['channel_id']})
    requests.post(url + "channel/addowner/v1",
                  json = {'token': login_list[0]['token'],
                          'channel_id': channel_list[0]['channel_id'],
                          'u_id': login_list[1]['auth_user_id']})
    response_1 = requests.post(url + "channel/removeowner/v1",
                               json = {'token': login_list[0]['token'],
                                       'channel_id': channel_list[0]['channel_id'],
                                       'u_id': invalid_u_id[0]})
    assert response_1.status_code == InputError.code
    
def test_channel_remove_owner_not_owner_u_id(login_list, channel_list):
    '''
    
    This test is to test when u_id refers to a user who is not an owner of the channel
        
    Raises:
        InputError
        
    Assumption:
        channel/join/v2 is working well
        
    '''

    requests.post(url + "channel/join/v2",
                  json = {'token': login_list[1]['token'],
                          'channel_id': channel_list[0]['channel_id']})
    response_1 = requests.post(url + "channel/removeowner/v1",
                               json = {'token': login_list[0]['token'],
                                       'channel_id': channel_list[0]['channel_id'],
                                       'u_id':login_list[1]['auth_user_id']})
    assert response_1.status_code == InputError.code
    
def test_channel_remove_owner_only_owner_u_id(login_list, channel_list):
    '''
    
    This test is to test when u_id refers to a user who is currently the only owner of the channel
        
    Raises:
        InputError
        
    '''

    response_1 = requests.post(url + "channel/removeowner/v1",
                               json = {'token': login_list[0]['token'],
                                       'channel_id': channel_list[0]['channel_id'],
                                       'u_id':login_list[0]['auth_user_id']})
    assert response_1.status_code == InputError.code
    
def test_channel_remove_owner_no_permissions(login_list, channel_list):
    '''
    
    This test is to test when channel_id is valid and the authorised user does not 
    have owner permissions in the channel
        
    Raises:
        InputError
        
    Assumption:
        channel/join/v2 is working well

    '''
            
    requests.post(url + "channel/join/v2",
                  json = {'token': login_list[1]['token'],
                          'channel_id': channel_list[0]['channel_id']})
    response_1 = requests.post(url + "channel/removeowner/v1",
                               json = {'token': login_list[1]['token'],
                                       'channel_id': channel_list[0]['channel_id'],
                                       'u_id': login_list[0]['auth_user_id']})
    assert response_1.status_code == AccessError.code
    
def test_channel_remove_owner_invalid_token(login_list, channel_list):
    '''
    
    This test is to test when input invalid token
    
    Raises: 
        AccessError
        
    '''
    requests.post(url + "channel/join/v2",
                  json = {'token': login_list[1]['token'],
                          'channel_id': channel_list[0]['channel_id']})
    requests.post(url + "channel/addowner/v1",
                  json = {'token': login_list[0]['token'],
                          'channel_id': channel_list[0]['channel_id'],
                          'u_id': login_list[1]['auth_user_id']})
    response_1 = requests.post(url + "channel/removeowner/v1",
                  json = {'token': -1,
                          'channel_id': channel_list[0]['channel_id'],
                          'u_id': login_list[1]['auth_user_id']})
    assert response_1.status_code == AccessError.code
    
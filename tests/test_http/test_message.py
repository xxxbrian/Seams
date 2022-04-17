import pytest
import requests
import random
from src.config import url
from src.error import InputError, AccessError
import time

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
        
    dm_0 = 'bojinli, brianlee, steveyang'
    dm_1 = 'bojinli, cicyzhou, steveyang'
    dm_2 = 'bojinli, brianlee, cicyzhou'
    
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

######################################## Test_message_send_v1 ########################################
def test_mesage_send_with_tag(channel_list, login_list):
    '''
    
    Test is to test when user sends a message with @
    
    '''
    requests.post(url + 'message/send/v1',
                  json = {'token': login_list[0]['token'],
                          'channel_id': channel_list[0]['channel_id'],
                          'message': 'I am SuperBoy @steveyang'})
    response_1 = requests.get(url + 'notifications/get/v1',
                              params={'token': login_list[0]['token']}).json()
    assert response_1['notifications'][0]['channel_id'] == channel_list[0]['channel_id']
    assert response_1['notifications'][0]['dm_id'] == -1
    assert response_1['notifications'][0]['notification_message'] == "steveyang tagged you in Steve's channel: I am SuperBoy @steve"
    
def test_mesage_senddm_with_tag(dm_list, login_list):
    '''
    
    Test is to test when user sends a message with @
    
    '''
    requests.post(url + 'message/senddm/v1',
                  json = {'token': login_list[0]['token'],
                          'dm_id': dm_list[0]['dm_id'],
                          'message': 'I am SuperBoy @steveyang'})
    response_1 = requests.get(url + 'notifications/get/v1',
                              params={'token': login_list[0]['token']}).json()
    assert response_1['notifications'][0]['dm_id'] == dm_list[0]['dm_id']
    assert response_1['notifications'][0]['channel_id'] == -1
    assert response_1['notifications'][0]['notification_message'] == "steveyang tagged you in bojinli, brianlee, steveyang: I am SuperBoy @steve"

def test_message_send_invalid_channel_id(channel_list, login_list):
    '''
    
    Test for input a invalid channel_id
    
    Raises:
        Inputerror
        
    '''
    new_id = random.randint(-65535, 65535)
    invalid_channel_id = []
    while len(invalid_channel_id) < 1:
        if not new_id in [channel_list[i]['channel_id'] for i in range(0,4)]:
            invalid_channel_id.append(new_id)
    response_1 = requests.post(url + 'message/send/v1',
                               json = {'token': login_list[0]['token'],
                                       'channel_id': invalid_channel_id[0],
                                       'message': 'Hello world!'})
    assert response_1.status_code == InputError.code
    
def test_message_send_empty_message(channel_list, login_list):
    '''
    
    Test for input an empty message
    
    Raises:
        InputError
        
    '''
    response_1 = requests.post(url + 'message/send/v1',
                               json = {'token': login_list[0]['token'],
                                       'channel_id': channel_list[0]['channel_id'],
                                       'message': ''})
    assert response_1.status_code == InputError.code
    
def test_message_send_too_long_message(channel_list, login_list):
    '''
    
    Test for input more than 1000 characters
    
    Raises:
        InputError
        
    '''
    too_long_message = ""
    while(len(too_long_message) < 1001):
        too_long_message += 'a'
    
    response_1 = requests.post(url + 'message/send/v1',
                               json = {'token': login_list[0]['token'],
                                       'channel_id': channel_list[0]['channel_id'],
                                       'message': too_long_message})
    assert response_1.status_code == InputError.code
    
def test_message_send_auth_user_out_of_channel(channel_list, login_list):
    '''
    
    This test is test when authorised user is not amember of channel
    
    Raises:
        AccessError
        
    '''
    response_1 = requests.post(url + 'message/send/v1',
                               json = {'token': login_list[1]['token'],
                                       'channel_id': channel_list[0]['channel_id'],
                                       'message': "Hello"})
    assert response_1.status_code == AccessError.code
    
def test_message_send_invalid_token(channel_list, login_list):
    '''
    
    This test is to test when toke is invalid
    
    Raises:
        AccessError
        
    '''
    # invalid channel id
    new_id = random.randint(-65535, 65535)
    invalid_channel_id = []
    while len(invalid_channel_id) < 1:
        if not new_id in [channel_list[i]['channel_id'] for i in range(0,4)]:
            invalid_channel_id.append(new_id)
    response_1 = requests.post(url + 'message/send/v1',
                               json = {'token': -1,
                                       'channel_id': invalid_channel_id[0],
                                       'message': 'Hello world!'})
    assert response_1.status_code == AccessError.code
    
    # invalid message
    response_2 = requests.post(url + 'message/send/v1',
                               json = {'token': -1,
                                       'channel_id': channel_list[0]['channel_id'],
                                       'message': ''})
    assert response_2.status_code == AccessError.code
    
    too_long_message = ""
    while(len(too_long_message) < 1001):
        too_long_message += 'a'
    
    response_3 = requests.post(url + 'message/send/v1',
                               json = {'token': -1,
                                       'channel_id': channel_list[0]['channel_id'],
                                       'message': too_long_message})
    assert response_3.status_code == AccessError.code
    
######################################## Test_message_edit_v1 ########################################

def test_channel_message_edit_normal(login_list, channel_list):
    '''
    
    This test is to test edit message successfully in channel
    
    Assumption:
        message/send/v1 is working well
        message/edit/v1 is working well 
    
    '''
    # send 3 messages in channel[0]
    response_1 = requests.post(url + 'message/send/v1',
                               json = {'token': login_list[0]['token'],
                                       'channel_id': channel_list[0]['channel_id'],
                                       'message': 'Hello world!'}).json()
    response_2 = requests.post(url + 'message/send/v1',
                               json = {'token': login_list[0]['token'],
                                       'channel_id': channel_list[0]['channel_id'],
                                       'message': 'Hello world!'}).json()
    requests.post(url + 'message/send/v1',
                  json = {'token': login_list[0]['token'],
                          'channel_id': channel_list[0]['channel_id'],
                          'message': 'Hello world!'})
    
    # change message[2]
    requests.put(url + 'message/edit/v1',
                 json = {'token': login_list[0]['token'],
                         'message_id': response_1['message_id'],
                         'message':'Hello'})
    
    response_4 = requests.get(url + 'channel/messages/v2',
                              params = {'token': login_list[0]['token'],
                                        'channel_id': channel_list[0]['channel_id'],
                                        'start': 0}).json()
    assert response_4['messages'][2]['message'] == 'Hello'
    
    # delete message[1]
    requests.put(url + 'message/edit/v1',
                 json = {'token': login_list[0]['token'],
                         'message_id': response_2['message_id'],
                         'message':''})
    response_5 = requests.get(url + 'channel/messages/v2',
                              params = {'token': login_list[0]['token'],
                                        'channel_id': channel_list[0]['channel_id'],
                                        'start': 0}).json()
    assert response_5['messages'][0]['message'] == 'Hello world!'
    assert response_5['messages'][1]['message'] == 'Hello'
    
def test_dm_message_edit_normal(login_list, dm_list):
    '''
    
    This test is to test edit message successfully in DM
    
    Assumption:
        message/senddm/v1 is working well
        dm/messages/v1 is working well 
    
    '''
    # send 3 messages in dm[0]
    response_1 = requests.post(url + 'message/senddm/v1',
                               json = {'token': login_list[0]['token'],
                                       'dm_id': dm_list[0]['dm_id'],
                                       'message': 'Hello world!'}).json()
    response_2 = requests.post(url + 'message/senddm/v1',
                               json = {'token': login_list[0]['token'],
                                       'dm_id': dm_list[0]['dm_id'],
                                       'message': 'Hello world!'}).json()
    requests.post(url + 'message/senddm/v1',
                  json = {'token': login_list[0]['token'],
                          'dm_id': dm_list[0]['dm_id'],
                          'message': 'Hello world!'}).json()
    
    # change message[2]
    requests.put(url + 'message/edit/v1',
                 json = {'token': login_list[0]['token'],
                         'message_id': response_1['message_id'],
                         'message':'Hello'})
    
    response_4 = requests.get(url + 'dm/messages/v1',
                              params = {'token': login_list[0]['token'],
                                        'dm_id': dm_list[0]['dm_id'],
                                        'start': 0}).json()
    assert response_4['messages'][2]['message'] == 'Hello'
    
    # delete message[1]
    requests.put(url + 'message/edit/v1',
                 json = {'token': login_list[0]['token'],
                         'message_id': response_2['message_id'],
                         'message':''})
    response_5 = requests.get(url + 'dm/messages/v1',
                              params = {'token': login_list[0]['token'],
                                        'dm_id': dm_list[0]['dm_id'],
                                        'start': 0}).json()
    assert response_5['messages'][0]['message'] == 'Hello world!'
    assert response_5['messages'][1]['message'] == 'Hello'
    
def test_channel_message_edit_too_long_message(login_list, channel_list):
    '''
    
    This test is to test the message which has been edit is more than 1000 characters
    in channel
    
    Raises:
        Inputerror
        
     Assumption:
        message/send/v1 is working well

    '''
    too_long_message = ""
    while(len(too_long_message) < 1001):
        too_long_message += 'a'
        
    response_1 = requests.post(url + 'message/send/v1',
                               json = {'token': login_list[0]['token'],
                                       'channel_id': channel_list[0]['channel_id'],
                                       'message': 'Hello world!'}).json()
    response_2 = requests.put(url + 'message/edit/v1',
                              json = {'token': login_list[0]['token'],
                                      'message_id': response_1['message_id'],
                                      'message': too_long_message})
    assert response_2.status_code == InputError.code
    
def test_dm_message_edit_too_long_message(login_list, dm_list):
    '''
    
    This test is to test the message which has been edit is more than 1000 characters
     in DM
    
    Raises:
        InputError
        
    Assumption:
        message/senddm/v1 is working well
        
    '''  
    too_long_message = ""
    while(len(too_long_message) < 1001):
        too_long_message += 'a'
    response_1 = requests.post(url + 'message/senddm/v1',
                               json = {'token': login_list[0]['token'],
                                       'dm_id': dm_list[0]['dm_id'],
                                       'message': 'Hello world!'}).json()
    response_2 = requests.put(url + 'message/edit/v1',
                              json = {'token': login_list[0]['token'],
                                      'message_id': response_1['message_id'],
                                      'message': too_long_message})
    assert response_2.status_code == InputError.code
    
def test_channel_message_edit_wrong_message_id(login_list, channel_list):
    '''
    
    This test is to test message_id does not refer to a valid message within a channel
    that the authorised user has joined
    
    Raises:
        InputError
       
     Assumption:
        message/send/v1 is working well
         
    '''
    response_1 = requests.post(url + 'message/send/v1',
                               json = {'token': login_list[0]['token'],
                                       'channel_id': channel_list[0]['channel_id'],
                                       'message': 'Hello world!'}).json()
    new_id = random.randint(-65535, 65535)
    invalid_message_id = []
    while len(invalid_message_id) < 1:
        if new_id != response_1['message_id']:
            invalid_message_id.append(new_id)
    response_2 = requests.put(url + 'message/edit/v1',
                              json = {'token': login_list[0]['token'],
                                      'message_id': invalid_message_id[0],
                                      'message': "Hi hi"})
    assert response_2.status_code == InputError.code
      
def test_channel_message_edit_user_not_in_channel(login_list, channel_list):
    '''
    
    This test is to test message_id does not refer to a valid message within a channel
    that the authorised user has joined
    
    Raises:
        InputError
       
     Assumption:
        message/send/v1 is working well
         
    '''
    response_1 = requests.post(url + 'message/send/v1',
                               json = {'token': login_list[0]['token'],
                                       'channel_id': channel_list[0]['channel_id'],
                                       'message': 'Hello world!'}).json()
    response_2 = requests.put(url + 'message/edit/v1',
                              json = {'token': login_list[3]['token'],
                                      'message_id': response_1['message_id'],
                                      'message': "Hi hi"})
    assert response_2.status_code == InputError.code
    
def test_dm_message_edit_wrong_message_id(login_list, dm_list):
    '''
    
    This test is to test message_id does not refer to a valid message within a DM
    that the authorised user has joined
    
    Raises:
        InputError
        
    Assumption:
        message/senddm/v1 is working well
        
    '''  
    response_1 = requests.post(url + 'message/senddm/v1',
                               json = {'token': login_list[0]['token'],
                                       'dm_id': dm_list[0]['dm_id'],
                                       'message': 'Hello world!'}).json()
    new_id = random.randint(-65535, 65535)
    invalid_message_id = []
    while len(invalid_message_id) < 1:
        if new_id != response_1['message_id']:
            invalid_message_id.append(new_id)
    response_2 = requests.put(url + 'message/edit/v1',
                              json = {'token': login_list[0]['token'],
                                      'message_id': invalid_message_id[0],
                                      'message': "Hi hi"})
    assert response_2.status_code == InputError.code
    
def test_message_edit_channel_invalid_user(login_list, channel_list):
    '''
    
    This test is to test when invalid user want to edit a valid message in valid channel
    
    Raises:
        Accesserror
        
    Assumption:
        message/send/v1 is working well
        channel/join/v2 is working well
        
    '''
    requests.post(url + "channel/join/v2",
                  json = {'token': login_list[1]['token'],
                          'channel_id': channel_list[0]['channel_id']})
    response_1 = requests.post(url + 'message/send/v1',
                               json = {'token': login_list[0]['token'],
                                       'channel_id': channel_list[0]['channel_id'],
                                       'message': 'Hello world!'}).json()
    response_2 = requests.put(url + 'message/edit/v1',
                              json = {'token': login_list[1]['token'],
                                      'message_id': response_1['message_id'],
                                      'message': "Hi hi"})
    assert response_2.status_code == AccessError.code
    
def test_message_edit_dm_invalid_user(login_list, dm_list):
    '''
    
    This test is to test when invalid user want to edit a valid message in valid channel
    
    Raises:
        Accesserror
        
    Assumption:
        message/senddm/v1 is working well
        
    '''
    response_1 = requests.post(url + "message/senddm/v1",
                               json = {'token': login_list[0]['token'],
                                       'dm_id': dm_list[0]['dm_id'],
                                       'message': 'Hello world!'}).json()
    response_2 = requests.put(url + 'message/edit/v1',
                              json = {'token': login_list[1]['token'],
                                      'message_id': response_1['message_id'],
                                      'message': "Hi hi"})
    assert response_2.status_code == AccessError.code
    
def test_channel_message_edit_owner_edit_message(login_list, channel_list):
    '''
    
    This test it to test owner edit message successfully
    
    Assumption:
        channel/addowner/v1 is working well
        channel/join/v2 is working well
        channel/messages/v2 is working well
        message/send/v1 is working well
        
    '''
    # add user[1] as an owner in channel[0]
    requests.post(url + "channel/join/v2",
                  json = {'token': login_list[1]['token'],
                          'channel_id': channel_list[0]['channel_id']})
    requests.post(url + "channel/addowner/v1",
                  json = {'token': login_list[0]['token'],
                          'channel_id': channel_list[0]['channel_id'],
                          'u_id': login_list[1]['auth_user_id']})
    response_1 = requests.post(url + 'message/send/v1',
                               json = {'token': login_list[0]['token'],
                                       'channel_id': channel_list[0]['channel_id'],
                                       'message': 'Hello world!'}).json()
    requests.put(url + 'message/edit/v1',
                 json = {'token': login_list[1]['token'],
                         'message_id': response_1['message_id'],
                         'message': "Hi hi"})
    response_3 = requests.get(url + 'channel/messages/v2',
                              params = {'token': login_list[1]['token'],
                                        'channel_id': channel_list[0]['channel_id'],
                                        'start': 0}).json()
    assert response_3['messages'][0]['message'] == 'Hi hi'
    
def test_dm_message_edit_owner_edit_message(login_list, dm_list):
    '''
    
    This test is to test dm owner edit message from other users successfully
    
    Assumption:
        message/senddm/v1 is working well
        dm/messages/v1 is working well 
        
    '''
    response_1 = requests.post(url + "message/senddm/v1",
                               json = {'token': login_list[1]['token'],
                                       'dm_id': dm_list[0]['dm_id'],
                                       'message': 'Hello world!'}).json()
    response_2 = requests.post(url + "message/senddm/v1",
                               json = {'token': login_list[2]['token'],
                                       'dm_id': dm_list[0]['dm_id'],
                                       'message': 'Steve'}).json()
    requests.put(url + 'message/edit/v1',
                 json = {'token': login_list[0]['token'],
                         'message_id': response_1['message_id'],
                         'message': "Hi"})
    requests.put(url + 'message/edit/v1',
                 json = {'token': login_list[0]['token'],
                         'message_id': response_2['message_id'],
                         'message': "Yang"})
    response_3 = requests.get(url + 'dm/messages/v1',
                              params = {'token': login_list[0]['token'],
                                        'dm_id': dm_list[0]['dm_id'],
                                        'start': 0}).json()
    assert response_3['messages'][0]['message'] == 'Yang'
    assert response_3['messages'][1]['message'] == 'Hi'
    
def test_dm_message_edit_invalid_token(login_list, channel_list):
    '''
    
    This test is to test when input invalid token
    
    Raises: 
        AccessError
        
    '''
    response_1 = requests.post(url + 'message/send/v1',
                               json = {'token': login_list[0]['token'],
                                       'channel_id': channel_list[0]['channel_id'],
                                       'message': 'Hello world!'}).json()
    response_2 = requests.put(url + 'message/edit/v1',
                 json = {'token': -1,
                         'message_id': response_1['message_id'],
                         'message':'Hello'})
    assert response_2.status_code == AccessError.code
    
def test_dm_message_edit_global_owner_cant_edit(login_list, dm_list):
    '''
    
    This test is to test when global owner want to edit members' messages in dm
    
    Assumption:
        admin/userpermission/change/v1 is working well
    
    Raises: 
        AccessError
        
    '''
    # set user[2] as an owner
    requests.post(url + 'admin/userpermission/change/v1',
                  json = {'token': login_list[0]['token'],
                          'u_id': login_list[2]['auth_user_id'],
                          'permission_id': 1})
    response_1 = requests.post(url + "message/senddm/v1",
                  json = {'token': login_list[3]['token'],
                          'dm_id': dm_list[2]['dm_id'],
                          'message': 'Hello world!'}).json()
    response_2 = requests.put(url + 'message/edit/v1',
                              json = {'token': login_list[2]['token'],
                                      'message_id': response_1['message_id'],
                                      'message':'Hello'})
    assert response_2.status_code == AccessError.code

######################################## message/remove/v1 ########################################

def test_channel_message_remove_normal(login_list, channel_list):
    '''
    
    This test is to test the normal situation of removing test from a channel
    
    Assumpition:
        message/send/v1 is working well
        channel/messages/v2 is working well (for check)
        
    '''
    requests.post(url + 'message/send/v1',
                  json = {'token': login_list[0]['token'],
                          'channel_id': channel_list[0]['channel_id'],
                          'message': 'Hello'})
    requests.post(url + 'message/send/v1',
                  json = {'token': login_list[0]['token'],
                          'channel_id': channel_list[0]['channel_id'],
                          'message': 'world'})
    response_1 = requests.post(url + 'message/send/v1',
                               json = {'token': login_list[0]['token'],
                                       'channel_id': channel_list[0]['channel_id'],
                                       'message': 'Steve'}).json()  
    # remove 'Steve'
    requests.delete(url + "message/remove/v1",
                    json = {'token': login_list[0]['token'],
                            'message_id': response_1['message_id']})
    response_2 = requests.get(url + 'channel/messages/v2',
                              params = {'token': login_list[0]['token'],
                                        'channel_id': channel_list[0]['channel_id'],
                                        'start': 0}).json()
    assert response_2['messages'][0]['message'] == 'world'
    assert response_2['messages'][1]['message'] == 'Hello'
    
def test_dm_message_remove_normal(login_list, dm_list):
    '''
    
    This test is to test the normal situation of removing test from a DM
    
    Assumption:
        message/senddm/v1 is working well
        dm/messages/v1 is working well 
    
    '''
    # send 3 messages in dm[0]
    requests.post(url + 'message/senddm/v1',
                  json = {'token': login_list[0]['token'],
                          'dm_id': dm_list[0]['dm_id'],
                          'message': 'Hello'}).json()
    response_2 = requests.post(url + 'message/senddm/v1',
                               json = {'token': login_list[0]['token'],
                                       'dm_id': dm_list[0]['dm_id'],
                                       'message': 'Hello world!'}).json()
    requests.post(url + 'message/senddm/v1',
                  json = {'token': login_list[0]['token'],
                          'dm_id': dm_list[0]['dm_id'],
                          'message': 'world!'}).json()
    
    # remove the second message
    requests.delete(url + "message/remove/v1",
                    json = {'token': login_list[0]['token'],
                            'message_id': response_2['message_id']})
    response_4 = requests.get(url + 'dm/messages/v1',
                              params = {'token': login_list[0]['token'],
                                        'dm_id': dm_list[0]['dm_id'],
                                        'start': 0}).json()
    assert response_4['messages'][0]['message'] == 'world!'
    assert response_4['messages'][1]['message'] == 'Hello'
    
def test_channel_message_remove_invalid_message_id(login_list, channel_list):
    '''
    
    This test is to test when remove a message, which message_id is invalid in channel
    
    Raises:
        InputError
        
    Assumpition:
        message/send/v1 is working well
        
    '''
    response_1 = requests.post(url + 'message/send/v1',
                               json = {'token': login_list[0]['token'],
                                       'channel_id': channel_list[0]['channel_id'],
                                       'message': 'Hello'}).json()
    new_id = random.randint(-65535, 65535)
    invalid_message_id = []
    while len(invalid_message_id) < 1:
        if new_id != response_1['message_id']:
            invalid_message_id.append(new_id)
    response_2 = requests.delete(url + "message/remove/v1",
                                 json = {'token': login_list[0]['token'],
                                         'message_id': invalid_message_id})
    assert response_2.status_code == InputError.code
    
def test_dm_message_remove_invalid_message_id(login_list, dm_list):
    '''
    
    This test is to test when remove a message, which message_id is invalid in dm
    
    Raises:
        InputError
        
    Assumpition:
        message/senddm/v1 is working well
        
    '''
    response_1 = requests.post(url + 'message/senddm/v1',
                               json = {'token': login_list[0]['token'],
                                       'dm_id': dm_list[0]['dm_id'],
                                       'message': 'Hello'}).json()
    new_id = random.randint(-65535, 65535)
    invalid_message_id = []
    while len(invalid_message_id) < 1:
        if new_id != response_1['message_id']:
            invalid_message_id.append(new_id)
    response_2 = requests.delete(url + "message/remove/v1",
                                 json = {'token': login_list[0]['token'],
                                         'message_id': invalid_message_id})
    assert response_2.status_code == InputError.code

def test_channel_message_remove_invalid_user(login_list, channel_list):
    '''
    
    This test is to test when invalid user remove message
    
    Raises:
        AccessError
        
    Assumption:
        message/send/v1 is working well
        channel/join/v2 is working well
        
    '''
    requests.post(url + "channel/join/v2",
                  json = {'token': login_list[1]['token'],
                          'channel_id': channel_list[0]['channel_id']})
    response_1 = requests.post(url + 'message/send/v1',
                               json = {'token': login_list[0]['token'],
                                       'channel_id': channel_list[0]['channel_id'],
                                       'message': 'Hello world!'}).json()
    response_2 = requests.delete(url + 'message/remove/v1',
                              json = {'token': login_list[1]['token'],
                                      'message_id': response_1['message_id']})
    assert response_2.status_code == AccessError.code
    
def test_message_remove_dm_invalid_user(login_list, dm_list):
    '''
    
    This test is to test when invalid user want to remove a valid message in valid channel
    
    Raises:
        Accesserror
        
    Assumption:
        message/senddm/v1 is working well
        
    '''
    response_1 = requests.post(url + "message/senddm/v1",
                               json = {'token': login_list[0]['token'],
                                       'dm_id': dm_list[0]['dm_id'],
                                       'message': 'Hello world!'}).json()
    response_2 = requests.delete(url + 'message/remove/v1',
                              json = {'token': login_list[1]['token'],
                                      'message_id': response_1['message_id']})
    assert response_2.status_code == AccessError.code
    
def test_message_remove_owner_remove_message(login_list, channel_list):
    '''
    
    This test it to test owner remove message successfully
    
    Assumption:
        channel/addowner/v1 is working well
        channel/join/v2 is working well
        channel/messages/v2 is working well
        message/send/v1 is working well
        
    '''
    # add user[1] as an owner in channel[0]
    requests.post(url + "channel/join/v2",
                  json = {'token': login_list[1]['token'],
                          'channel_id': channel_list[0]['channel_id']})
    requests.post(url + "channel/addowner/v1",
                  json = {'token': login_list[0]['token'],
                          'channel_id': channel_list[0]['channel_id'],
                          'u_id': login_list[1]['auth_user_id']})
    response_1 = requests.post(url + 'message/send/v1',
                               json = {'token': login_list[0]['token'],
                                       'channel_id': channel_list[0]['channel_id'],
                                       'message': 'Hello'}).json()
    requests.post(url + 'message/send/v1',
                  json = {'token': login_list[0]['token'],
                          'channel_id': channel_list[0]['channel_id'],
                          'message': 'world!'}).json()
    requests.delete(url + 'message/remove/v1',
                 json = {'token': login_list[1]['token'],
                         'message_id': response_1['message_id']})
    response_3 = requests.get(url + 'channel/messages/v2',
                              params = {'token': login_list[0]['token'],
                                        'channel_id': channel_list[0]['channel_id'],
                                        'start': 0}).json()
    assert response_3['messages'][0]['message'] == 'world!'
    
def test_channel_message_remove_owner_remove_message(login_list, dm_list):
    '''
    
    This test is to test dm owner remove message from other users successfully
    
    Assumption:
        message/senddm/v1 is working well
        dm/messages/v1 is working well 
        
    '''
    requests.post(url + "message/senddm/v1",
                  json = {'token': login_list[0]['token'],
                          'dm_id': dm_list[0]['dm_id'],
                          'message': 'Hello world!'})
    response_1 = requests.post(url + "message/senddm/v1",
                               json = {'token': login_list[1]['token'],
                                       'dm_id': dm_list[0]['dm_id'],
                                       'message': 'Hello world!'}).json()
    response_2 = requests.post(url + "message/senddm/v1",
                               json = {'token': login_list[2]['token'],
                                       'dm_id': dm_list[0]['dm_id'],
                                       'message': 'Steve'}).json()
    requests.delete(url + 'message/remove/v1',
                 json = {'token': login_list[0]['token'],
                         'message_id': response_1['message_id']})
    requests.delete(url + 'message/remove/v1',
                 json = {'token': login_list[0]['token'],
                         'message_id': response_2['message_id']})
    response_3 = requests.get(url + 'dm/messages/v1',
                              params = {'token': login_list[0]['token'],
                                        'dm_id': dm_list[0]['dm_id'],
                                        'start': 0}).json()
    assert response_3['messages'][0]['message'] == 'Hello world!'
    
def test_dm_message_remove_global_owner_cant_remove_message(login_list, dm_list):
    '''
    
    This test is to test when global owner want to remove members' messages in dm
    
    Assumption:
        admin/userpermission/change/v1 is working well
        message/senddm/v1 is working well
    
    Raises: 
        AccessError
        
    '''
    # set user[2] as an owner
    requests.post(url + 'admin/userpermission/change/v1',
                  json = {'token': login_list[0]['token'],
                          'u_id': login_list[2]['auth_user_id'],
                          'permission_id': 1})
    response_1 = requests.post(url + "message/senddm/v1",
                  json = {'token': login_list[3]['token'],
                          'dm_id': dm_list[2]['dm_id'],
                          'message': 'Hello world!'}).json()
    response_2 = requests.delete(url + 'message/remove/v1',
                 json = {'token': login_list[2]['token'],
                         'message_id': response_1['message_id']})
    assert response_2.status_code == AccessError.code

######################################## message/senddm/v1 ########################################

def test_message_senddm_invalid_dm_id(dm_list, login_list):
    '''
    
    Test for input a invalid dm_id
    
    Raises:
        Inputerror
        
    '''
    new_id = random.randint(-65535, 65535)
    invalid_dm_id = []
    while len(invalid_dm_id) < 1:
        if not new_id in [dm_list[i]['dm_id'] for i in range(0,3)]:
            invalid_dm_id.append(new_id)
    response_1 = requests.post(url + 'message/senddm/v1',
                               json = {'token': login_list[0]['token'],
                                       'dm_id': invalid_dm_id[0],
                                       'message': 'Hello world!'})
    assert response_1.status_code == InputError.code
    
def test_message_senddm_empty_message(dm_list, login_list):
    '''
    
    Test for input an empty message
    
    Raises:
        InputError
        
    '''
    response_1 = requests.post(url + 'message/senddm/v1',
                               json = {'token': login_list[0]['token'],
                                       'dm_id': dm_list[0]['dm_id'],
                                       'message': ''})
    assert response_1.status_code == InputError.code
    
def test_message_senddm_too_long_message(dm_list, login_list):
    '''
    
    Test for input more than 1000 characters
    
    Raises:
        InputError
        
    '''
    too_long_message = ""
    while(len(too_long_message) < 1001):
        too_long_message += 'a'
    
    response_1 = requests.post(url + 'message/senddm/v1',
                               json = {'token': login_list[0]['token'],
                                       'dm_id': dm_list[0]['dm_id'],
                                       'message': too_long_message})
    assert response_1.status_code == InputError.code
    
def test_message_senddm_auth_user_out_of_dm(dm_list, login_list):
    '''
    
    This test is test when authorised user is not amember of dm
    
    Raises:
        AccessError
        
    '''
    response_1 = requests.post(url + 'message/senddm/v1',
                               json = {'token': login_list[3]['token'],
                                       'dm_id': dm_list[0]['dm_id'],
                                       'message': "Hello"})
    assert response_1.status_code == AccessError.code
    
def test_message_senddm_invalid_token(dm_list, login_list):
    '''
    
    This test is to test when toke is invalid
    
    Raises:
        AccessError
        
    '''
    # invalid dm id
    new_id = random.randint(-65535, 65535)
    invalid_dm_id = []
    while len(invalid_dm_id) < 1:
        if not new_id in [dm_list[i]['dm_id'] for i in range(0,3)]:
            invalid_dm_id.append(new_id)
    response_1 = requests.post(url + 'message/senddm/v1',
                               json = {'token': -1,
                                       'dm_id': invalid_dm_id[0],
                                       'message': 'Hello world!'})
    assert response_1.status_code == AccessError.code
    
    # invalid message
    response_2 = requests.post(url + 'message/senddm/v1',
                               json = {'token': -1,
                                       'dm_id': dm_list[0]['dm_id'],
                                       'message': ''})
    assert response_2.status_code == AccessError.code
    
    too_long_message = ""
    while(len(too_long_message) < 1001):
        too_long_message += 'a'
    
    response_3 = requests.post(url + 'message/senddm/v1',
                               json = {'token': -1,
                                       'dm_id': dm_list[0]['dm_id'],
                                       'message': too_long_message})
    assert response_3.status_code == AccessError.code

######################################## message/share/v1 ########################################

def test_message_share_in_channel_normal(login_list, channel_list, dm_list):
    '''
    
    This test is to test when everything is going well in channel
    
    Args:
        login_list, channel_list
        
    '''
    # user[1] add user[0] to channel[1]
    requests.post(f"{url}channel/invite/v2",
                  json= {'token': login_list[1]['token'],
                         'channel_id': channel_list[1]['channel_id'],
                         'u_id': login_list[0]['auth_user_id']})
    # user[0] send a msg in channel[0]
    res_1 = requests.post(url + 'message/send/v1',
                  json = {'token': login_list[0]['token'],
                          'channel_id': channel_list[0]['channel_id'],
                          'message': 'Hello guys'}).json()
    # user[0] shares a msg to channel[1] without a new msg
    res_2 = requests.post(url + "message/share/v1",
                          json = {'token': login_list[0]['token'],
                                  'og_message_id': res_1['message_id'],
                                  'message': '',
                                  'channel_id': channel_list[1]['channel_id'],
                                  'dm_id': -1})
    assert res_2.status_code == 200
    # user[0] shares a msg to channel[1] with a new msg
    res_3 = requests.post(url + "message/share/v1",
                          json = {'token': login_list[0]['token'],
                                  'og_message_id': res_1['message_id'],
                                  'message': 'This is Steve @bojinli',
                                  'channel_id': channel_list[1]['channel_id'],
                                  'dm_id': -1})
    assert res_3.status_code == 200
    # user[0] shares a msg from channel[0] to dm[0] with a new msg
    res_4 = requests.post(url + "message/share/v1",
                          json = {'token': login_list[0]['token'],
                                  'og_message_id': res_1['message_id'],
                                  'message': 'This is Steve @cicyzhou',
                                  'channel_id': -1,
                                  'dm_id': dm_list[0]['dm_id']})
    assert res_4.status_code == 200

def test_message_share_in_dm_normal(login_list, dm_list, channel_list):
    '''
    
    This test is to test when everything is going well in dm
    
    Args:
        login_list, dm_list
        
    '''
    # user[0] send a msg in dm[0]
    res_1 = requests.post(url + 'message/senddm/v1',
                  json = {'token': login_list[0]['token'],
                          'dm_id': dm_list[0]['dm_id'],
                          'message': 'Hello guys'}).json()
    # user[0] shares a msg to dm[1] without a new msg
    res_2 = requests.post(url + "message/share/v1",
                          json = {'token': login_list[0]['token'],
                                  'og_message_id': res_1['message_id'],
                                  'message': '',
                                  'channel_id': -1,
                                  'dm_id': dm_list[1]['dm_id']})
    assert res_2.status_code == 200
    # user[0] shares a msg to dm[1] with a new msg
    res_3 = requests.post(url + "message/share/v1",
                          json = {'token': login_list[0]['token'],
                                  'og_message_id': res_1['message_id'],
                                  'message': 'This is Steve @brianlee',
                                  'channel_id': -1,
                                  'dm_id': dm_list[1]['dm_id']})
    assert res_3.status_code == 200
    # user[0] shares a msg from dm[0] to channel[0] with a new msg
    res_4 = requests.post(url + "message/share/v1",
                          json = {'token': login_list[0]['token'],
                                  'og_message_id': res_1['message_id'],
                                  'message': 'This is Steve @steveyang',
                                  'channel_id': channel_list[0]['channel_id'],
                                  'dm_id': -1})
    assert res_4.status_code == 200

def test_message_share_dm_and_channel_id_are_invalid(login_list, dm_list, channel_list):
    '''
    
    This test is to test when both channel_id and dm_id are invalid
    
    Args:
        login_list, dm_list, channel_list
        
    Raises:
        InputError
        
    '''
    # invalid dm_id
    new_id = random.randint(-65535, 65535)
    invalid_dm_id = []
    while len(invalid_dm_id) < 1:
        if not new_id in [dm_list[i]['dm_id'] for i in range(0,3)]:
            invalid_dm_id.append(new_id)
    # invalid channel_id
    new_id = random.randint(-65535, 65535)
    invalid_channel_id = []
    while len(invalid_channel_id) < 1:
        if not new_id in [channel_list[i]['channel_id'] for i in range(0,4)]:
            invalid_channel_id.append(new_id)
    # user[0] send a msg in dm[0]
    res_1 = requests.post(url + 'message/senddm/v1',
                  json = {'token': login_list[0]['token'],
                          'dm_id': dm_list[0]['dm_id'],
                          'message': 'Hello guys'}).json()
    res_2 = requests.post(url + "message/share/v1",
                          json = {'token': login_list[0]['token'],
                                  'og_message_id': res_1['message_id'],
                                  'message': '',
                                  'channel_id': invalid_channel_id[0],
                                  'dm_id': invalid_dm_id[0]})
    res_3 = requests.post(url + "message/share/v1",
                          json = {'token': login_list[0]['token'],
                                  'og_message_id': res_1['message_id'],
                                  'message': 'This is Steve',
                                  'channel_id': invalid_channel_id[0],
                                  'dm_id': invalid_dm_id[0]})
    
    # user[1] add user[0] to channel[1]
    requests.post(f"{url}channel/invite/v2",
                  json= {'token': login_list[1]['token'],
                         'channel_id': channel_list[1]['channel_id'],
                         'u_id': login_list[0]['auth_user_id']})
    # user[0] send a msg in channel[0]
    res_4 = requests.post(url + 'message/send/v1',
                  json = {'token': login_list[0]['token'],
                          'channel_id': channel_list[0]['channel_id'],
                          'message': 'Hello guys'}).json()
    res_5 = requests.post(url + "message/share/v1",
                          json = {'token': login_list[0]['token'],
                                  'og_message_id': res_4['message_id'],
                                  'message': '',
                                  'channel_id': invalid_channel_id[0],
                                  'dm_id': invalid_dm_id[0]})
    res_6 = requests.post(url + "message/share/v1",
                          json = {'token': login_list[0]['token'],
                                  'og_message_id': res_4['message_id'],
                                  'message': 'This is Steve',
                                  'channel_id': invalid_channel_id[0],
                                  'dm_id': invalid_dm_id[0]})
    assert res_2.status_code == InputError.code
    assert res_3.status_code == InputError.code
    assert res_5.status_code == InputError.code
    assert res_6.status_code == InputError.code
    
def test_message_share_no_dm_and_channel_id_is_minus_1(login_list, dm_list, channel_list):
    '''
    
    This test is to test when neither channel_id nor dm_id are -1
    
    Args:
        login_list, dm_list, channel_list
        
    Raises:
        InputError
        
    '''
    res_1 = requests.post(url + 'message/senddm/v1',
                  json = {'token': login_list[0]['token'],
                          'dm_id': dm_list[0]['dm_id'],
                          'message': 'Hello guys'}).json()
    res_2 = requests.post(url + "message/share/v1",
                          json = {'token': login_list[0]['token'],
                                  'og_message_id': res_1['message_id'],
                                  'message': '',
                                  'channel_id': channel_list[1]['channel_id'],
                                  'dm_id': dm_list[1]['dm_id']})
    res_3 = requests.post(url + "message/share/v1",
                          json = {'token': login_list[0]['token'],
                                  'og_message_id': res_1['message_id'],
                                  'message': 'This is Steve',
                                  'channel_id': channel_list[2]['channel_id'],
                                  'dm_id': dm_list[2]['dm_id']})
    
    # user[1] add user[0] to channel[1]
    requests.post(f"{url}channel/invite/v2",
                  json= {'token': login_list[1]['token'],
                         'channel_id': channel_list[1]['channel_id'],
                         'u_id': login_list[0]['auth_user_id']})
    # user[0] send a msg in channel[0]
    res_4 = requests.post(url + 'message/send/v1',
                  json = {'token': login_list[0]['token'],
                          'channel_id': channel_list[0]['channel_id'],
                          'message': 'Hello guys'}).json()
    res_5 = requests.post(url + "message/share/v1",
                          json = {'token': login_list[0]['token'],
                                  'og_message_id': res_4['message_id'],
                                  'message': '',
                                  'channel_id': channel_list[2]['channel_id'],
                                  'dm_id': dm_list[2]['dm_id']})
    res_6 = requests.post(url + "message/share/v1",
                          json = {'token': login_list[0]['token'],
                                  'og_message_id': res_4['message_id'],
                                  'message': 'This is Steve',
                                  'channel_id': channel_list[3]['channel_id'],
                                  'dm_id': dm_list[1]['dm_id']})
    assert res_2.status_code == InputError.code
    assert res_3.status_code == InputError.code
    assert res_5.status_code == InputError.code
    assert res_6.status_code == InputError.code
    
def test_message_share_wrong_message_id(login_list, dm_list, channel_list):
    '''
    
    This test is to test when og_message_id does not refer to a valid message 
    within a channel/DM that the authorised user has joined
    
    Args:
        login_list, dm_list, channel_list
        
    Raises:
        InputError
        
    '''
    ### channel ###
    # user[1] send a msg in channel[1]
    res_1 = requests.post(url + 'message/send/v1',
                  json = {'token': login_list[1]['token'],
                          'channel_id': channel_list[1]['channel_id'],
                          'message': 'Hello guys'}).json()
    # user[0] shares a msg in channel[1] to channel[0] without a new msg, but user[0] 
    # has not joined channel[1]
    res_2 = requests.post(url + "message/share/v1",
                          json = {'token': login_list[0]['token'],
                                  'og_message_id': res_1['message_id'],
                                  'message': '',
                                  'channel_id': channel_list[0]['channel_id'],
                                  'dm_id': -1})
    assert res_2.status_code == InputError.code
    res_2 = requests.post(url + "message/share/v1",
                          json = {'token': login_list[0]['token'],
                                  'og_message_id': -1,
                                  'message': '',
                                  'channel_id': channel_list[0]['channel_id'],
                                  'dm_id': -1})
    assert res_2.status_code == InputError.code
    # user[0] shares a msg in channel[1] to channel[0] with a new msg, but user[0] 
    # has not joined channel[1]
    res_3 = requests.post(url + "message/share/v1",
                          json = {'token': login_list[0]['token'],
                                  'og_message_id': res_1['message_id'],
                                  'message': 'This is Steve',
                                  'channel_id': channel_list[0]['channel_id'],
                                  'dm_id': -1})
    assert res_3.status_code == InputError.code
    
    ### dm ###
    # user[0] send a msg in dm[0]
    res_4 = requests.post(url + 'message/senddm/v1',
                  json = {'token': login_list[0]['token'],
                          'dm_id': dm_list[0]['dm_id'],
                          'message': 'Hello guys'}).json()
    # user[3] shares a msg to dm[2] without a new msg, but user[0] has not joined
    # dm[0]
    res_5 = requests.post(url + "message/share/v1",
                          json = {'token': login_list[3]['token'],
                                  'og_message_id': res_4['message_id'],
                                  'message': '',
                                  'channel_id': -1,
                                  'dm_id': dm_list[2]['dm_id']})
    assert res_5.status_code == InputError.code
    # user[3] shares a msg to dm[2] with a new msg, but user[0] has not joined
    # dm[0]
    res_6 = requests.post(url + "message/share/v1",
                          json = {'token': login_list[3]['token'],
                                  'og_message_id': res_4['message_id'],
                                  'message': 'This is Steve',
                                  'channel_id': -1,
                                  'dm_id': dm_list[2]['dm_id']})
    assert res_6.status_code == InputError.code
    res_6 = requests.post(url + "message/share/v1",
                          json = {'token': login_list[3]['token'],
                                  'og_message_id': -1,
                                  'message': 'This is Steve',
                                  'channel_id': -1,
                                  'dm_id': dm_list[2]['dm_id']})
    assert res_6.status_code == InputError.code
    
def test_message_share_with_too_long_message(login_list, dm_list, channel_list):
    '''
    
    This test is to test when length of message is more than 1000 characters
    
    Args:
        login_list, dm_list, channel_list
        
    Raises:
        InputError
        
    '''
    too_long_message = ''
    while len(too_long_message) <= 1000:
        too_long_message += 'a'
        # user[1] add user[0] to channel[1]
    requests.post(f"{url}channel/invite/v2",
                  json= {'token': login_list[1]['token'],
                         'channel_id': channel_list[1]['channel_id'],
                         'u_id': login_list[0]['auth_user_id']})
    # user[0] send a msg in channel[0]
    res_1 = requests.post(url + 'message/send/v1',
                  json = {'token': login_list[0]['token'],
                          'channel_id': channel_list[0]['channel_id'],
                          'message': 'Hello guys'}).json()
    # user[0] shares a msg to channel[1] with a too long msg
    res_2 = requests.post(url + "message/share/v1",
                          json = {'token': login_list[0]['token'],
                                  'og_message_id': res_1['message_id'],
                                  'message': too_long_message,
                                  'channel_id': channel_list[1]['channel_id'],
                                  'dm_id': -1})
    assert res_2.status_code == InputError.code
    
    # user[0] send a msg in dm[0]
    res_3 = requests.post(url + 'message/senddm/v1',
                  json = {'token': login_list[0]['token'],
                          'dm_id': dm_list[0]['dm_id'],
                          'message': 'Hello guys'}).json()
    # user[0] shares a msg to dm[1] with a too long msg
    res_4 = requests.post(url + "message/share/v1",
                          json = {'token': login_list[0]['token'],
                                  'og_message_id': res_3['message_id'],
                                  'message': too_long_message,
                                  'channel_id': -1,
                                  'dm_id': dm_list[1]['dm_id']})
    assert res_4.status_code == InputError.code
    
def test_message_share_cant_chare_to_not_joined_channel_dm(login_list, dm_list, channel_list):
    '''
    
    This test is to test when the pair of channel_id and dm_id are valid (i.e. one is -1, the other 
    is valid) and the authorised user has not joined the channel or DM they are trying to share the message to
    
    Args:
        login_list, dm_list, channel_list
        
    Raises:
        AccessError
        
    '''
    # user[0] send a msg in channel[0]
    res_1 = requests.post(url + 'message/send/v1',
                  json = {'token': login_list[0]['token'],
                          'channel_id': channel_list[0]['channel_id'],
                          'message': 'Hello guys'}).json()
    # user[0] shares a msg to channel[1] without a new msg, but user[0] didn't 
    # join channel[1]
    res_2 = requests.post(url + "message/share/v1",
                          json = {'token': login_list[0]['token'],
                                  'og_message_id': res_1['message_id'],
                                  'message': '',
                                  'channel_id': channel_list[1]['channel_id'],
                                  'dm_id': -1})
    assert res_2.status_code == AccessError.code
    # user[0] shares a msg to channel[1] with a new msg, but user[0] didn't 
    # join channel[1]
    res_3 = requests.post(url + "message/share/v1",
                          json = {'token': login_list[0]['token'],
                                  'og_message_id': res_1['message_id'],
                                  'message': 'This is Steve',
                                  'channel_id': channel_list[1]['channel_id'],
                                  'dm_id': -1})
    assert res_3.status_code == AccessError.code
    
    # user[0] send a msg in dm[0]
    res_4 = requests.post(url + 'message/senddm/v1',
                  json = {'token': login_list[0]['token'],
                          'dm_id': dm_list[0]['dm_id'],
                          'message': 'Hello guys'}).json()
    # user[0] shares a msg to dm[2] without a new msg, but user[0] didn't join dm[2]
    res_5 = requests.post(url + "message/share/v1",
                          json = {'token': login_list[0]['token'],
                                  'og_message_id': res_4['message_id'],
                                  'message': '',
                                  'channel_id': -1,
                                  'dm_id': dm_list[2]['dm_id']})
    assert res_5.status_code == AccessError.code
    # user[0] shares a msg to dm[2] with a new msg, but user[0] didn't join dm[2]
    res_6 = requests.post(url + "message/share/v1",
                          json = {'token': login_list[0]['token'],
                                  'og_message_id': res_4['message_id'],
                                  'message': 'This is Steve',
                                  'channel_id': -1,
                                  'dm_id': dm_list[2]['dm_id']})
    assert res_6.status_code == AccessError.code
    
def test_message_share_invalid_token(login_list, dm_list, channel_list):
    '''
    
    This test is to test when the authorised user's token is invalid
    
    Args:
        login_list, dm_list, channel_list
        
    Raises:
        AccessError
        
    '''
    # user[1] add user[0] to channel[1]
    requests.post(f"{url}channel/invite/v2",
                  json= {'token': login_list[1]['token'],
                         'channel_id': channel_list[1]['channel_id'],
                         'u_id': login_list[0]['auth_user_id']})
    # user[0] send a msg in channel[0]
    res_1 = requests.post(url + 'message/send/v1',
                  json = {'token': login_list[0]['token'],
                          'channel_id': channel_list[0]['channel_id'],
                          'message': 'Hello guys'}).json()
    # user[0] shares a msg to channel[1] without a new msg
    res_2 = requests.post(url + "message/share/v1",
                          json = {'token': -1,
                                  'og_message_id': res_1['message_id'],
                                  'message': '',
                                  'channel_id': channel_list[1]['channel_id'],
                                  'dm_id': -1})
    assert res_2.status_code == AccessError.code
    # user[0] shares a msg to channel[1] with a new msg
    res_3 = requests.post(url + "message/share/v1",
                          json = {'token': -1,
                                  'og_message_id': res_1['message_id'],
                                  'message': 'This is Steve',
                                  'channel_id': channel_list[1]['channel_id'],
                                  'dm_id': -1})
    assert res_3.status_code == AccessError.code
    
    # user[0] send a msg in dm[0]
    res_4 = requests.post(url + 'message/senddm/v1',
                  json = {'token': login_list[0]['token'],
                          'dm_id': dm_list[0]['dm_id'],
                          'message': 'Hello guys'}).json()
    # user[0] shares a msg to dm[1] without a new msg
    res_5 = requests.post(url + "message/share/v1",
                          json = {'token': -1,
                                  'og_message_id': res_4['message_id'],
                                  'message': '',
                                  'channel_id': -1,
                                  'dm_id': dm_list[1]['dm_id']})
    assert res_5.status_code == AccessError.code
    # user[0] shares a msg to dm[1] with a new msg
    res_6 = requests.post(url + "message/share/v1",
                          json = {'token': -1,
                                  'og_message_id': res_4['message_id'],
                                  'message': 'This is Steve',
                                  'channel_id': -1,
                                  'dm_id': dm_list[1]['dm_id']})
    assert res_6.status_code == AccessError.code

######################################## message/react/v1 ########################################
def test_message_react_invalid_message_id(login_list, channel_list, dm_list):
    '''
    
    This test is to test when message_id is not a valid message within a channel 
    or DM that the authorised user has joined
    
    Args:
        login_list, channel_list, dm_list
        
    Raises:
        InputError
        
    '''
    # user[0] send a msg in channel[0]
    res_1 = requests.post(url + 'message/send/v1',
                        json = {'token': login_list[0]['token'],
                                'channel_id': channel_list[0]['channel_id'],
                                'message': 'Hello guys'}).json()
    # user[0] send a msg in dm[0]
    res_2 = requests.post(url + 'message/senddm/v1',
                        json = {'token': login_list[0]['token'],
                                'dm_id': dm_list[0]['dm_id'],
                                'message': 'Hello guys'}).json()
    res_3 = requests.post(url + 'message/react/v1',
                          json = {'token': login_list[3]['token'],
                                  'message_id': res_1['message_id'],
                                  'react_id': 1})
    res_4 = requests.post(url + 'message/react/v1',
                          json = {'token': login_list[3]['token'],
                                  'message_id': res_2['message_id'],
                                  'react_id': 1})
    res_5 = requests.post(url + 'message/react/v1',
                          json = {'token': login_list[3]['token'],
                                  'message_id': -1,
                                  'react_id': 1})
    res_6 = requests.post(url + 'message/react/v1',
                          json = {'token': login_list[3]['token'],
                                  'message_id': -1,
                                  'react_id': 1})
    assert res_3.status_code == res_4.status_code == InputError.code 
    assert res_5.status_code == res_6.status_code == InputError.code   

def test_message_react_invalid_react_id(login_list, channel_list, dm_list):
    '''
        
    This test is to test when react_id is not a valid react ID-currently,
    the only valid react ID the frontend has is 1
    
    Args:
        login_list, channel_list, dm_list
        
    Raises:
        InputError
        
    '''   
    # user[0] send a msg in channel[0]
    res_1 = requests.post(url + 'message/send/v1',
                        json = {'token': login_list[0]['token'],
                                'channel_id': channel_list[0]['channel_id'],
                                'message': 'Hello guys'}).json()
    # user[0] send a msg in dm[0]
    res_2 = requests.post(url + 'message/senddm/v1',
                        json = {'token': login_list[0]['token'],
                                'dm_id': dm_list[0]['dm_id'],
                                'message': 'Hello guys'}).json()
    res_3 = requests.post(url + 'message/react/v1',
                          json = {'token': login_list[0]['token'],
                                  'message_id': res_1['message_id'],
                                  'react_id': 3})
    res_4 = requests.post(url + 'message/react/v1',
                          json = {'token': login_list[1]['token'],
                                  'message_id': res_2['message_id'],
                                  'react_id': 0})
    assert res_3.status_code == res_4.status_code == InputError.code  
    
def test_message_react_twice(login_list, channel_list, dm_list):
    '''
        
    This test is to test when the message already contains a react 
    with ID react_id from the authorised user
    
    Args:
        login_list, channel_list, dm_list
        
    Raises:
        InputError
        
    '''    
    # user[0] send a msg in channel[0]
    res_1 = requests.post(url + 'message/send/v1',
                        json = {'token': login_list[0]['token'],
                                'channel_id': channel_list[0]['channel_id'],
                                'message': 'Hello guys'}).json()
    # user[0] send a msg in dm[0]
    res_2 = requests.post(url + 'message/senddm/v1',
                        json = {'token': login_list[0]['token'],
                                'dm_id': dm_list[0]['dm_id'],
                                'message': 'Hello guys'}).json()
    requests.post(url + 'message/react/v1',
                          json = {'token': login_list[0]['token'],
                                  'message_id': res_1['message_id'],
                                  'react_id': 1})
    res_3 = requests.post(url + 'message/react/v1',
                          json = {'token': login_list[0]['token'],
                                  'message_id': res_1['message_id'],
                                  'react_id': 1})
    requests.post(url + 'message/react/v1',
                          json = {'token': login_list[1]['token'],
                                  'message_id': res_2['message_id'],
                                  'react_id': 1})
    res_4 = requests.post(url + 'message/react/v1',
                          json = {'token': login_list[1]['token'],
                                  'message_id': res_2['message_id'],
                                  'react_id': 1})
    assert res_3.status_code == res_4.status_code == InputError.code  
    
def test_message_react_invalid_token(login_list, channel_list, dm_list):
    '''
        
    This test is to test when token is invalid
    
    Args:
        login_list, channel_list, dm_list
        
    Raises:
        InputError
        
    '''    
    # user[0] send a msg in channel[0]
    res_1 = requests.post(url + 'message/send/v1',
                        json = {'token': login_list[0]['token'],
                                'channel_id': channel_list[0]['channel_id'],
                                'message': 'Hello guys'}).json()
    # user[0] send a msg in dm[0]
    res_2 = requests.post(url + 'message/senddm/v1',
                        json = {'token': login_list[0]['token'],
                                'dm_id': dm_list[0]['dm_id'],
                                'message': 'Hello guys'}).json()
    res_3 = requests.post(url + 'message/react/v1',
                          json = {'token': -1,
                                  'message_id': res_1['message_id'],
                                  'react_id': 1})
    res_4 = requests.post(url + 'message/react/v1',
                          json = {'token': -1,
                                  'message_id': res_2['message_id'],
                                  'react_id': 0})
    assert res_3.status_code == res_4.status_code == AccessError.code

######################################## message/unreact/v1 ########################################
def test_message_unreact_normal(login_list, channel_list, dm_list):
    '''
    
    This test is to test when user unreact a message successfully
    
    Args:
        login_list, channel_list, dm_list
        
    '''
    # user[0] send a msg in channel[0]
    res_1 = requests.post(url + 'message/send/v1',
                        json = {'token': login_list[0]['token'],
                                'channel_id': channel_list[0]['channel_id'],
                                'message': 'Hello guys @brianlee'}).json()
    # user[0] send a msg in dm[0]
    res_2 = requests.post(url + 'message/senddm/v1',
                        json = {'token': login_list[0]['token'],
                                'dm_id': dm_list[0]['dm_id'],
                                'message': 'Hello guys @cicyzhou'}).json()
    requests.post(url + 'message/react/v1',
                          json = {'token': login_list[0]['token'],
                                  'message_id': res_1['message_id'],
                                  'react_id': 1})
    res_3 = requests.post(url + 'message/unreact/v1',
                          json = {'token': login_list[0]['token'],
                                  'message_id': res_1['message_id'],
                                  'react_id': 1})
    requests.post(url + 'message/react/v1',
                          json = {'token': login_list[1]['token'],
                                  'message_id': res_2['message_id'],
                                  'react_id': 1})
    res_4 = requests.post(url + 'message/unreact/v1',
                          json = {'token': login_list[1]['token'],
                                  'message_id': res_2['message_id'],
                                  'react_id': 1})
    assert res_3.status_code == 200
    assert res_4.status_code == 200
    
def test_message_unreact_invalid_message_id(login_list, channel_list, dm_list):
    '''
    
    This test is to test when message_id is not a valid message within a channel 
    or DM that the authorised user has joined
    
    Args:
        login_list, channel_list, dm_list
        
    '''
    # user[1] send a msg in channel[1]
    res_1 = requests.post(url + 'message/send/v1',
                        json = {'token': login_list[1]['token'],
                                'channel_id': channel_list[1]['channel_id'],
                                'message': 'Hello guys'}).json()
    # user[2] send a msg in dm[2]
    res_2 = requests.post(url + 'message/senddm/v1',
                        json = {'token': login_list[2]['token'],
                                'dm_id': dm_list[2]['dm_id'],
                                'message': 'Hello guys'}).json()
    res_3 = requests.post(url + 'message/unreact/v1',
                          json = {'token': login_list[0]['token'],
                                  'message_id': res_1['message_id'],
                                  'react_id': 1})
    res_4 = requests.post(url + 'message/unreact/v1',
                          json = {'token': login_list[0]['token'],
                                  'message_id': res_2['message_id'],
                                  'react_id': 1})
    assert res_3.status_code == InputError.code
    assert res_4.status_code == InputError.code
    res_5 = requests.post(url + 'message/unreact/v1',
                          json = {'token': login_list[0]['token'],
                                  'message_id': -1,
                                  'react_id': 1})
    res_6 = requests.post(url + 'message/unreact/v1',
                          json = {'token': login_list[0]['token'],
                                  'message_id': -2,
                                  'react_id': 1})
    assert res_5.status_code == InputError.code
    assert res_6.status_code == InputError.code
    
def test_message_unreact_invalid_react_id(login_list, channel_list, dm_list):
    '''
    
    This test is to test when react_id is not a valid react ID
    
    Args:
        login_list, channel_list, dm_list
        
    '''
    # user[0] send a msg in channel[0]
    res_1 = requests.post(url + 'message/send/v1',
                        json = {'token': login_list[0]['token'],
                                'channel_id': channel_list[0]['channel_id'],
                                'message': 'Hello guys'}).json()
    # user[0] send a msg in dm[0]
    res_2 = requests.post(url + 'message/senddm/v1',
                        json = {'token': login_list[0]['token'],
                                'dm_id': dm_list[0]['dm_id'],
                                'message': 'Hello guys'}).json()
    requests.post(url + 'message/react/v1',
                          json = {'token': login_list[0]['token'],
                                  'message_id': res_1['message_id'],
                                  'react_id': 1})
    res_3 = requests.post(url + 'message/unreact/v1',
                          json = {'token': login_list[0]['token'],
                                  'message_id': res_1['message_id'],
                                  'react_id': 2})
    requests.post(url + 'message/react/v1',
                          json = {'token': login_list[1]['token'],
                                  'message_id': res_2['message_id'],
                                  'react_id': 1})
    res_4 = requests.post(url + 'message/unreact/v1',
                          json = {'token': login_list[1]['token'],
                                  'message_id': res_2['message_id'],
                                  'react_id': -1})
    assert res_3.status_code == res_4.status_code == InputError.code
    
def test_message_unreact_no_react_message(login_list, channel_list, dm_list):
    '''
    
    This test is to test when the message does not contain a react with ID 
    react_id from the authorised use
    
    Args:
        login_list, channel_list, dm_list
        
    '''
    # user[0] send a msg in channel[0]
    res_1 = requests.post(url + 'message/send/v1',
                        json = {'token': login_list[0]['token'],
                                'channel_id': channel_list[0]['channel_id'],
                                'message': 'Hello guys'}).json()
    # user[0] send a msg in dm[0]
    res_2 = requests.post(url + 'message/senddm/v1',
                        json = {'token': login_list[0]['token'],
                                'dm_id': dm_list[0]['dm_id'],
                                'message': 'Hello guys'}).json()
    res_3 = requests.post(url + 'message/unreact/v1',
                          json = {'token': login_list[0]['token'],
                                  'message_id': res_1['message_id'],
                                  'react_id': 1})
    res_4 = requests.post(url + 'message/unreact/v1',
                          json = {'token': login_list[1]['token'],
                                  'message_id': res_2['message_id'],
                                  'react_id': 1})
    assert res_3.status_code == InputError.code
    assert res_4.status_code == InputError.code

def test_message_unreact_invalid_token(login_list, channel_list, dm_list):
    '''
    
    This test is to test when user unreact a message successfully
    
    Args:
        login_list, channel_list, dm_list
        
    '''
    # user[0] send a msg in channel[0]
    res_1 = requests.post(url + 'message/send/v1',
                        json = {'token': login_list[0]['token'],
                                'channel_id': channel_list[0]['channel_id'],
                                'message': 'Hello guys'}).json()
    # user[0] send a msg in dm[0]
    res_2 = requests.post(url + 'message/senddm/v1',
                        json = {'token': login_list[0]['token'],
                                'dm_id': dm_list[0]['dm_id'],
                                'message': 'Hello guys'}).json()
    requests.post(url + 'message/react/v1',
                          json = {'token': login_list[0]['token'],
                                  'message_id': res_1['message_id'],
                                  'react_id': 1})
    res_3 = requests.post(url + 'message/unreact/v1',
                          json = {'token': -1,
                                  'message_id': res_1['message_id'],
                                  'react_id': 1})
    requests.post(url + 'message/react/v1',
                          json = {'token': login_list[1]['token'],
                                  'message_id': res_2['message_id'],
                                  'react_id': 1})
    res_4 = requests.post(url + 'message/unreact/v1',
                          json = {'token': -1,
                                  'message_id': res_2['message_id'],
                                  'react_id': 1})
    assert res_3.status_code == AccessError.code
    assert res_4.status_code == AccessError.code

######################################## message/pin/v1 ########################################
def test_message_pin_normal(login_list, channel_list, dm_list):
    '''
    
    This test is to test when user pin a message successfully
    
    Args:
        login_list, channel_list, dm_list
        
    '''
    # user[0] send a msg in channel[0]
    res_1 = requests.post(url + 'message/send/v1',
                        json = {'token': login_list[0]['token'],
                                'channel_id': channel_list[0]['channel_id'],
                                'message': 'Hello guys'}).json()
    # user[0] send a msg in dm[0]
    res_2 = requests.post(url + 'message/senddm/v1',
                        json = {'token': login_list[0]['token'],
                                'dm_id': dm_list[0]['dm_id'],
                                'message': 'Hello guys'}).json()
    res_3 = requests.post(url + 'message/pin/v1',
                          json = {'token': login_list[0]['token'],
                                  'message_id': res_1['message_id']})
    res_4 = requests.post(url + 'message/pin/v1',
                          json = {'token': login_list[0]['token'],
                                  'message_id': res_2['message_id']})
    assert res_3.status_code == res_4.status_code == 200
    res_5 = requests.get(url + 'channel/messages/v2',
                         params = {'token': login_list[0]['token'],
                                  'channel_id': channel_list[0]['channel_id'],
                                  'start': 0}).json()
    res_6 = requests.get(url + 'dm/messages/v1',
                         params = {'token': login_list[0]['token'],
                                   'dm_id': dm_list[0]['dm_id'],
                                   'start': 0}).json()
    assert res_5['messages'][0]['is_pinned'] == True
    assert res_6['messages'][0]['is_pinned'] == True

def test_message_pin_invalid_message_id(login_list, channel_list, dm_list):
    '''
    
    This test is to test when message_id is not a valid message within a 
    channel or DM that the authorised user has joined
    
    Args:
        login_list, channel_list, dm_list
        
    Raises:
        InputError
        
    '''
    # user[0] send a msg in channel[0]
    res_1 = requests.post(url + 'message/send/v1',
                        json = {'token': login_list[0]['token'],
                                'channel_id': channel_list[0]['channel_id'],
                                'message': 'Hello guys'}).json()
    # user[0] send a msg in dm[0]
    res_2 = requests.post(url + 'message/senddm/v1',
                        json = {'token': login_list[0]['token'],
                                'dm_id': dm_list[0]['dm_id'],
                                'message': 'Hello guys'}).json()
    res_3 = requests.post(url + 'message/pin/v1',
                          json = {'token': login_list[1]['token'],
                                  'message_id': res_1['message_id']})
    res_4 = requests.post(url + 'message/pin/v1',
                          json = {'token': login_list[3]['token'],
                                  'message_id': res_2['message_id']})
    assert res_3.status_code == res_4.status_code == InputError.code
    res_5 = requests.post(url + 'message/pin/v1',
                          json = {'token': login_list[1]['token'],
                                  'message_id': -1})
    res_6 = requests.post(url + 'message/pin/v1',
                          json = {'token': login_list[3]['token'],
                                  'message_id': -2})
    assert res_5.status_code == res_6.status_code == InputError.code
    
def test_message_pin_twice(login_list, channel_list, dm_list):
    '''
    
    This test is to test when the message is already pinned
    
    Args:
        login_list, channel_list, dm_list
        
    Raises:
        InputError
        
    '''
    # user[0] send a msg in channel[0]
    res_1 = requests.post(url + 'message/send/v1',
                        json = {'token': login_list[0]['token'],
                                'channel_id': channel_list[0]['channel_id'],
                                'message': 'Hello guys'}).json()
    # user[0] send a msg in dm[0]
    res_2 = requests.post(url + 'message/senddm/v1',
                        json = {'token': login_list[0]['token'],
                                'dm_id': dm_list[0]['dm_id'],
                                'message': 'Hello guys'}).json()
    requests.post(url + 'message/pin/v1',
                          json = {'token': login_list[0]['token'],
                                  'message_id': res_1['message_id']})
    res_3 = requests.post(url + 'message/pin/v1',
                          json = {'token': login_list[0]['token'],
                                  'message_id': res_1['message_id']})
    requests.post(url + 'message/pin/v1',
                          json = {'token': login_list[0]['token'],
                                  'message_id': res_2['message_id']})
    res_4 = requests.post(url + 'message/pin/v1',
                          json = {'token': login_list[0]['token'],
                                  'message_id': res_2['message_id']})
    assert res_3.status_code == res_4.status_code == InputError.code
    
def test_message_pin_no_permission(login_list, channel_list, dm_list):
    '''
    
    This test is to test when message_id refers to a valid message in a 
    joined channel/DM and the authorised user does not have owner permissions 
    in the channel/DM
    
    Args:
        login_list, channel_list, dm_list
        
    Raises:
        AccessError
        
    '''
    # user[0] add user[1] to channel[0]
    requests.post(f"{url}channel/invite/v2",
                  json= {'token': login_list[0]['token'],
                         'channel_id': channel_list[0]['channel_id'],
                         'u_id': login_list[1]['auth_user_id']})
    # user[1] send a msg in channel[0]
    res_1 = requests.post(url + 'message/send/v1',
                        json = {'token': login_list[1]['token'],
                                'channel_id': channel_list[0]['channel_id'],
                                'message': 'Hello guys'}).json()
    # user[1] send a msg in dm[0]
    res_2 = requests.post(url + 'message/senddm/v1',
                        json = {'token': login_list[1]['token'],
                                'dm_id': dm_list[0]['dm_id'],
                                'message': 'Hello guys'}).json()
    res_3 = requests.post(url + 'message/pin/v1',
                          json = {'token': login_list[1]['token'],
                                  'message_id': res_1['message_id']})
    res_4 = requests.post(url + 'message/pin/v1',
                          json = {'token': login_list[1]['token'],
                                  'message_id': res_2['message_id']})
    assert res_3.status_code == res_4.status_code == AccessError.code
    
def test_message_pin_invalid_token(login_list, channel_list, dm_list):
    '''
    
    This test is to test when token is invalid
    
    Args:
        login_list, channel_list, dm_list
        
    Raises:
        AccessError
        
    '''
    # user[0] send a msg in channel[0]
    res_1 = requests.post(url + 'message/send/v1',
                        json = {'token': login_list[0]['token'],
                                'channel_id': channel_list[0]['channel_id'],
                                'message': 'Hello guys'}).json()
    # user[0] send a msg in dm[0]
    res_2 = requests.post(url + 'message/senddm/v1',
                        json = {'token': login_list[0]['token'],
                                'dm_id': dm_list[0]['dm_id'],
                                'message': 'Hello guys'}).json()
    res_3 = requests.post(url + 'message/pin/v1',
                          json = {'token': -1,
                                  'message_id': res_1['message_id']})
    res_4 = requests.post(url + 'message/pin/v1',
                          json = {'token': -1,
                                  'message_id': res_2['message_id']})
    assert res_3.status_code == AccessError.code
    assert res_4.status_code == AccessError.code

######################################## message/pin/v1 ########################################
def test_message_unpin_normal(login_list, channel_list, dm_list):
    '''
    
    This test is to test when user unpin a message successfully
    
    Args:
        login_list, channel_list, dm_list
        
    '''
    # user[0] send a msg in channel[0]
    res_1 = requests.post(url + 'message/send/v1',
                        json = {'token': login_list[0]['token'],
                                'channel_id': channel_list[0]['channel_id'],
                                'message': 'Hello guys'}).json()
    # user[0] send a msg in dm[0]
    res_2 = requests.post(url + 'message/senddm/v1',
                        json = {'token': login_list[0]['token'],
                                'dm_id': dm_list[0]['dm_id'],
                                'message': 'Hello guys'}).json()
    requests.post(url + 'message/pin/v1',
                  json = {'token': login_list[0]['token'],
                          'message_id': res_1['message_id']})
    requests.post(url + 'message/pin/v1',
                  json = {'token': login_list[0]['token'],
                          'message_id': res_2['message_id']})
    res_3 = requests.post(url + 'message/unpin/v1',
                          json = {'token': login_list[0]['token'],
                                  'message_id': res_1['message_id']})
    res_4 = requests.post(url + 'message/unpin/v1',
                          json = {'token': login_list[0]['token'],
                                  'message_id': res_2['message_id']})
    assert res_3.status_code == res_4.status_code == 200
    res_5 = requests.get(url + 'channel/messages/v2',
                         params = {'token': login_list[0]['token'],
                                  'channel_id': channel_list[0]['channel_id'],
                                  'start': 0}).json()
    res_6 = requests.get(url + 'dm/messages/v1',
                         params = {'token': login_list[0]['token'],
                                   'dm_id': dm_list[0]['dm_id'],
                                   'start': 0}).json()
    assert res_5['messages'][0]['is_pinned'] == False
    assert res_6['messages'][0]['is_pinned'] == False

def test_message_unpin_invalid_message_id(login_list, channel_list, dm_list):
    '''
    
    This test is to test when message_id is not a valid message within a channel 
    or DM that the authorised user has joined
    
    Args:
        login_list, channel_list, dm_list
        
    Raises:
        InputError
        
    '''
    # user[0] send a msg in channel[0]
    res_1 = requests.post(url + 'message/send/v1',
                        json = {'token': login_list[0]['token'],
                                'channel_id': channel_list[0]['channel_id'],
                                'message': 'Hello guys'}).json()
    # user[0] send a msg in dm[0]
    res_2 = requests.post(url + 'message/senddm/v1',
                        json = {'token': login_list[0]['token'],
                                'dm_id': dm_list[0]['dm_id'],
                                'message': 'Hello guys'}).json()
    requests.post(url + 'message/pin/v1',
                  json = {'token': login_list[0]['token'],
                          'message_id': res_1['message_id']})
    requests.post(url + 'message/pin/v1',
                  json = {'token': login_list[0]['token'],
                          'message_id': res_2['message_id']})
    res_3 = requests.post(url + 'message/unpin/v1',
                          json = {'token': login_list[1]['token'],
                                  'message_id': res_1['message_id']})
    res_4 = requests.post(url + 'message/unpin/v1',
                          json = {'token': login_list[3]['token'],
                                  'message_id': res_2['message_id']})
    assert res_3.status_code == res_4.status_code == InputError.code
    res_5 = requests.post(url + 'message/unpin/v1',
                          json = {'token': login_list[1]['token'],
                                  'message_id': -1})
    res_6 = requests.post(url + 'message/unpin/v1',
                          json = {'token': login_list[3]['token'],
                                  'message_id': -2})
    assert res_5.status_code == res_6.status_code == InputError.code

def test_message_unpin_not_pinned_message(login_list, channel_list, dm_list):
    '''
    
    This test is to test when the message is not already pinned
    
    Args:
        login_list, channel_list, dm_list
        
    Raises:
        InputError
        
    '''
    # user[0] send a msg in channel[0]
    res_1 = requests.post(url + 'message/send/v1',
                        json = {'token': login_list[0]['token'],
                                'channel_id': channel_list[0]['channel_id'],
                                'message': 'Hello guys'}).json()
    # user[0] send a msg in dm[0]
    res_2 = requests.post(url + 'message/senddm/v1',
                        json = {'token': login_list[0]['token'],
                                'dm_id': dm_list[0]['dm_id'],
                                'message': 'Hello guys'}).json()
    res_3 = requests.post(url + 'message/unpin/v1',
                          json = {'token': login_list[0]['token'],
                                  'message_id': res_1['message_id']})
    res_4 = requests.post(url + 'message/unpin/v1',
                          json = {'token': login_list[0]['token'],
                                  'message_id': res_2['message_id']})
    assert res_3.status_code == res_4.status_code == InputError.code

def test_message_unpin_no_permission(login_list, channel_list, dm_list):
    '''
    
    This test is to test when message_id refers to a valid message in a 
    joined channel/DM and the authorised user does not have owner permissions 
    in the channel/DM
    
    Args:
        login_list, channel_list, dm_list
        
    Raises:
        AccessError
        
    '''
    # user[0] add user[1] to channel[0]
    requests.post(f"{url}channel/invite/v2",
                  json= {'token': login_list[0]['token'],
                         'channel_id': channel_list[0]['channel_id'],
                         'u_id': login_list[1]['auth_user_id']})
    # user[1] send a msg in channel[0]
    res_1 = requests.post(url + 'message/send/v1',
                        json = {'token': login_list[1]['token'],
                                'channel_id': channel_list[0]['channel_id'],
                                'message': 'Hello guys'}).json()
    # user[1] send a msg in dm[0]
    res_2 = requests.post(url + 'message/senddm/v1',
                        json = {'token': login_list[1]['token'],
                                'dm_id': dm_list[0]['dm_id'],
                                'message': 'Hello guys'}).json()
    requests.post(url + 'message/pin/v1',
                  json = {'token': login_list[0]['token'],
                          'message_id': res_1['message_id']})
    requests.post(url + 'message/pin/v1',
                  json = {'token': login_list[0]['token'],
                          'message_id': res_2['message_id']})
    res_3 = requests.post(url + 'message/unpin/v1',
                          json = {'token': login_list[1]['token'],
                                  'message_id': res_1['message_id']})
    res_4 = requests.post(url + 'message/unpin/v1',
                          json = {'token': login_list[1]['token'],
                                  'message_id': res_2['message_id']})
    assert res_3.status_code == res_4.status_code == AccessError.code
    
def test_message_unpin_invalid_token(login_list, channel_list, dm_list):
    '''
    
    This test is to test when token is invalid
    
    Args:
        login_list, channel_list, dm_list
        
    Raises:
        AccessError
        
    '''
    # user[0] send a msg in channel[0]
    res_1 = requests.post(url + 'message/send/v1',
                        json = {'token': login_list[0]['token'],
                                'channel_id': channel_list[0]['channel_id'],
                                'message': 'Hello guys'}).json()
    # user[0] send a msg in dm[0]
    res_2 = requests.post(url + 'message/senddm/v1',
                        json = {'token': login_list[0]['token'],
                                'dm_id': dm_list[0]['dm_id'],
                                'message': 'Hello guys'}).json()
    requests.post(url + 'message/pin/v1',
                  json = {'token': login_list[0]['token'],
                          'message_id': res_1['message_id']})
    requests.post(url + 'message/pin/v1',
                  json = {'token': login_list[0]['token'],
                          'message_id': res_2['message_id']})
    res_3 = requests.post(url + 'message/unpin/v1',
                          json = {'token': -1,
                                  'message_id': res_1['message_id']})
    res_4 = requests.post(url + 'message/unpin/v1',
                          json = {'token': -1,
                                  'message_id': res_2['message_id']})
    assert res_3.status_code == AccessError.code
    assert res_4.status_code == AccessError.code

######################################## message/sendlater/v1 ########################################
def timestamp():
    '''
    
    This is a helper function
    
    '''
    # today = date.today()
    # dt = datetime(today.year, today.month, today.day)
    # timestamp = dt.replace(tzinfo=timezone.utc).timestamp()
    timestamp = int(time.time())
    return timestamp

def test_message_sendlater_normal(login_list, channel_list):
    '''
    
    This test is to test when user sends a later message successfully
    
    Args:
        login_list, channel_list
        
    '''
    # user[0] sends a later message in channel[0], 1s later
    requests.post(url + 'message/sendlater/v1', 
                  json={'token': login_list[0]['token'],
                        'channel_id': channel_list[0]['channel_id'],
                        'message': 'I am SuperBoy @steveyang',
                        'time_sent': timestamp()+10})
    res_1 = requests.get(url + 'channel/messages/v2', 
                         params = {'token': login_list[0]['token'],
                                   'channel_id': channel_list[0]['channel_id'],
                                   'start': 0}).json()
    assert len(res_1['messages']) == 0
    time.sleep(10.1)
    res_2 = requests.get(url + 'channel/messages/v2', 
                         params = {'token': login_list[0]['token'],
                                   'channel_id': channel_list[0]['channel_id'],
                                   'start': 0}).json()
    assert len(res_2['messages']) == 1
    response_6 = requests.get(url + 'notifications/get/v1',
                              params={'token': login_list[0]['token']}).json()
    assert response_6['notifications'][0]['channel_id'] == channel_list[0]['channel_id']
    assert response_6['notifications'][0]['dm_id'] == -1
    assert response_6['notifications'][0]['notification_message'] == "steveyang tagged you in Steve's channel: I am SuperBoy @steve"
    requests.post(url + 'message/sendlater/v1', 
                  json={'token': login_list[0]['token'],
                        'channel_id': channel_list[0]['channel_id'],
                        'message': 'I am SuperBoy @cicyzhou',
                        'time_sent': timestamp()+1})
    time.sleep(1.1)
    response_7 = requests.get(url + 'notifications/get/v1',
                              params={'token': login_list[3]['token']}).json()
    assert response_7['notifications'] == []
    
def test_message_sendlater_invalid_channel_id(login_list, channel_list):
    '''
    
    This test is to test when channel_id does not refer to a valid channel
    
    Args:
        login_list, channel_list
        
    Raises:
        InputError
        
    '''
    new_id = random.randint(-65535, 65535)
    invalid_channel_id = []
    while len(invalid_channel_id) < 1:
        if not new_id in [channel_list[i]['channel_id'] for i in range(0,4)]:
            invalid_channel_id.append(new_id)
    res_1 = requests.post(url + 'message/sendlater/v1', 
                          json={'token': login_list[0]['token'],
                                'channel_id': invalid_channel_id[0],
                                'message': 'I am SuperBoy',
                                'time_sent': timestamp()+1})
    assert res_1.status_code == InputError.code
    
def test_message_sendlater_invalid_message(login_list, channel_list):
    '''
    
    This test is to test when length of message is less than 1 or over 1000
    characters
    
    Args:
        login_list, channel_list
        
    Raises:
        InputError
        
    '''
    empty_message = ''
    too_long_message = ''
    while len(too_long_message) <= 1000:
        too_long_message += 'a'
    res_1 = requests.post(url + 'message/sendlater/v1', 
                          json={'token': login_list[0]['token'],
                                'channel_id': channel_list[0]['channel_id'],
                                'message': empty_message,
                                'time_sent': timestamp()+1})
    res_2 = requests.post(url + 'message/sendlater/v1', 
                          json={'token': login_list[0]['token'],
                                'channel_id': channel_list[0]['channel_id'],
                                'message': too_long_message,
                                'time_sent': timestamp()+1})
    assert res_1.status_code == res_2.status_code == InputError.code
    
def test_message_sendlater_send_past(login_list, channel_list):
    '''
    
    This test is to test when time_sent is a time in the past
    
    Args:
        login_list, channel_list
        
    Raises:
        InputError
        
    '''
    res_1 = requests.post(url + 'message/sendlater/v1', 
                          json={'token': login_list[0]['token'],
                                'channel_id': channel_list[0]['channel_id'],
                                'message': "Hello world",
                                'time_sent': timestamp()-1})
    assert res_1.status_code == InputError.code
    
def test_message_sendlater_invalid_auth_user(login_list, channel_list):
    '''
    
    This test is to test when channel_id is valid and the authorised user 
    is not a member of the channel they are trying to post to
    
    Args:
        login_list, channel_list
        
    Raises:
        AccessError
        
    '''
    res_1 = requests.post(url + 'message/sendlater/v1', 
                          json={'token': login_list[1]['token'],
                                'channel_id': channel_list[0]['channel_id'],
                                'message': "Hello world",
                                'time_sent': timestamp()+1})
    assert res_1.status_code == AccessError.code
    
def test_message_sendlater_invalid_token(login_list, channel_list):
    '''
    
    This test is to test when token is invalid
    
    Args:
        login_list, channel_list
        
    Raises:
        AccessError
        
    '''
    res_1 = requests.post(url + 'message/sendlater/v1', 
                          json={'token': -1,
                                'channel_id': channel_list[0]['channel_id'],
                                'message': "Hello world",
                                'time_sent': timestamp()+1})
    assert res_1.status_code == AccessError.code
    
######################################## message/sendlaterdm/v1 ########################################
def test_message_sendlaterdm_normal(login_list, dm_list):
    '''
    
    This test is to test when user sends a later message successfully
    
    Args:
        login_list, dm_list
        
    '''
    # user[0] sends a later message in dm[0], 1s later
    requests.post(url + 'message/sendlaterdm/v1', 
                  json={'token': login_list[0]['token'],
                        'dm_id': dm_list[0]['dm_id'],
                        'message': 'I am SuperBoy @steveyang',
                        'time_sent': timestamp()+10})
    res_1 = requests.get(url + 'dm/messages/v1', 
                         params = {'token': login_list[0]['token'],
                                   'dm_id': dm_list[0]['dm_id'],
                                   'start': 0}).json()
    assert len(res_1['messages']) == 0
    time.sleep(10.1)
    res_2 = requests.get(url + 'dm/messages/v1', 
                         params = {'token': login_list[0]['token'],
                                   'dm_id': dm_list[0]['dm_id'],
                                   'start': 0}).json()
    assert len(res_2['messages']) == 1
    response_6 = requests.get(url + 'notifications/get/v1',
                              params={'token': login_list[0]['token']}).json()
    assert response_6['notifications'][0]['dm_id'] == dm_list[0]['dm_id']
    assert response_6['notifications'][0]['channel_id'] == -1
    assert response_6['notifications'][0]['notification_message'] == "steveyang tagged you in bojinli, brianlee, steveyang: I am SuperBoy @steve"
    requests.post(url + 'message/sendlaterdm/v1', 
                  json={'token': login_list[0]['token'],
                        'dm_id': dm_list[0]['dm_id'],
                        'message': 'I am SuperBoy @cicyzhou',
                        'time_sent': timestamp()+1})
    time.sleep(1.1)
    response_7 = requests.get(url + 'notifications/get/v1',
                              params={'token': login_list[3]['token']}).json()
    assert len(response_7['notifications']) == 2 # only 2 add notification
    
def test_message_sendlaterdm_invalid_dm_id(login_list, dm_list):
    '''
    
    This test is to test when dm_id does not refer to a valid dm
    
    Args:
        login_list, dm_list
        
    Raises:
        InputError
        
    '''
    new_id = random.randint(-65535, 65535)
    invalid_dm_id = []
    while len(invalid_dm_id) < 1:
        if not new_id in [dm_list[i]['dm_id'] for i in range(0,3)]:
            invalid_dm_id.append(new_id)
    res_1 = requests.post(url + 'message/sendlaterdm/v1', 
                          json={'token': login_list[0]['token'],
                                'dm_id': invalid_dm_id[0],
                                'message': 'I am SuperBoy',
                                'time_sent': timestamp()+1})
    assert res_1.status_code == InputError.code
    
def test_message_sendlaterdm_invalid_message(login_list, dm_list):
    '''
    
    This test is to test when length of message is less than 1 or over 1000
    characters
    
    Args:
        login_list, dm_list
        
    Raises:
        InputError
        
    '''
    empty_message = ''
    too_long_message = ''
    while len(too_long_message) <= 1000:
        too_long_message += 'a'
    res_1 = requests.post(url + 'message/sendlaterdm/v1', 
                          json={'token': login_list[0]['token'],
                                'dm_id': dm_list[0]['dm_id'],
                                'message': empty_message,
                                'time_sent': timestamp()+1})
    res_2 = requests.post(url + 'message/sendlaterdm/v1', 
                          json={'token': login_list[0]['token'],
                                'dm_id': dm_list[0]['dm_id'],
                                'message': too_long_message,
                                'time_sent': timestamp()+1})
    assert res_1.status_code == res_2.status_code == InputError.code
    
def test_message_sendlaterdm_send_past(login_list, dm_list):
    '''
    
    This test is to test when time_sent is a time in the past
    
    Args:
        login_list, dm_list
        
    Raises:
        InputError
        
    '''
    res_1 = requests.post(url + 'message/sendlaterdm/v1', 
                          json={'token': login_list[0]['token'],
                                'dm_id': dm_list[0]['dm_id'],
                                'message': "Hello world",
                                'time_sent': timestamp()-1})
    assert res_1.status_code == InputError.code
    
def test_message_sendlaterdm_invalid_auth_user(login_list, dm_list):
    '''
    
    This test is to test when dm_id is valid and the authorised user 
    is not a member of the dm they are trying to post to
    
    Args:
        login_list, dm_list
        
    Raises:
        AccessError
        
    '''
    res_1 = requests.post(url + 'message/sendlaterdm/v1', 
                          json={'token': login_list[3]['token'],
                                'dm_id': dm_list[0]['dm_id'],
                                'message': "Hello world",
                                'time_sent': timestamp()+1})
    assert res_1.status_code == AccessError.code
    
def test_message_sendlaterdm_invalid_token(login_list, dm_list):
    '''
    
    This test is to test when token is invalid
    
    Args:
        login_list, dm_list
        
    Raises:
        AccessError
        
    '''
    res_1 = requests.post(url + 'message/sendlaterdm/v1', 
                          json={'token': -1,
                                'dm_id': dm_list[0]['dm_id'],
                                'message': "Hello world",
                                'time_sent': timestamp()+1})
    assert res_1.status_code == AccessError.code
    
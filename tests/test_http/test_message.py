from urllib import response
import pytest
import requests
import json
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
                                              'is_public': False}).json())
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
                                         'u_ids': [login_list[1]['auth_user_id'], login_list[2]['auth_user_id']]}).json())
    
    # dm_list[1]: user[0], user[2]. user[3]
    dm_list.append(requests.post(url + "dm/create/v1",
                                 json = {'token': login_list[0]['token'],
                                         'u_ids': [login_list[3]['auth_user_id'], login_list[2]['auth_user_id']]}).json())
    
    # dm_list[2]: user[1], user[2]. user[3]
    dm_list.append(requests.post(url + "dm/create/v1",
                                 json = {'token': login_list[1]['token'],
                                         'u_ids': [login_list[2]['auth_user_id'], login_list[3]['auth_user_id']]}).json())
    
    return dm_list

######################################## Test_message_send_v1 ########################################

def test_message_send_invalid_channel_id(user_list, channel_list, login_list):
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
    
def test_message_send_empty_message(user_list, channel_list, login_list):
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
    
def test_message_send_too_long_message(user_list, channel_list, login_list):
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
    
def test_message_send_auth_user_out_of_channel(user_list, channel_list, login_list):
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
    
def test_message_send_invalid_token(user_list, channel_list, login_list):
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

def test_channel_message_edit_normal(user_list, login_list, channel_list):
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
                          'message': 'Hello world!'}).json()
    
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
    
def test_dm_message_edit_normal(user_list, login_list, dm_list):
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
    
def test_channel_message_edit_too_long_message(user_list, login_list, channel_list):
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
    
def test_dm_message_edit_too_long_message(user_list, login_list, dm_list):
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
    
def test_channel_message_edit_wrong_message_id(user_list, login_list, channel_list):
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
      
def test_dm_message_edit_wrong_message_id(user_list, login_list, dm_list):
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
    
def test_message_edit_channel_invalid_user(user_list, login_list, channel_list):
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
    
def test_message_edit_dm_invalid_user(user_list, login_list, dm_list):
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
    
def test_channel_message_edit_owner_edit_message(user_list, login_list, channel_list):
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
    
def test_dm_message_edit_owner_edit_message(user_list, login_list, dm_list):
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
    
######################################## message/remove/v1 ########################################

def test_channel_message_remove_normal(user_list, login_list, channel_list):
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
    
def test_dm_message_remove_normal(user_list, login_list, dm_list):
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
    
def test_channel_message_remove_invalid_message_id(user_list, login_list, channel_list):
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
    
def test_dm_message_remove_invalid_message_id(user_list, login_list, dm_list):
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

def test_channel_message_remove_invalid_user(user_list, login_list, channel_list):
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
    
def test_message_remove_dm_invalid_user(user_list, login_list, dm_list):
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
    
def test_message_remove_owner_remove_message(user_list, login_list, channel_list):
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
    
def test_channel_message_remove_owner_remove_message(user_list, login_list, dm_list):
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

######################################## message/senddm/v1 ########################################

def test_message_senddm_invalid_dm_id(user_list, dm_list, login_list):
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
    
def test_message_senddm_empty_message(user_list, dm_list, login_list):
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
    
def test_message_senddm_too_long_message(user_list, dm_list, login_list):
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
    
def test_message_senddm_auth_user_out_of_dm(user_list, dm_list, login_list):
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
    
def test_message_senddm_invalid_token(user_list, dm_list, login_list):
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
    
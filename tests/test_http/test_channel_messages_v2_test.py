import random
import pytest
import requests
import json
from src.config import url
from src.error import InputError, AccessError
from src.server import channels_list

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
                                              'is_public': False}).json())
    channel_list.append(requests.post(url + 'channels/create/v2',
                                      json = {'token': login_list[3]['token'],
                                              'name': "Cicy's channel",
                                              'is_public': False}).json())
    return channel_list

def test_normal_channel_messages(login_list, channel_list):
    '''
    
    This tests is testing the normal situation of sending messages in 
    public/private channels
    
    Parameters:
        login_list, channel_list
        
    Return:
        N/A
        
    '''
    requests.post(url + 'message/send/v1',
                  json = {'token': login_list[0]['token'],
                          'channel_id': channel_list[0]['channel_id'],
                          'message': 'message1'})
    requests.post(url + 'message/send/v1',
                  json = {'token': login_list[0]['token'],
                          'channel_id': channel_list[0]['channel_id'],
                          'message': 'message2'})
    requests.post(url + 'message/send/v1',
                  json = {'token': login_list[0]['token'],
                          'channel_id': channel_list[0]['channel_id'],
                          'message': 'message3'})
    requests.post(url + 'message/send/v1',
                  json = {'token': login_list[0]['token'],
                          'channel_id': channel_list[0]['channel_id'],
                          'message': 'message4'})
    
    requests.post(url + 'message/send/v1',
                  json = {'token': login_list[3]['token'],
                          'channel_id': channel_list[3]['channel_id'],
                          'message': 'message1'})
    requests.post(url + 'message/send/v1',
                  json = {'token': login_list[3]['token'],
                          'channel_id': channel_list[3]['channel_id'],
                          'message': 'message2'})
    requests.post(url + 'message/send/v1',
                  json = {'token': login_list[3]['token'],
                          'channel_id': channel_list[3]['channel_id'],
                          'message': 'message3'})
    requests.post(url + 'message/send/v1',
                  json = {'token': login_list[3]['token'],
                          'channel_id': channel_list[3]['channel_id'],
                          'message': 'message4'})
    
    response_1 = requests.get(url + 'channel/messages/v2',
                              params = {'token': login_list[0]['token'],
                                        'channel_id': channel_list[0]['channel_id'],
                                        'start': 0}).json()
    response_2 = requests.get(url + 'channel/messages/v2',
                              params = {'token': login_list[3]['token'],
                                        'channel_id': channel_list[3]['channel_id'],
                                        'start': 0}).json()

    assert response_1['messages'][0]['message'] == "message4"
    assert response_1['messages'][1]['message'] == "message3"
    assert response_1['messages'][2]['message'] == "message2"
    assert response_1['messages'][3]['message'] == "message1"
    assert response_2['messages'][0]['message'] == "message4"
    assert response_2['messages'][1]['message'] == "message3"
    assert response_2['messages'][2]['message'] == "message2"
    assert response_2['messages'][3]['message'] == "message1"
    
    assert response_1['start'] == 0
    assert response_2['start'] == 0
    assert response_1['end'] == -1
    assert response_2['end'] == -1
    
def test_channel_message_more_messages(login_list, channel_list):
    '''
    
    This tests is to test when sending more than 50 messages, the end value is start +50
    
    Parameters:
        login_list, channel_list
        
    Return:
        N/A
        
    '''
    for i in range(55):
        # sending 55 messages in channel 0
        requests.post(url + 'message/send/v1',
                  json = {'token': login_list[0]['token'],
                          'channel_id': channel_list[0]['channel_id'],
                          'message': 'messages'})
    
    response_1 = requests.get(url + 'channel/messages/v2',
                              params = {'token': login_list[0]['token'],
                                        'channel_id': channel_list[0]['channel_id'],
                                        'start': 0}).json()
    
    for i in range(50):
        # test messages are correct
        assert response_1['messages'][i]['message'] == 'messages'
        
    # test start and end
    assert response_1['start'] == 0
    assert response_1['end'] == 50

def test_channel_messages_invalid_start(login_list, channel_list):
    '''
    
    Test channel messages with invalid start
    
    Parameters:
        login_list, channel_list
        
    Raises:
        InputError
        
    '''
    # no messages
    response_1 = requests.get(url + 'channel/messages/v2',
                              params = {'token': login_list[0]['token'],
                                        'channel_id': channel_list[0]['channel_id'],
                                        'start': 10})
    assert response_1.status_code == InputError.code
    
    # 4 messages but start at 10
    requests.post(url + 'message/send/v1',
                  json = {'token': login_list[0]['token'],
                          'channel_id': channel_list[0]['channel_id'],
                          'message': 'message1'})
    requests.post(url + 'message/send/v1',
                  json = {'token': login_list[0]['token'],
                          'channel_id': channel_list[0]['channel_id'],
                          'message': 'message2'})
    requests.post(url + 'message/send/v1',
                  json = {'token': login_list[0]['token'],
                          'channel_id': channel_list[0]['channel_id'],
                          'message': 'message3'})
    requests.post(url + 'message/send/v1',
                  json = {'token': login_list[0]['token'],
                          'channel_id': channel_list[0]['channel_id'],
                          'message': 'message4'})
    response_2 = requests.get(url + 'channel/messages/v2',
                              params = {'token': login_list[0]['token'],
                                        'channel_id': channel_list[0]['channel_id'],
                                        'start': 10})
    assert response_2.status_code == InputError.code
    
def test_channel_messages_invalid_channel_id(login_list, channel_list):
    '''
    
    This test is for testing input invalid channel_id
    
    Parameters:
        login_list, channel_list
        
    Raises:
        InputError
        
    '''
    new_id = random.randint(-65535, 65535)
    invalid_channel_id = []
    while len(invalid_channel_id) < 1:
        if not new_id in [channel_list[i]['channel_id'] for i in range(0,4)]:
            invalid_channel_id.append(new_id)
    requests.post(url + 'message/send/v1',
                  json = {'token': login_list[0]['token'],
                          'channel_id': channel_list[0]['channel_id'],
                          'message': 'message1'})
    requests.post(url + 'message/send/v1',
                  json = {'token': login_list[0]['token'],
                          'channel_id': channel_list[0]['channel_id'],
                          'message': 'message2'})
    requests.post(url + 'message/send/v1',
                  json = {'token': login_list[0]['token'],
                          'channel_id': channel_list[0]['channel_id'],
                          'message': 'message3'})
    requests.post(url + 'message/send/v1',
                  json = {'token': login_list[0]['token'],
                          'channel_id': channel_list[0]['channel_id'],
                          'message': 'message4'})
    response_1 = requests.get(url + 'channel/messages/v2',
                              params = {'token': login_list[0]['token'],
                                        'channel_id': invalid_channel_id[0],
                                        'start': 0})
    assert response_1.status_code == InputError.code
    
def test_channel_messages_user_not_in_channel(login_list, channel_list):
    '''
    
    This test is for testing input user isn't in channel
    
    Parameters:
        login_list, channel_list
        
    Raises:
        AccessError
        
    '''
    # all normal
    requests.post(url + 'message/send/v1',
                  json = {'token': login_list[0]['token'],
                          'channel_id': channel_list[0]['channel_id'],
                          'message': 'message1'})
    requests.post(url + 'message/send/v1',
                  json = {'token': login_list[0]['token'],
                          'channel_id': channel_list[0]['channel_id'],
                          'message': 'message2'})
    requests.post(url + 'message/send/v1',
                  json = {'token': login_list[0]['token'],
                          'channel_id': channel_list[0]['channel_id'],
                          'message': 'message3'})
    requests.post(url + 'message/send/v1',
                  json = {'token': login_list[0]['token'],
                          'channel_id': channel_list[0]['channel_id'],
                          'message': 'message4'})
    response_1 = requests.get(url + 'channel/messages/v2',
                              params = {'token': login_list[1]['token'],
                                        'channel_id': channel_list[0]['channel_id'],
                                        'start': 0})
    assert response_1.status_code == AccessError.code
    
def test_channel_messages_invalid_user_token(login_list, channel_list):
    '''
    
    This test is for testing raises AccessError for invalid token
    Even if there are some InputError, raises AccessError at first
    
    Parameters:
        login_list, channel_list
        
    Raises:
        AccessError
        
    '''
    new_id = random.randint(-65535, 65535)
    invalid_channel_id = []
    while len(invalid_channel_id) < 1:
        if not new_id in [channel_list[i]['channel_id'] for i in range(0,4)]:
            invalid_channel_id.append(new_id)
    # normal situation
    requests.post(url + 'message/send/v1',
                  json = {'token': login_list[0]['token'],
                          'channel_id': channel_list[0]['channel_id'],
                          'message': 'message1'})
    requests.post(url + 'message/send/v1',
                  json = {'token': login_list[0]['token'],
                          'channel_id': channel_list[0]['channel_id'],
                          'message': 'message2'})
    requests.post(url + 'message/send/v1',
                  json = {'token': login_list[0]['token'],
                          'channel_id': channel_list[0]['channel_id'],
                          'message': 'message3'})
    requests.post(url + 'message/send/v1',
                  json = {'token': login_list[0]['token'],
                          'channel_id': channel_list[0]['channel_id'],
                          'message': 'message4'})
    response_1 = requests.get(url + 'channel/messages/v2',
                              params = {'token': -1,
                                        'channel_id': channel_list[0]['channel_id'],
                                        'start': 0})
    assert response_1.status_code == AccessError.code
    
    # invalid start
    response_2 = requests.get(url + 'channel/messages/v2',
                              params = {'token': -1,
                                        'channel_id': channel_list[0]['channel_id'],
                                        'start': 10})
    assert response_2.status_code == AccessError.code
    
    # invalid channel_id
    response_3 = requests.get(url + 'channel/messages/v2',
                              params = {'token': -1,
                                        'channel_id': invalid_channel_id[0],
                                        'start': 0})
    assert response_3.status_code == AccessError.code
    
import pytest
import requests
import json
import random
from src.config import url
from src.error import InputError, AccessError

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

########################################################### Test_notifications/get/v1 ########################################################### 

def test_notification_in_channel(login_list, channel_list):
    '''
    
    This test is to test when some events happened in channel
    
    Args
        login_list, channel_list
        
    Assumption
        channel/invite/v2 is working well
        message/send/v1 is working well
        message/react/v1
        
    '''
    # user[0] add user[1] to channel[0]
    requests.post(f"{url}channel/invite/v2",
                  json= {'token': login_list[0]['token'],
                         'channel_id': channel_list[0]['channel_id'],
                         'u_id': login_list[1]['auth_user_id']})
    response_1 = requests.get(url + 'notifications/get/v1',
                              params={'token': login_list[1]['token']}).json()
    assert response_1['notifications'][0]['channel_id'] == channel_list[0]['channel_id']
    assert response_1['notifications'][0]['dm_id'] == -1
    assert response_1['notifications'][0]['notification_message'] == "steveyang added you to Steve's channel"
    
    # user[1] send a message in channel[0]
    response_2 = requests.post(url + 'message/send/v1',
                               json = {'token': login_list[1]['token'],
                                       'channel_id': channel_list[0]['channel_id'],
                                       'message': 'Hello guys'}).json()
    requests.post(url + "message/react/v1",
                  json = {'token': login_list[0]['token'],
                          'message_id': response_2['message_id'],
                          'react_id': 1})
    response_3 = requests.get(url + 'notifications/get/v1',
                              params={'token': login_list[1]['token']}).json()
    assert response_3['notifications'][1]['channel_id'] == channel_list[0]['channel_id']
    assert response_3['notifications'][1]['dm-id'] == -1
    assert response_3['notifications'][1]['notification_message'] == "steveyang reacted to your message in Steve's channel"

def test_notification_in_DM(login_list, dm_list):
    '''
    
    This test is to test when some events happened in DM
    
    Args
        login_list, dm_list
        
    Assumption
        message/senddm/v1 is working well
        dm/create/v1 is working well
        
    '''
    # in fixture, user[1] has been added to DM[0]
    response_1 = requests.get(url + 'notifications/get/v1',
                              params={'token': login_list[1]['token']}).json()
    assert response_1['notifications'][0]['channel_id'] == -1
    assert response_1['notifications'][0]['dm_id'] == dm_list[0]['dm_id']
    assert response_1['notifications'][0]['notification_message'] == "steveyang added you to bojinli, brianlee, steveyang"
    
    # user[1] sends a message in dm[0]
    response_2 = requests.post(url + 'message/senddm/v1',
                               json = {'token': login_list[1]['token'],
                                       'dm_id': dm_list[0]['dm_id'],
                                       'message': 'Hello guys'}).json()
    # user[0] reacts to this message
    requests.post(url + "message/react/v1",
                  json = {'token': login_list[0]['token'],
                          'message_id': response_2['message_id'],
                          'react_id': 1})
    response_3 = requests.get(url + 'notifications/get/v1',
                              params={'token': login_list[1]['token']}).json()
    assert response_3['notifications'][1]['dm_id'] == -1
    assert response_3['notifications'][1]['dm-id'] == dm_list[0]['dm_id']
    assert response_3['notifications'][1]['notification_message'] == "steveyang reacted to your message in bojinli, brianlee, steveyang"
    
########################################################### Test_notifications/get/v1 ########################################################### 

def test_search_normal(login_list, dm_list, channel_list):
    '''
    
    This test is to test when searching with a valid string
    
    Assumption
        message/senddm/v1 is working well
        message/send/v1 is working well
    
    '''
    # user[0] send 'Hello guys' 3 times
    requests.post(url + 'message/send/v1',
                  json = {'token': login_list[0]['token'],
                          'channel_id': channel_list[0]['channel_id'],
                          'message': 'Hello guys'})
    requests.post(url + 'message/send/v1',
                  json = {'token': login_list[0]['token'],
                          'channel_id': channel_list[0]['channel_id'],
                          'message': 'Hello guys'})
    requests.post(url + 'message/send/v1',
                  json = {'token': login_list[0]['token'],
                          'channel_id': channel_list[0]['channel_id'],
                          'message': 'Hello guys'})
    
    requests.post(url + 'message/senddm/v1',
                  json = {'token': login_list[1]['token'],
                          'dm_id': dm_list[0]['dm_id'],
                          'message': 'Hello Steve'})
    requests.post(url + 'message/senddm/v1',
                  json = {'token': login_list[0]['token'],
                          'dm_id': dm_list[0]['dm_id'],
                          'message': 'Hello Brian'})
    requests.post(url + 'message/senddm/v1',
                  json = {'token': login_list[2]['token'],
                          'dm_id': dm_list[0]['dm_id'],
                          'message': 'Hello world'})
    
    response_1 = requests.get(url + 'search/v1',
                               params = {'token': login_list[0]['token'],
                                       'query_str': 'guys'}).json()
    # assert 3 messages about 'guys'
    assert len(response_1['messages']) == 3
    response_2 = requests.get(url + 'search/v1',
                              params = {'token': login_list[0]['token'],
                                       'query_str': 'h'}).json()
    # assert 6 messages about 'h', also, this test is to test case-insensitive
    assert len(response_2['messages']) == 6
    response_3 = requests.get(url + 'search/v1',
                              params = {'token': login_list[0]['token'],
                                       'query_str': 'steve'}).json()
    # assert 1 messages about 'steve', also, this test is to test case-insensitive
    assert len(response_3['messages']) == 1
    

def test_search_invalid_query_string(login_list, dm_list, channel_list):
    '''
    
    This test is to test when searching with too long or empty query_string
    
    Assumption
        message/senddm/v1 is working well
        message/send/v1 is working well
    
    '''
    
    too_long_str = ""
    while len(too_long_str) <= 1000:
        too_long_str += 'a'
        
    # user[0] send 'Hello guys' 3 times
    requests.post(url + 'message/send/v1',
                  json = {'token': login_list[0]['token'],
                          'channel_id': channel_list[0]['channel_id'],
                          'message': 'Hello guys'})
    requests.post(url + 'message/send/v1',
                  json = {'token': login_list[0]['token'],
                          'channel_id': channel_list[0]['channel_id'],
                          'message': 'Hello guys'})
    requests.post(url + 'message/send/v1',
                  json = {'token': login_list[0]['token'],
                          'channel_id': channel_list[0]['channel_id'],
                          'message': 'Hello guys'})
    
    requests.post(url + 'message/senddm/v1',
                  json = {'token': login_list[1]['token'],
                          'dm_id': dm_list[0]['dm_id'],
                          'message': 'Hello Steve'})
    requests.post(url + 'message/senddm/v1',
                  json = {'token': login_list[0]['token'],
                          'dm_id': dm_list[0]['dm_id'],
                          'message': 'Hello Brian'})
    requests.post(url + 'message/senddm/v1',
                  json = {'token': login_list[2]['token'],
                          'dm_id': dm_list[0]['dm_id'],
                          'message': 'Hello world'})
    # test for empty query_str
    response_1 = requests.get(url + 'search/v1',
                              params = {'token': login_list[0]['token'],
                                       'query_str': ''})
    assert response_1.status_code == InputError.code
    
    # test for too long query_str
    response_2 = requests.get(url + 'search/v1',
                              params = {'token': login_list[0]['token'],
                                       'query_str': too_long_str})
    assert response_2.status_code == InputError.code
    
def test_search_invalid_token():
    '''
    
    This test is to test when token is invalid
    
    '''
    response_1 = requests.get(url + 'search/v1',
                              params = {'token': -1,
                                       'query_str': 'haha'})
    assert response_1.status_code == AccessError.code
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

########################################################### Test standup/start/v1 ########################################################### 

def test_standup_start(login_list, channel_list):
    """
    
    This test is to test successful start standup period

    Args:
        channel_list: pre-create channel list
        login_list: pre-login users

    Returns:
        N/A

    """
    standup_list = []
    standup_list.append(requests.post(url + 'standup/start/v1',
                                      json={'token': login_list[0]['token'],
                                            'channel_id': channel_list[0]['channel_id'],
                                            'length': 10}).json())
    time.sleep(10.1)
    standup_list.append(requests.post(url + 'standup/start/v1',
                                      json={'token': login_list[0]['token'],
                                            'channel_id': channel_list[0]['channel_id'],
                                            'length': 1}).json())
    standup_list.append(requests.post(url + 'standup/start/v1',
                                      json={'token': login_list[1]['token'],
                                            'channel_id': channel_list[1]['channel_id'],
                                            'length': 1}).json())
    standup_list.append(requests.post(url + 'standup/start/v1',
                                      json={'token': login_list[2]['token'],
                                            'channel_id': channel_list[2]['channel_id'],
                                            'length': 1}).json())
    for standup in standup_list:
        assert type(standup).__name__ == 'dict'
        assert type(standup['time_finish']).__name__ == 'int'
        
def test_standup_start_invalid_channel_id(login_list, channel_list):
    '''
    
    This test is to test when channel_id does not refer to a valid channel
    
    Args
        channel_list: pre-create channel list
        login_list: pre-login users

    Raises:
        InputError

    '''
    new_id = random.randint(-65535, 65535)
    invalid_channel_id = []
    while len(invalid_channel_id) < 1:
        if not new_id in [channel_list[i]['channel_id'] for i in range(0,4)]:
            invalid_channel_id.append(new_id)
    
    res_1 = requests.post(url + 'standup/start/v1',
                          json={'token': login_list[2]['token'],
                                'channel_id': invalid_channel_id[0],
                                'length': 1})
    assert res_1.status_code == InputError.code
    
def test_standup_start_length_cant_be_negative(login_list, channel_list):
    '''
    
    This test is to test when length is a negative integer
    
    Args
        channel_list: pre-create channel list
        login_list: pre-login users

    Raises:
        InputError

    '''
    res = requests.post(url + 'standup/start/v1',
                          json={'token': login_list[2]['token'],
                                'channel_id': channel_list[2]['channel_id'],
                                'length': -1})
    assert res.status_code == InputError.code
    res = requests.post(url + 'standup/start/v1',
                          json={'token': login_list[0]['token'],
                                'channel_id': channel_list[0]['channel_id'],
                                'length': -100})
    assert res.status_code == InputError.code
    
def test_standup_start_already_started(login_list, channel_list):
    '''
    
    This test is to test when an active standup is currently running in the channel
    
    Args
        channel_list: pre-create channel list
        login_list: pre-login users

    Raises:
        InputError

    '''
    # user[0] add user[1] to channel[0]
    requests.post(f"{url}channel/invite/v2",
                  json= {'token': login_list[0]['token'],
                         'channel_id': channel_list[0]['channel_id'],
                         'u_id': login_list[1]['auth_user_id']})
    # user[0] asked a 10 seconds standup
    requests.post(url + 'standup/start/v1',
                  json={'token': login_list[0]['token'],
                        'channel_id': channel_list[0]['channel_id'],
                        'length': 10})
    time.sleep(8)
    # user[0] asked a 10 seconds standup when the last standup didn't finish
    res = requests.post(url + 'standup/start/v1',
                        json={'token': login_list[1]['token'],
                              'channel_id': channel_list[0]['channel_id'],
                              'length': 10})
    assert res.status_code == InputError.code
    
def test_standuo_start_user_didnot_join_channel(login_list, channel_list):
    '''
    
    This test is to test when channel_id is valid and the authorised user is 
    not a member of the channel
    
    Args
        channel_list: pre-create channel list
        login_list: pre-login users

    Raises:
        AccessError

    '''
    res = requests.post(url + 'standup/start/v1',
                        json={'token': login_list[1]['token'],
                              'channel_id': channel_list[0]['channel_id'],
                              'length': 10})
    assert res.status_code == AccessError.code
    
def test_standuo_start_user_invalid_token(channel_list):
    '''
    
    This test is to test when token is invalid
    
    Args
        channel_list: pre-create channel list
        login_list: pre-login users

    Raises:
        AccessError

    '''
    res = requests.post(url + 'standup/start/v1',
                        json={'token': -1,
                              'channel_id': channel_list[0]['channel_id'],
                              'length': 10})
    assert res.status_code == AccessError.code
    
########################################################### Test standup/active/v1 ########################################################### 

def test_standup_active_normal(login_list, channel_list):
    '''
    
    This test is to test normal situations for standup_active
    
    Args
        channel_list: pre-create channel list
        login_list: pre-login users

    '''
    requests.post(url + 'standup/start/v1',
                  json={'token': login_list[0]['token'],
                        'channel_id': channel_list[0]['channel_id'],
                        'length': 2})
    res = requests.get(url + 'standup/active/v1',
                       params={'token': login_list[0]['token'],
                               'channel_id': channel_list[0]['channel_id']}).json()
    assert res['is_active'] is True
    assert res['time_finish'] == int(time.time()) + 2
    time.sleep(2.1)
    res = requests.get(url + 'standup/active/v1',
                       params={'token': login_list[0]['token'],
                               'channel_id': channel_list[0]['channel_id']}).json()
    assert res['is_active'] is False
    assert res['time_finish'] is None

def test_standup_active_invalid_channel_id(login_list, channel_list):
    '''
    
    This test is to test when channel_id does not refer to a valid channel
    
    Args
        channel_list: pre-create channel list
        login_list: pre-login users

    Raises:
        InputError

    '''
    new_id = random.randint(-65535, 65535)
    invalid_channel_id = []
    while len(invalid_channel_id) < 1:
        if not new_id in [channel_list[i]['channel_id'] for i in range(0,4)]:
            invalid_channel_id.append(new_id)
            
    res = requests.get(url + 'standup/active/v1',
                       params={'token': login_list[0]['token'],
                               'channel_id': invalid_channel_id[0]})
    assert res.status_code == InputError.code
    
def test_standup_active_user_didnot_join_channel(login_list, channel_list):
    '''
    
    This test is to test when channel_id is valid and the authorised user is 
    not a member of the channel
    
    Args
        channel_list: pre-create channel list
        login_list: pre-login users

    Raises:
        AccessError

    '''
    res = requests.get(url + 'standup/active/v1',
                       params={'token': login_list[1]['token'],
                               'channel_id': channel_list[0]['channel_id']})
    assert res.status_code == AccessError.code
    
def test_standup_active_invalid_token(channel_list):
    '''
    
    This test is to test when token is invalid
    
    Args
        channel_list: pre-create channel list
        login_list: pre-login users

    Raises:
        AccessError

    '''
    res = requests.get(url + 'standup/active/v1',
                       params={'token': -1,
                               'channel_id': channel_list[0]['channel_id']})
    assert res.status_code == AccessError.code

########################################################### Test standup/send/v1 ###########################################################

def test_standup_send_normal(login_list, channel_list):
    '''
    
    This test is to test when standup_send normal
    
    Args
        channel_list: pre-create channel list
        login_list: pre-login users
        
    '''
    requests.post(url + 'standup/start/v1',
                  json={'token': login_list[0]['token'],
                        'channel_id': channel_list[0]['channel_id'],
                        'length': 2})
    # send a message with @
    res = requests.post(url + 'standup/send/v1',
                  json = {'token': login_list[0]['token'],
                          'channel_id': channel_list[0]['channel_id'],
                          'message': "Hello guys @steveyang"})
    assert res.status_code == 200
    time.sleep(2.1)
    res = requests.get(url + 'notifications/get/v1',
                       params={'token': login_list[0]['token']}).json()
    # test @ should not be parsed as proper tag here
    assert res['notifications'] == []
    
def test_standup_send_invalid_channel_id(login_list, channel_list):
    '''
    
    This test is to test when channel_id does not refer to a valid channel
    
    Args
        channel_list: pre-create channel list
        login_list: pre-login users
        
    Raises:
        InputError
        
    '''
    new_id = random.randint(-65535, 65535)
    invalid_channel_id = []
    while len(invalid_channel_id) < 1:
        if not new_id in [channel_list[i]['channel_id'] for i in range(0,4)]:
            invalid_channel_id.append(new_id)
            
    requests.post(url + 'standup/start/v1',
                  json={'token': login_list[0]['token'],
                        'channel_id': channel_list[0]['channel_id'],
                        'length': 2})
    res = requests.post(url + 'standup/send/v1',
                  json = {'token': login_list[0]['token'],
                          'channel_id': invalid_channel_id[0],
                          'message': "Hello guys @steveyang"})
    assert res.status_code == InputError.code

def test_standup_send_too_long_message(login_list, channel_list):
    '''
    
    This test is to test when length of message is over 1000 characters
    
    Args
        channel_list: pre-create channel list
        login_list: pre-login users
        
    Raises:
        InputError
        
    '''
    too_long_message = ''
    while len(too_long_message) <= 1000:
        too_long_message += 'a'
    requests.post(url + 'standup/start/v1',
                  json={'token': login_list[0]['token'],
                        'channel_id': channel_list[0]['channel_id'],
                        'length': 2})
    # send a message with @
    res = requests.post(url + 'standup/send/v1',
                  json = {'token': login_list[0]['token'],
                          'channel_id': channel_list[0]['channel_id'],
                          'message': too_long_message})
    assert res.status_code == InputError.code
    
def test_standup_send_before_standup(login_list, channel_list):
    '''
    
    This test is to test when an active standup is not currently 
    running in the channel
    
    Args
        channel_list: pre-create channel list
        login_list: pre-login users
        
    Raises:
        InputError
        
    '''
    res = requests.post(url + 'standup/send/v1',
                  json = {'token': login_list[0]['token'],
                          'channel_id': channel_list[0]['channel_id'],
                          'message': "Hi"})
    assert res.status_code == InputError.code
    
def test_standup_send_user_didnot_join_channel(login_list, channel_list):
    '''
    
    This test is to test when channel_id is valid and the authorised user 
    is not a member of the channel
    
    Args
        channel_list: pre-create channel list
        login_list: pre-login users
        
    Raises:
        AccessError
        
    '''
    requests.post(url + 'standup/start/v1',
                  json={'token': login_list[0]['token'],
                        'channel_id': channel_list[0]['channel_id'],
                        'length': 2})
    res = requests.post(url + 'standup/send/v1',
                  json = {'token': login_list[1]['token'],
                          'channel_id': channel_list[0]['channel_id'],
                          'message': "Hi"})
    assert res.status_code == AccessError.code
    
def test_standup_send_invalid_token(login_list, channel_list):
    '''
    
    This test is to test when token is invalid
    
    Args
        channel_list: pre-create channel list
        login_list: pre-login users
        
    Raises:
        AccessError
        
    '''
    requests.post(url + 'standup/start/v1',
                  json={'token': login_list[0]['token'],
                        'channel_id': channel_list[0]['channel_id'],
                        'length': 2})
    res = requests.post(url + 'standup/send/v1',
                  json = {'token': -1,
                          'channel_id': channel_list[0]['channel_id'],
                          'message': "Hi"})
    assert res.status_code == AccessError.code
 
def test_standup_user_cant_leave_channel(login_list, channel_list):
    '''
    
    This test is to test when user who starts a standup can't leave 
    the channel
    
    Raises:
        InputError
        
    '''
    # user[0] add user[1] to channel[0]
    requests.post(f"{url}channel/invite/v2",
                  json= {'token': login_list[0]['token'],
                         'channel_id': channel_list[0]['channel_id'],
                         'u_id': login_list[1]['auth_user_id']})
    # user[1] asked a 10 seconds standup
    requests.post(url + 'standup/start/v1',
                  json={'token': login_list[1]['token'],
                        'channel_id': channel_list[0]['channel_id'],
                        'length': 10})
    # During standup, user[1] wanna leave the channel[0]
    res = requests.post(url + 'channel/leave/v1',
                        json = {'token': login_list[1]['token'],
                                'channel_id': channel_list[0]['channel_id']})
    assert res.status_code == InputError.code
    time.sleep(10.1)
    res = requests.post(url + 'channel/leave/v1',
                        json = {'token': login_list[1]['token'],
                                'channel_id': channel_list[0]['channel_id']})
    assert res.status_code == 200

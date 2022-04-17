import pytest
import requests
from src.config import url
from src.error import InputError, AccessError

@pytest.fixture(name = 'user_list')
def create_user_list():
    '''
    This function is to pre-register 4 users for further tests
    
    returns:
        user_list (dictionary), contains 4 pre-register users' information
    '''
    user_list = []
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
    user_list.append(requests.post(url + "auth/login/v2",
                                    json = {"email": "z5374603@unsw.com",
                                            "password": "123456"}).json())
    user_list.append(requests.post(url + "auth/login/v2",
                                    json = {"email": "z5374602@unsw.com",
                                            "password": "123456"}).json())
    user_list.append(requests.post(url + "auth/login/v2",
                                    json = {"email": "z5374601@unsw.com",
                                            "password": "123456"}).json())
    user_list.append(requests.post(url + "auth/login/v2",
                                    json = {"email": "z5374600@unsw.com",
                                            "password": "123456"}).json())
    return user_list

@pytest.fixture(name = 'channel_list')
def channel_create(user_list):
    '''
    This function is to pre-create 4 channels for further tests
    
    Steve and Brian's channels are public channels. Bojin and Cicy's channels are private channels
    
    returns:
        channel_list, contains 4 channels' channel_id
    '''
    channel_list = []
    channel_list.append(requests.post(url + 'channels/create/v2',
                                      json = {'token': user_list[0]['token'],
                                              'name': "Steve's channel",
                                              'is_public': True}).json())
    channel_list.append(requests.post(url + 'channels/create/v2',
                                      json = {'token': user_list[1]['token'],
                                              'name': "Brian's channel",
                                              'is_public': True}).json())
    channel_list.append(requests.post(url + 'channels/create/v2',
                                      json = {'token': user_list[2]['token'],
                                              'name': "Bojin's channel",
                                              'is_public': True}).json())
    channel_list.append(requests.post(url + 'channels/create/v2',
                                      json = {'token': user_list[3]['token'],
                                              'name': "Cicy's channel",
                                              'is_public': False}).json())
    return channel_list

@pytest.fixture(name = 'dm_list')
def create_dm(user_list):
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
                                 json = {'token': user_list[0]['token'],
                                         'u_ids': [user_list[1]['auth_user_id'], 
                                                   user_list[2]['auth_user_id']]}).json())
    
    # dm_list[1]: user[0], user[2]. user[3]
    dm_list.append(requests.post(url + "dm/create/v1",
                                 json = {'token': user_list[0]['token'],
                                         'u_ids': [user_list[3]['auth_user_id'], 
                                                   user_list[2]['auth_user_id']]}).json())
    
    # dm_list[2]: user[1], user[2]. user[3]
    dm_list.append(requests.post(url + "dm/create/v1",
                                 json = {'token': user_list[1]['token'],
                                         'u_ids': [user_list[2]['auth_user_id'], 
                                                   user_list[3]['auth_user_id']]}).json())
    return dm_list

@pytest.fixture(name = 'users')
def users(user_list):
    '''
    Make a list of users' info 
    
    Return:
        users 
        Type: list[dict]
    '''
    users = [
        {
            'u_id': user_list[0]['auth_user_id'],
            'email': 'z5374603@unsw.com',
            'name_first': 'Steve',
            'name_last': 'Yang',
            'handle_str': 'steveyang',
            'profile_img_url': ''
        },
        {
            'u_id': user_list[1]['auth_user_id'],
            'email': 'z5374602@unsw.com',
            'name_first': 'Brian',
            'name_last': 'Lee',
            'handle_str': 'brianlee',
            'profile_img_url': ''
        },
        {
            'u_id': user_list[2]['auth_user_id'],
            'email': 'z5374601@unsw.com',
            'name_first': 'Bojin',
            'name_last': 'Li',
            'handle_str': 'bojinli',
            'profile_img_url': ''
        },
        {
            'u_id': user_list[3]['auth_user_id'],
            'email': 'z5374600@unsw.com',
            'name_first':'Cicy',
            'name_last': 'Zhou',
            'handle_str': 'cicyzhou',
            'profile_img_url': ''
        }
    ]
    return users

################################################ user/stats/v1 test ################################################

def test_user_stats_normal(user_list, channel_list, dm_list):
    """

    This test is to test when user successfuly check stats

    """
    requests.post(url + 'message/send/v1',
                  json = {'token': user_list[0]['token'],
                          'channel_id': channel_list[0]['channel_id'],
                          'message': 'I am SuperBoy @steveyang'})
    requests.post(url + 'message/senddm/v1',
                  json = {'token': user_list[0]['token'],
                          'dm_id': dm_list[0]['dm_id'],
                          'message': 'I am SuperBoy @steveyang'})
    requests.post(url + 'message/send/v1',
                  json = {'token': user_list[1]['token'],
                          'channel_id': channel_list[1]['channel_id'],
                          'message': 'I am SuperBoy'})
    requests.post(url + 'message/senddm/v1',
                  json = {'token': user_list[2]['token'],
                          'dm_id': dm_list[2]['dm_id'],
                          'message': 'I am SuperBoy'})
    res = requests.get(url + 'user/stats/v1',
                       params = {'token': user_list[0]['token']}).json()
    assert len(res['user_stats']['channels_joined']) == 2
    assert res['user_stats']['channels_joined'][-1]['num_channels_joined'] == 1
    assert len(res['user_stats']['dms_joined']) == 3
    assert res['user_stats']['dms_joined'][-1]['num_dms_joined'] == 2
    assert len(res['user_stats']['messages_sent']) == 3
    assert res['user_stats']['messages_sent'][-1]['num_messages_sent'] == 2
    assert res['user_stats']['involvement_rate'] == 5/11

def test_user_stats_invalid_token(user_list, channel_list, dm_list):
    """

    This test is to test when token is invalid
    
    Raises:
        AccessError

    """
    requests.post(url + 'message/send/v1',
                  json = {'token': user_list[0]['token'],
                          'channel_id': channel_list[0]['channel_id'],
                          'message': 'I am SuperBoy @steveyang'})
    requests.post(url + 'message/senddm/v1',
                  json = {'token': user_list[0]['token'],
                          'dm_id': dm_list[0]['dm_id'],
                          'message': 'I am SuperBoy @steveyang'})
    requests.post(url + 'message/send/v1',
                  json = {'token': user_list[1]['token'],
                          'channel_id': channel_list[1]['channel_id'],
                          'message': 'I am SuperBoy'})
    requests.post(url + 'message/senddm/v1',
                  json = {'token': user_list[2]['token'],
                          'dm_id': dm_list[2]['dm_id'],
                          'message': 'I am SuperBoy'})
    res = requests.get(url + 'user/stats/v1',
                       params = {'token': -1})
    assert res.status_code == AccessError.code
    
################################################ users/stats/v1 test ################################################

def test_users_stats_normal(user_list, channel_list, dm_list):
    '''
    
    This test is to test when users_list get info successfully
    
    '''
    requests.post(url + 'message/send/v1',
                  json = {'token': user_list[0]['token'],
                          'channel_id': channel_list[0]['channel_id'],
                          'message': 'I am SuperBoy @steveyang'})
    requests.post(url + 'message/senddm/v1',
                  json = {'token': user_list[0]['token'],
                          'dm_id': dm_list[0]['dm_id'],
                          'message': 'I am SuperBoy @steveyang'})
    requests.post(url + 'message/send/v1',
                  json = {'token': user_list[1]['token'],
                          'channel_id': channel_list[1]['channel_id'],
                          'message': 'I am SuperBoy'})
    requests.post(url + 'message/senddm/v1',
                  json = {'token': user_list[2]['token'],
                          'dm_id': dm_list[2]['dm_id'],
                          'message': 'I am SuperBoy'})
    # remove a dm
    requests.delete(url + 'dm/remove/v1',
                    json = {"token": user_list[0]["token"], 
                            "dm_id": dm_list[0]['dm_id']})
    res = requests.get(url + 'users/stats/v1',
                       params = {'token': user_list[0]['token']}).json()
    assert res['workspace_stats']['channels_exist'][-1]['num_channels_exist'] == 4
    assert res['workspace_stats']['dms_exist'][-1]['num_dms_exist'] == 2
    assert res['workspace_stats']['messages_exist'][-1]['num_messages_exist'] == 3
    assert res['workspace_stats']['utilization_rate'] == 1
    requests.post(f"{url}auth/register/v2",
                  json = { 'email': 'z537@unsw.com',
                           'password': '123456',
                           'name_first': 'Stephen',
                           'name_last': 'Curry'})
    res = requests.get(url + 'users/stats/v1',
                       params = {'token': user_list[0]['token']}).json()
    assert res['workspace_stats']['utilization_rate'] == 4/5
    
def test_users_stats_invalid_token(user_list, channel_list, dm_list):
    '''
    
    This test is to test when token is invalid
    
    Raises:
        AccessError
    
    '''
    requests.post(url + 'message/send/v1',
                  json = {'token': user_list[0]['token'],
                          'channel_id': channel_list[0]['channel_id'],
                          'message': 'I am SuperBoy @steveyang'})
    requests.post(url + 'message/senddm/v1',
                  json = {'token': user_list[0]['token'],
                          'dm_id': dm_list[0]['dm_id'],
                          'message': 'I am SuperBoy @steveyang'})
    requests.post(url + 'message/send/v1',
                  json = {'token': user_list[1]['token'],
                          'channel_id': channel_list[1]['channel_id'],
                          'message': 'I am SuperBoy'})
    requests.post(url + 'message/senddm/v1',
                  json = {'token': user_list[2]['token'],
                          'dm_id': dm_list[2]['dm_id'],
                          'message': 'I am SuperBoy'})
    # remove a dm
    requests.delete(url + 'dm/remove/v1',
                    json = {"token": user_list[0]["token"], 
                            "dm_id": dm_list[0]['dm_id']})
    res = requests.get(url + 'users/stats/v1',
                       params = {'token': -1})
    assert res.status_code == AccessError.code
    
################################################ users/all/v1 test ################################################

def test_users_all_valid_token(user_list, users):
    '''
    
    This test is testing token is valid for user/all/v1
    
    parameters:
        user_list
        
    returns:
        N/A
        
    '''
    respon = requests.get(url + "users/all/v1", params = {
        'token': user_list[0]['token']
    }).json()

    # assert all users in the response return
    for i in range(4):
        assert users[i]['u_id'] == respon['users'][i]['u_id']
        assert users[i]['email'] == respon['users'][i]['email']
        assert users[i]['name_first'] == respon['users'][i]['name_first']
        assert users[i]['name_last'] == respon['users'][i]['name_last']
        assert users[i]['handle_str'] == respon['users'][i]['handle_str']

def test_users_all_invalid_token():
    '''
    Test users/all/v1 takes in an invalid token
    
    Raises:
        AccessError
    '''
    respon = requests.get(url + 'users/all/v1', params = {
        'token': -100})
    
    assert respon.status_code == AccessError.code
    
################################################ user/profile/v1 test ################################################ 

def test_user_profile_valid_token_and_uid(user_list, users):
    '''
    Test when u_id and token are both correct
    
    parameters:
        user_list
        
    returns:
        N/A
    '''
    response_1 = requests.get(url + "user/profile/v1", 
                              params = {
                                  'token': user_list[0]['token'],
                                  'u_id': user_list[0]['auth_user_id']
                              }).json()
    response_2 = requests.get(url + "user/profile/v1", 
                              params = {
                                  'token': user_list[1]['token'],
                                  'u_id': user_list[1]['auth_user_id']
                              }).json()
    
    assert users[0]['u_id'] == response_1['user']['u_id']
    assert users[0]['email'] == response_1['user']['email']
    assert users[0]['name_first'] == response_1['user']['name_first']
    assert users[0]['name_last'] == response_1['user']['name_last']
    assert users[0]['handle_str'] == response_1['user']['handle_str']
    assert users[1]['u_id'] == response_2['user']['u_id']
    assert users[1]['email'] == response_2['user']['email']
    assert users[1]['name_first'] == response_2['user']['name_first']
    assert users[1]['name_last'] == response_2['user']['name_last']
    assert users[1]['handle_str'] == response_2['user']['handle_str']
    
def test_users_profile_invalid_uid(user_list):
    '''
    Test when input u_id is wrong but token is correct
    
    Raises:
        InpuError
    '''
    response_1 = requests.get(url + "user/profile/v1", 
                              params = {
                                  'token': user_list[0]['token'],
                                  'u_id': -100
                              })
    assert response_1.status_code == InputError.code
    
def test_users_profile_invalid_token(user_list):
    '''
    Test when input token is wrong but u_id is correct
    and when token and u_id are both wrong
    
    Raises:
        AccessError
    '''
    response_1 = requests.get(url + "user/profile/v1", 
                              params = {
                                  'token': -100,
                                  'u_id': user_list[0]['auth_user_id']
                              })
    response_2 = requests.get(url + "user/profile/v1", 
                              params = {
                                  'token': -100,
                                  'u_id': -100
                              })
    
    assert response_1.status_code == AccessError.code
    assert response_2.status_code == AccessError.code
    
################################################ user/profile/setname/v1 test ################################################

def test_user_profile_setname_v1_valid_name(user_list):
    '''
    
    Test when user's new name is valid and set name successfully
    
    '''
    # set a new name
    requests.put(url + 'user/profile/setname/v1', json={
        'token': user_list[0]['token'],
        'name_first': 'Newfname',
        'name_last': 'Newlname',
    })
    
    # get the profile of the user who reset name
    respon = requests.get(url + 'user/profile/v1', params={
        'token': user_list[0]['token'],
        'u_id': user_list[0]['auth_user_id'],
    })

    # assert the frofile of this user will be changed and the first name and last name will match the new
    assert respon.json()['user']['name_first'] == 'Newfname'
    assert respon.json()['user']['name_last'] == 'Newlname'

def test_user_profile_setname_v1_empty_first_name(user_list):
    '''
    
    Test when user's first name is empty
    
    Raises:
        InpuError
    
    '''
    respon = requests.put(url + 'user/profile/setname/v1', json={
        'token': user_list[0]['token'],
        'name_first': '',
        'name_last': 'Newlname',
    })

    assert respon.status_code == InputError.code
    
def test_user_profile_setname_v1_empty_last_name(user_list):
    '''
    
    Test when user's last name is empty
    
    Raises:
        InpuError
    
    '''
    respon = requests.put(url + 'user/profile/setname/v1', json={
        'token': user_list[0]['token'],
        'name_first': 'Newfname',
        'name_last': '',
    })

    assert respon.status_code == InputError.code
    
def test_user_profile_setname_v1_empty_name(user_list):
    '''
    
    Test when user's name is empty
    
    Raises:
        InpuError
    
    '''
    respon = requests.put(url + 'user/profile/setname/v1', json={
        'token': user_list[0]['token'],
        'name_first': '',
        'name_last': '',
    })

    assert respon.status_code == InputError.code
    
def test_user_profile_setname_v1_too_long_first_name(user_list):
    '''
    
    Test when user's first name is too long
    
    Raises:
        InpuError
    
    '''
    too_long_name = ''
    while len(too_long_name) < 51:
        too_long_name += 'a'
    respon = requests.put(url + 'user/profile/setname/v1', json={
        'token': user_list[0]['token'],
        'name_first': too_long_name,
        'name_last': 'Newlname',
    })

    assert respon.status_code == InputError.code
    
def test_user_profile_setname_v1_too_long_last_name(user_list):
    '''
    
    Test when user's last name is too long
    
    Raises:
        InpuError
    
    '''
    too_long_name = ''
    while len(too_long_name) < 51:
        too_long_name += 'a'
    respon = requests.put(url + 'user/profile/setname/v1', json={
        'token': user_list[0]['token'],
        'name_first': 'Newfname',
        'name_last': too_long_name,
    })

    assert respon.status_code == InputError.code
    
def test_user_profile_setname_v1_too_long_name(user_list):
    '''
    
    Test when user's name is too long
    
    Raises:
        InpuError
    
    '''
    too_long_name = ''
    while len(too_long_name) < 51:
        too_long_name += 'a'
    respon = requests.put(url + 'user/profile/setname/v1', json={
        'token': user_list[0]['token'],
        'name_first': too_long_name,
        'name_last': too_long_name,
    })

    assert respon.status_code == InputError.code
 
def test_user_profile_setname_v1_invalid_token(user_list):
    '''
     
    Test when token is invalid, including those InputError but still raises AccessError 
     
    Raises:
        AccessError
        
    '''
    too_long_name = ''
    while len(too_long_name) < 51:
        too_long_name += 'a'
        
    # valid name
    response_1 = requests.put(url + 'user/profile/setname/v1', json={
        'token': -100,
        'name_first': 'Newfname',
        'name_last': 'Newlname',
    })
    
    # empty new first name
    response_2 = requests.put(url + 'user/profile/setname/v1', json={
        'token': -100,
        'name_first': '',
        'name_last': 'Newlname',
    })
    
    # empty new last name
    response_3 = requests.put(url + 'user/profile/setname/v1', json={
        'token': -100,
        'name_first': 'Newfname',
        'name_last': '',
    })
    
    # empty new name
    response_4 = requests.put(url + 'user/profile/setname/v1', json={
        'token': -100,
        'name_first': '',
        'name_last': '',
    })
    
    # too long first name
    response_5 = requests.put(url + 'user/profile/setname/v1', json={
        'token': -100,
        'name_first': too_long_name,
        'name_last': 'Newlname',
    })
    
    # too long last name
    response_6 = requests.put(url + 'user/profile/setname/v1', json={
        'token': -100,
        'name_first': 'Newfname',
        'name_last': too_long_name,
    })
    
    # too long name
    response_7 = requests.put(url + 'user/profile/setname/v1', json={
        'token': -100,
        'name_first': too_long_name,
        'name_last': too_long_name,
    })
    
    assert response_1.status_code == AccessError.code
    assert response_2.status_code == AccessError.code
    assert response_3.status_code == AccessError.code
    assert response_4.status_code == AccessError.code
    assert response_5.status_code == AccessError.code
    assert response_6.status_code == AccessError.code
    assert response_7.status_code == AccessError.code
    
################################################ user/profile/setemail/v1 test ################################################

def test_user_profile_setemail_valid_email(user_list):
    '''
    
    Test user set a valid new email and change profile successfully
    
    parameters:
        user_list
        
    returns:
        N/A
    
    '''
    # change email successfully
    requests.put(url + 'user/profile/setemail/v1', json={
        'token': user_list[0]['token'],
        'email': '1981686549@qq.com',
    })

    # get the profile of the user
    respon = requests.get(url + 'user/profile/v1', params={
        'token': user_list[0]['token'],
        'u_id': user_list[0]['auth_user_id'],
    })
    
    # users email will be changed
    assert respon.json()['user']['email'] == '1981686549@qq.com'
    
def test_user_profile_setemail_without_both_dot_and_at_email(user_list):
    '''
    
    Test user set a without both . and @ new email 
    
    Raises:
        InputError
        
    '''
    response_1 = requests.put(url + 'user/profile/setemail/v1', json={
        'token': user_list[0]['token'],
        'email': '1981686549qqcom',
    })
    
    # empty email
    response_2 = requests.put(url + 'user/profile/setemail/v1', json={
        'token': user_list[0]['token'],
        'email': '',
    })
    
    assert response_1.status_code == InputError.code
    assert response_2.status_code == InputError.code
    
def test_user_profile_setemail_without_dot_email(user_list):
    '''
    
    Test user set a without both . new email 
    
    Raises:
        InputError
        
    '''
    response_1 = requests.put(url + 'user/profile/setemail/v1', json={
        'token': user_list[0]['token'],
        'email': '1981686549@qqcom',
    })
    
    assert response_1.status_code == InputError.code
    
def test_user_profile_setemail_without_at_email(user_list):
    '''
    
    Test user set a without both . new email 
    
    Raises:
        InputError
        
    '''
    response_1 = requests.put(url + 'user/profile/setemail/v1', json={
        'token': user_list[0]['token'],
        'email': '1981686549qq.com',
    })
    
    assert response_1.status_code == InputError.code
    
def test_user_profile_setemail_email_has_been_used(user_list):
    '''
    
    Test user set a new email, which has been used
    
    Raises:
        InputError
        
    '''
    response_1 = requests.put(url + 'user/profile/setemail/v1', json={
        'token': user_list[0]['token'],
        'email': 'z5374602@unsw.com',
    })
    response_2 = requests.put(url + 'user/profile/setemail/v1', json={
        'token': user_list[0]['token'],
        'email': 'z5374601@unsw.com',
    })
    
    assert response_1.status_code == InputError.code
    assert response_2.status_code == InputError.code
    
def test_user_profile_setemail_invalid_token(user_list):
    '''
    
    Test when token is invalid, including those InputError but still raises AccessError 
     
    Raises:
        AccessError
        
    '''
    # valid email
    response_1 = requests.put(url + 'user/profile/setemail/v1', json={
        'token': -100,
        'email': '1981686549@qq.com',
    })
    
    # empty email
    response_2 = requests.put(url + 'user/profile/setemail/v1', json={
        'token': -100,
        'email': '',
    })
    
    # without . anmd @
    response_3 = requests.put(url + 'user/profile/setemail/v1', json={
        'token': -100,
        'email': '1981686549qqcom',
    })
    
    # without .
    response_4 = requests.put(url + 'user/profile/setemail/v1', json={
        'token': -100,
        'email': '1981686549@qqcom',
    })
    
    # without @
    response_5 = requests.put(url + 'user/profile/setemail/v1', json={
        'token': -100,
        'email': '1981686549qq.com',
    })
    
    # email has been used
    response_6 = requests.put(url + 'user/profile/setemail/v1', json={
        'token': -100,
        'email': 'z5374602@unsw.com',
    })
    
    assert response_1.status_code == AccessError.code
    assert response_2.status_code == AccessError.code
    assert response_3.status_code == AccessError.code
    assert response_4.status_code == AccessError.code
    assert response_5.status_code == AccessError.code
    assert response_6.status_code == AccessError.code
    
################################################ user/profile/sethandle/v1 test ################################################

def test_user_profile_sethandle_valid_handle(user_list):
    '''
    
    Successfully change the handle
    
    '''

    # handle with lower_chareacters
    requests.put(url + 'user/profile/sethandle/v1', json={
        'token': user_list[0]['token'],
        'handle_str': 'stttteve',
    })
    
    # handle with number
    requests.put(url + 'user/profile/sethandle/v1', json={
        'token': user_list[1]['token'],
        'handle_str': 'sttteve1',
    })

    # handle with upper_characters
    requests.put(url + 'user/profile/sethandle/v1', json={
        'token': user_list[2]['token'],
        'handle_str': 'Sttteve1',
    })

    response_1 = requests.get(url + 'user/profile/v1', params={
        'token': user_list[0]['token'],
        'u_id': user_list[0]['auth_user_id'],
    })
    
    response_2 = requests.get(url + 'user/profile/v1', params={
        'token': user_list[1]['token'],
        'u_id': user_list[1]['auth_user_id'],
    })
    
    response_3 = requests.get(url + 'user/profile/v1', params={
        'token': user_list[2]['token'],
        'u_id': user_list[2]['auth_user_id'],
    })

    assert response_1.json()['user']['handle_str'] == 'stttteve'
    assert response_2.json()['user']['handle_str'] == 'sttteve1'
    assert response_3.json()['user']['handle_str'] == 'Sttteve1'
    
def test_user_profile_sethandle_too_short_handle(user_list):
    '''
    
    Test new handle is less than 3 characters
    
    Raises:
        InputError
        
    '''
    response_1 = requests.put(url + 'user/profile/sethandle/v1', json={
        'token': user_list[0]['token'],
        'handle_str': '',
    })
    
    response_2 = requests.put(url + 'user/profile/sethandle/v1', json={
        'token': user_list[1]['token'],
        'handle_str': 'a',
    })
    
    response_3 = requests.put(url + 'user/profile/sethandle/v1', json={
        'token': user_list[2]['token'],
        'handle_str': 'ab',
    })
    
    assert response_1.status_code == InputError.code
    assert response_2.status_code == InputError.code
    assert response_3.status_code == InputError.code
    
def test_user_profile_sethandle_too_long_handle(user_list):
    '''
    
    Test new handle is more than 20 characters
    
    Raises:
        InputError
        
    '''
    too_long_handle = ""
    while len(too_long_handle) < 21:
        too_long_handle += 'a'
        
    response_1 = requests.put(url + 'user/profile/sethandle/v1', json={
        'token': user_list[0]['token'],
        'handle_str': too_long_handle,
    })
    
    assert response_1.status_code == InputError.code
    
def test_user_profile_sethandle_not_alphanumeric_handle(user_list):
    '''
    
    Test new handle is not alphanumeric
    
    Raises:
        InputError
        
    '''
    response_1 = requests.put(url + 'user/profile/sethandle/v1', json={
        'token': user_list[0]['token'],
        'handle_str': '@qwasS&^%$!',
    })
    
    assert response_1.status_code == InputError.code
    
def test_user_profile_sethandle_has_been_used_handle(user_list):
    '''
    
    Test new handle has been used
    
    Raises:
        InputError
        
    '''
    response_1 = requests.put(url + 'user/profile/sethandle/v1', json={
        'token': user_list[0]['token'],
        'handle_str': 'cicyzhou',
    })
    
    assert response_1.status_code == InputError.code
    
def test_user_profile_sethandle_invalid_token(user_list):
    '''
    
    Test when token is invalid, including those InputError but still raises AccessError 
     
    Raises:
        AccessError
        
    '''
    too_long_handle = ""
    while len(too_long_handle) < 21:
        too_long_handle += 'a'
        
    # valid handle
    response_1 = requests.put(url + 'user/profile/sethandle/v1', json={
        'token': -100,
        'handle_str': 'SSSSssssteve',
    })
    
    # too_short_handle
    response_2 = requests.put(url + 'user/profile/sethandle/v1', json={
        'token': -100,
        'handle_str': 'SS',
    })
    
    # too long handle
    response_3 = requests.put(url + 'user/profile/sethandle/v1', json={
        'token': -100,
        'handle_str': too_long_handle,
    })
    
    # has been used handle
    response_4 = requests.put(url + 'user/profile/sethandle/v1', json={
        'token': -100,
        'handle_str': 'bojinli',
    })
    
    # not alphanumeric handle
    response_5 = requests.put(url + 'user/profile/sethandle/v1', json={
        'token': -100,
        'handle_str': 'bojinli!@#',
    })
    
    assert response_1.status_code == AccessError.code
    assert response_2.status_code == AccessError.code
    assert response_3.status_code == AccessError.code
    assert response_4.status_code == AccessError.code
    assert response_5.status_code == AccessError.code
    
################################################ user/profile/uploadphoto/v1 test ################################################
    
def test_user_profile_uploadphoto_normal(user_list):
    """

    Test user_profile_uploadphoto when all condition are valid
    
    """
    resp = requests.post(url + 'user/profile/uploadphoto/v1', json={
        "token": user_list[0]["token"],
        "img_url": 'http://unswcse.alwaysdata.net/profile_img/vc1LgHIMq4DHV1UIfMCHdGOC7lrW0JKi2xliwRthcIc.jpg',
        "x_start": 0,
        "y_start": 0,
        "x_end": 200,
        "y_end": 200,
    })
    
    assert resp.status_code == 200
    
def test_user_profile_uploadphoto_invalid_URL(user_list):
    """

    Test user_profile_uploadphoto when img_url is invalid
    
    Raises:
        InputError
    
    """
    resp = requests.post(url + 'user/profile/uploadphoto/v1', json={
        "token": user_list[0]["token"],
        "img_url": 'unswcs.alwaysdata.net/profile_img/vc1LgHIMq4DHV1UIfMCHdGOC7lrW0JKi2xliwRth',
        "x_start": 0,
        "y_start": 0,
        "x_end": 200,
        "y_end": 200,
    })
    
    assert resp.status_code == InputError.code

def test_user_profile_uploadphoto_invalid_status_code(user_list):
    """

    Test user_profile_uploadphoto when img_url returns an
    HTTP status other than 200, or any other errors occur 
    when attempting to retrieve the image
    
    Raises:
        InputError
    
    """
    resp = requests.post(url + 'user/profile/uploadphoto/v1', json={
        "token": user_list[0]["token"],
        "img_url": 'http://unswcse.alwaysdata.net/abc.jpg',
        "x_start": 0,
        "y_start": 0,
        "x_end": 200,
        "y_end": 200,
    })
    
    assert resp.status_code == InputError.code
    
def test_user_profile_uploadphoto_out_of_dimensions(user_list):
    """

    Test user_profile_uploadphoto when any of x_start, y_start, 
    x_end, y_end are not within the dimensions of the image at the URL
    
    Raises:
        InputError
    
    """
    resp = requests.post(url + 'user/profile/uploadphoto/v1', json={
        "token": user_list[0]["token"],
        "img_url": 'http://unswcse.alwaysdata.net/profile_img/vc1LgHIMq4DHV1UIfMCHdGOC7lrW0JKi2xliwRthcIc.jpg',
        "x_start": 0,
        "y_start": 0,
        "x_end": 1800,
        "y_end": 2000,
    })
    
    assert resp.status_code == InputError.code
    
def test_user_profile_uploadphoto_invalid_start_and_end(user_list):
    """

    Test user_profile_uploadphoto when image uploaded is not a JPG
    
    Raises:
        InputError
    
    """
    resp = requests.post(url + 'user/profile/uploadphoto/v1', json={
        "token": user_list[0]["token"],
        "img_url": 'http://unswcse.alwaysdata.net/profile_img/vc1LgHIMq4DHV1UIfMCHdGOC7lrW0JKi2xliwRthcIc.jpg',
        "x_start": 100,
        "y_start": 100,
        "x_end": 100,
        "y_end": 50,
    })
    assert resp.status_code == InputError.code
    resp = requests.post(url + 'user/profile/uploadphoto/v1', json={
        "token": user_list[0]["token"],
        "img_url": 'http://unswcse.alwaysdata.net/profile_img/vc1LgHIMq4DHV1UIfMCHdGOC7lrW0JKi2xliwRthcIc.jpg',
        "x_start": 100,
        "y_start": 100,
        "x_end": 50,
        "y_end": 100,
    })
    assert resp.status_code == InputError.code
    
def test_user_profile_uploadphoto_not_JPG(user_list):
    """

    Test user_profile_uploadphoto when all condition are valid
    
    Raises:
        InputError
        
    """
    resp = requests.post(url + 'user/profile/uploadphoto/v1', json={
        "token": user_list[0]["token"],
        "img_url": 'https://www.bing.com/images/search?q=Png图片&FORM=IQFRBA&id=6E60E94DB8C2D2BA8B9036F95011FD3504117596',
        "x_start": 0,
        "y_start": 0,
        "x_end": 2,
        "y_end": 2,
    })
    assert resp.status_code == InputError.code
    
def test_user_profile_uploadphoto_invalid_token(user_list):
    '''
    
    This test is to test when token is invalid
    
    Raises:
        AccessError
        
    '''
    resp = requests.post(url + 'user/profile/uploadphoto/v1', json={
        "token": -1,
        "img_url": 'http://unswcse.alwaysdata.net/profile_img/vc1LgHIMq4DHV1UIfMCHdGOC7lrW0JKi2xliwRthcIc.jpg',
        "x_start": 0,
        "y_start": 0,
        "x_end": 200,
        "y_end": 200,
    })
    
    assert resp.status_code == AccessError.code
    

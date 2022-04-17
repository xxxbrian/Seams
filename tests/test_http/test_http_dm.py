import pytest
import requests
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

######################################## Test_dm/details/v1 ########################################

def test_dm_details_normal(login_list, dm_list):
    '''
    
    This test is to test when everything is fine and return correct info
    
    Assumption:
        dm/create/v1 is working well
    '''
    dm_0 = 'bojinli, brianlee, steveyang'
    dm_1 = 'bojinli, cicyzhou, steveyang'
    dm_2 = 'bojinli, brianlee, cicyzhou'
    response_1 = requests.get(url + 'dm/details/v1',
                              params = {'token': login_list[0]['token'],
                                        'dm_id': dm_list[0]['dm_id']}).json()
    response_2 = requests.get(url + 'dm/details/v1',
                              params = {'token': login_list[0]['token'],
                                        'dm_id': dm_list[1]['dm_id']}).json()
    response_3 = requests.get(url + 'dm/details/v1',
                              params = {'token': login_list[1]['token'],
                                        'dm_id': dm_list[2]['dm_id']}).json()

    assert response_1['name'] == dm_0
    assert response_1['members'][0]['u_id'] == login_list[1]['auth_user_id']
    assert response_1['members'][0]['email'] == "z5374602@unsw.com"
    assert response_1['members'][0]['name_first'] == 'Brian'
    assert response_1['members'][0]['name_last'] == 'Lee'
    assert response_1['members'][0]['handle_str'] == 'brianlee'
    assert response_1['members'][1]['u_id'] == login_list[2]['auth_user_id']
    assert response_1['members'][1]['email'] == "z5374601@unsw.com"
    assert response_1['members'][1]['name_first'] == 'Bojin'
    assert response_1['members'][1]['name_last'] == 'Li'
    assert response_1['members'][1]['handle_str'] == 'bojinli'
    assert response_1['members'][2]['u_id'] == login_list[0]['auth_user_id']
    assert response_1['members'][2]['email'] == "z5374603@unsw.com"
    assert response_1['members'][2]['name_first'] == 'Steve'
    assert response_1['members'][2]['name_last'] == 'Yang'
    assert response_1['members'][2]['handle_str'] == 'steveyang'
    
    assert response_2['name'] == dm_1
    assert response_2['members'][0]['u_id'] == login_list[3]['auth_user_id']
    assert response_2['members'][0]['email'] == "z5374600@unsw.com"
    assert response_2['members'][0]['name_first'] == 'Cicy'
    assert response_2['members'][0]['name_last'] == 'Zhou'
    assert response_2['members'][0]['handle_str'] == 'cicyzhou'
    assert response_2['members'][1]['u_id'] == login_list[2]['auth_user_id']
    assert response_2['members'][1]['email'] == "z5374601@unsw.com"
    assert response_2['members'][1]['name_first'] == 'Bojin'
    assert response_2['members'][1]['name_last'] == 'Li'
    assert response_2['members'][1]['handle_str'] == 'bojinli'
    assert response_2['members'][2]['u_id'] == login_list[0]['auth_user_id']
    assert response_2['members'][2]['email'] == "z5374603@unsw.com"
    assert response_2['members'][2]['name_first'] == 'Steve'
    assert response_2['members'][2]['name_last'] == 'Yang'
    assert response_2['members'][2]['handle_str'] == 'steveyang'
    
    assert response_3['name'] == dm_2
    assert response_3['members'][0]['u_id'] == login_list[2]['auth_user_id']
    assert response_3['members'][0]['email'] == "z5374601@unsw.com"
    assert response_3['members'][0]['name_first'] == 'Bojin'
    assert response_3['members'][0]['name_last'] == 'Li'
    assert response_3['members'][0]['handle_str'] == 'bojinli'
    assert response_3['members'][1]['u_id'] == login_list[3]['auth_user_id']
    assert response_3['members'][1]['email'] == "z5374600@unsw.com"
    assert response_3['members'][1]['name_first'] == 'Cicy'
    assert response_3['members'][1]['name_last'] == 'Zhou'
    assert response_3['members'][1]['handle_str'] == 'cicyzhou'
    assert response_3['members'][2]['u_id'] == login_list[1]['auth_user_id']
    assert response_3['members'][2]['email'] == "z5374602@unsw.com"
    assert response_3['members'][2]['name_first'] == 'Brian'
    assert response_3['members'][2]['name_last'] == 'Lee'
    assert response_3['members'][2]['handle_str'] == 'brianlee'
    
def test_dm_details_invalid_dm_id(login_list, dm_list):
    '''
    
    This test is to test when input a invalid dm_id
    
    Raises:
        InputError
        
    '''
    new_id = random.randint(-65535, 65535)
    invalid_dm_id = []
    while len(invalid_dm_id) < 1:
        if not new_id in [dm_list[i]['dm_id'] for i in range(0,3)]:
            invalid_dm_id.append(new_id)
    response_1 = requests.get(url + 'dm/details/v1',
                              params = {'token': login_list[0]['token'],
                                        'dm_id': invalid_dm_id[0]})
    assert response_1.status_code == InputError.code
    
def test_dm_details_invalid_auth_user(login_list, dm_list):
    '''
    
    This test is to test when dm_id is valid and the authorised user is 
    not a member of the DM
    
    Raises:
        AccessError    

    '''
    response_1 = requests.get(url + 'dm/details/v1',
                              params = {'token': login_list[3]['token'],
                                        'dm_id': dm_list[0]['dm_id']})
    assert response_1.status_code == AccessError.code

def test_dm_details_invalid_token(login_list, dm_list):
    '''
    
    This test is to test when input invalid token
    
    Raises: 
        AccessError
        
    '''
    response_1 = requests.get(url + 'dm/details/v1',
                              params = {'token': -1,
                                        'dm_id': dm_list[0]['dm_id']})
    assert response_1.status_code == AccessError.code
    
######################################## Test_dm/leave/v1 ########################################
    
def test_dm_leave_normal(login_list, dm_list):
    '''
    
    This test is to test when user leaves dm successfully
    
    Assumption:
        dm/details/v1 is working well
        
    '''
    # user[1] leaves dm[0]
    dm_0 = 'bojinli, brianlee, steveyang'
    requests.post(url + "dm/leave/v1",
                  json = {'token': login_list[1]['token'],
                          'dm_id': dm_list[0]['dm_id']})
    response_1 = requests.get(url + 'dm/details/v1',
                              params = {'token': login_list[0]['token'],
                                        'dm_id': dm_list[0]['dm_id']}).json()
    assert response_1['name'] == dm_0
    assert response_1['members'][0]['u_id'] == login_list[2]['auth_user_id']
    assert response_1['members'][0]['email'] == "z5374601@unsw.com"
    assert response_1['members'][0]['name_first'] == 'Bojin'
    assert response_1['members'][0]['name_last'] == 'Li'
    assert response_1['members'][0]['handle_str'] == 'bojinli'
    assert response_1['members'][1]['u_id'] == login_list[0]['auth_user_id']
    assert response_1['members'][1]['email'] == "z5374603@unsw.com"
    assert response_1['members'][1]['name_first'] == 'Steve'
    assert response_1['members'][1]['name_last'] == 'Yang'
    assert response_1['members'][1]['handle_str'] == 'steveyang'
    
def test_dm_leave_owner_leaves(login_list, dm_list):
    '''
    
    This test is to test when owner user leaves dm successfully
    
    Assumption:
        dm/details/v1 is working well
        
    '''
    # user[0] leaves dm[0]
    dm_0 = 'bojinli, brianlee, steveyang'
    requests.post(url + "dm/leave/v1",
                  json = {'token': login_list[0]['token'],
                          'dm_id': dm_list[0]['dm_id']})
    response_1 = requests.get(url + 'dm/details/v1',
                              params = {'token': login_list[1]['token'],
                                        'dm_id': dm_list[0]['dm_id']}).json()
    assert response_1['name'] == dm_0
    assert response_1['members'][0]['u_id'] == login_list[1]['auth_user_id']
    assert response_1['members'][0]['email'] == "z5374602@unsw.com"
    assert response_1['members'][0]['name_first'] == 'Brian'
    assert response_1['members'][0]['name_last'] == 'Lee'
    assert response_1['members'][0]['handle_str'] == 'brianlee'
    assert response_1['members'][1]['u_id'] == login_list[2]['auth_user_id']
    assert response_1['members'][1]['email'] == "z5374601@unsw.com"
    assert response_1['members'][1]['name_first'] == 'Bojin'
    assert response_1['members'][1]['name_last'] == 'Li'
    assert response_1['members'][1]['handle_str'] == 'bojinli'
    
def test_dm_leave_invalid_dm_id(login_list, dm_list):
    '''
    
    This test is to test when input a invalid dm_id
    
    Raises:
        InputError
        
    '''
    new_id = random.randint(-65535, 65535)
    invalid_dm_id = []
    while len(invalid_dm_id) < 1:
        if not new_id in [dm_list[i]['dm_id'] for i in range(0,3)]:
            invalid_dm_id.append(new_id)
    response_1 = requests.post(url + "dm/leave/v1",
                               json = {'token': login_list[0]['token'],
                                       'dm_id': invalid_dm_id[0]})
    assert response_1.status_code == InputError.code
    
def test_dm_leave_invalid_auth_user(login_list, dm_list):
    '''
    
    This test is to test when dm_id is valid and the authorised user is 
    not a member of the DM
    
    Raises:
        AccessError
        
    '''
    response_1 = requests.post(url + "dm/leave/v1",
                               json = {'token': login_list[3]['token'],
                                       'dm_id': dm_list[0]['dm_id']})
    assert response_1.status_code == AccessError.code
    
def test_dm_leave_invalid_token(login_list, dm_list):
    '''
    
    This test is to test when input invalid token
    
    Raises: 
        AccessError
        
    '''
    response_1 = requests.post(url + "dm/leave/v1",
                  json = {'token': -1,
                          'dm_id': dm_list[0]['dm_id']})
    assert response_1.status_code == AccessError.code
    
######################################## Test_dm/messages/v1 ########################################

def test_dm_messages_normal(login_list, dm_list):
    '''
    
    This tests is testing the normal situation of sending messages in 
    DMs

    Assumption:
        message/senddm/v1 is working well
        
    '''
    requests.post(url + 'message/senddm/v1',
                  json = {'token': login_list[0]['token'],
                          'dm_id': dm_list[0]['dm_id'],
                          'message': 'message1'})
    requests.post(url + 'message/senddm/v1',
                  json = {'token': login_list[0]['token'],
                          'dm_id': dm_list[0]['dm_id'],
                          'message': 'message2'})
    requests.post(url + 'message/senddm/v1',
                  json = {'token': login_list[0]['token'],
                          'dm_id': dm_list[0]['dm_id'],
                          'message': 'message3'})
    requests.post(url + 'message/senddm/v1',
                  json = {'token': login_list[0]['token'],
                          'dm_id': dm_list[0]['dm_id'],
                          'message': 'message4'})
    
    requests.post(url + 'message/senddm/v1',
                  json = {'token': login_list[1]['token'],
                          'dm_id': dm_list[2]['dm_id'],
                          'message': 'message1'})
    requests.post(url + 'message/senddm/v1',
                  json = {'token': login_list[1]['token'],
                          'dm_id': dm_list[2]['dm_id'],
                          'message': 'message2'})
    requests.post(url + 'message/senddm/v1',
                  json = {'token': login_list[1]['token'],
                          'dm_id': dm_list[2]['dm_id'],
                          'message': 'message3'})
    requests.post(url + 'message/senddm/v1',
                  json = {'token': login_list[1]['token'],
                          'dm_id': dm_list[2]['dm_id'],
                          'message': 'message4'})
    
    response_1 = requests.get(url + 'dm/messages/v1',
                              params = {'token': login_list[0]['token'],
                                        'dm_id': dm_list[0]['dm_id'],
                                        'start': 0}).json()
    response_2 = requests.get(url + 'dm/messages/v1',
                              params = {'token': login_list[1]['token'],
                                        'dm_id': dm_list[2]['dm_id'],
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

def test_dm_messages_more_messages(login_list, dm_list):
    '''
    
    This tests is to test when sending more than 50 messages, the end value is start +50
    
    Assumption:
        message/senddm/v1 is working well
        
    '''
    for i in range(55):
        # sending 55 messages in dm 0
        requests.post(url + 'message/senddm/v1',
                  json = {'token': login_list[0]['token'],
                          'dm_id': dm_list[0]['dm_id'],
                          'message': 'messages'})
    
    response_1 = requests.get(url + 'dm/messages/v1',
                              params = {'token': login_list[0]['token'],
                                        'dm_id': dm_list[0]['dm_id'],
                                        'start': 0}).json()
    
    for i in range(50):
        # test messages are correct
        assert response_1['messages'][i]['message'] == 'messages'
        
    # test start and end
    assert response_1['start'] == 0
    assert response_1['end'] == 50

def test_dm_messages_invalid_start(login_list, dm_list):
    '''
    
    Test dm messages with invalid start
    
    Parameters:
        login_list, dm_list
        
    Raises:
        InputError
        
    Assumption:
        message/senddm/v1
        
    '''
    # no messages
    response_1 = requests.get(url + 'dm/messages/v1',
                              params = {'token': login_list[0]['token'],
                                        'dm_id': dm_list[0]['dm_id'],
                                        'start': 10})
    assert response_1.status_code == InputError.code
    
    # 4 messages but start at 10
    requests.post(url + 'message/senddm/v1',
                  json = {'token': login_list[0]['token'],
                          'dm_id': dm_list[0]['dm_id'],
                          'message': 'message1'})
    requests.post(url + 'message/senddm/v1',
                  json = {'token': login_list[0]['token'],
                          'dm_id': dm_list[0]['dm_id'],
                          'message': 'message2'})
    requests.post(url + 'message/senddm/v1',
                  json = {'token': login_list[0]['token'],
                          'dm_id': dm_list[0]['dm_id'],
                          'message': 'message3'})
    requests.post(url + 'message/senddm/v1',
                  json = {'token': login_list[0]['token'],
                          'dm_id': dm_list[0]['dm_id'],
                          'message': 'message4'})
    response_2 = requests.get(url + 'dm/messages/v1',
                              params = {'token': login_list[0]['token'],
                                        'dm_id': dm_list[0]['dm_id'],
                                        'start': 10})
    assert response_2.status_code == InputError.code

def test_dm_messages_invalid_dm_id(login_list, dm_list):
    '''
    
    This test is for testing input invalid dm_id
    
    Parameters:
        login_list, dm_list
        
    Raises:
        InputError
        
    Assumption:
        message/senddm/v1
        
    '''
    new_id = random.randint(-65535, 65535)
    invalid_dm_id = []
    while len(invalid_dm_id) < 1:
        if not new_id in [dm_list[i]['dm_id'] for i in range(0,3)]:
            invalid_dm_id.append(new_id)
    requests.post(url + 'message/senddm/v1',
                  json = {'token': login_list[0]['token'],
                          'dm_id': dm_list[0]['dm_id'],
                          'message': 'message1'})
    requests.post(url + 'message/senddm/v1',
                  json = {'token': login_list[0]['token'],
                          'dm_id': dm_list[0]['dm_id'],
                          'message': 'message2'})
    requests.post(url + 'message/senddm/v1',
                  json = {'token': login_list[0]['token'],
                          'dm_id': dm_list[0]['dm_id'],
                          'message': 'message3'})
    requests.post(url + 'message/senddm/v1',
                  json = {'token': login_list[0]['token'],
                          'dm_id': dm_list[0]['dm_id'],
                          'message': 'message4'})
    response_1 = requests.get(url + 'dm/messages/v1',
                              params = {'token': login_list[0]['token'],
                                        'dm_id': invalid_dm_id[0],
                                        'start': 0})
    assert response_1.status_code == InputError.code

def test_dm_messages_user_not_in_dm(login_list, dm_list):
    '''
    
    This test is for testing input user isn't in dm
    
    Parameters:
        login_list, dm_list
        
    Raises:
        AccessError
        
    Assumption:
        message/senddm/v1
        
    '''
    # all normal
    requests.post(url + 'message/senddm/v1',
                  json = {'token': login_list[0]['token'],
                          'dm_id': dm_list[0]['dm_id'],
                          'message': 'message1'})
    requests.post(url + 'message/senddm/v1',
                  json = {'token': login_list[0]['token'],
                          'dm_id': dm_list[0]['dm_id'],
                          'message': 'message2'})
    requests.post(url + 'message/senddm/v1',
                  json = {'token': login_list[0]['token'],
                          'dm_id': dm_list[0]['dm_id'],
                          'message': 'message3'})
    requests.post(url + 'message/senddm/v1',
                  json = {'token': login_list[0]['token'],
                          'dm_id': dm_list[0]['dm_id'],
                          'message': 'message4'})
    response_1 = requests.get(url + 'dm/messages/v1',
                              params = {'token': login_list[3]['token'],
                                        'dm_id': dm_list[0]['dm_id'],
                                        'start': 0})
    assert response_1.status_code == AccessError.code
    
def test_dm_messages_invalid_user_token(login_list, dm_list):
    '''
    
    This test is for testing raises AccessError for invalid token
    Even if there are some InputError, raises AccessError at first
    
    Parameters:
        login_list, dm_list
        
    Raises:
        AccessError
        
    Assumption:
        message/senddm/v1
        
    '''
    new_id = random.randint(-65535, 65535)
    invalid_dm_id = []
    while len(invalid_dm_id) < 1:
        if not new_id in [dm_list[i]['dm_id'] for i in range(0,3)]:
            invalid_dm_id.append(new_id)
    # normal situation
    requests.post(url + 'message/senddm/v1',
                  json = {'token': login_list[0]['token'],
                          'dm_id': dm_list[0]['dm_id'],
                          'message': 'message1'})
    requests.post(url + 'message/senddm/v1',
                  json = {'token': login_list[0]['token'],
                          'dm_id': dm_list[0]['dm_id'],
                          'message': 'message2'})
    requests.post(url + 'message/senddm/v1',
                  json = {'token': login_list[0]['token'],
                          'dm_id': dm_list[0]['dm_id'],
                          'message': 'message3'})
    requests.post(url + 'message/senddm/v1',
                  json = {'token': login_list[0]['token'],
                          'dm_id': dm_list[0]['dm_id'],
                          'message': 'message4'})
    response_1 = requests.get(url + 'dm/messages/v1',
                              params = {'token': -1,
                                        'dm_id': dm_list[0]['dm_id'],
                                        'start': 0})
    assert response_1.status_code == AccessError.code
    
    # invalid start
    response_2 = requests.get(url + 'dm/messages/v1',
                              params = {'token': -1,
                                        'dm_id': dm_list[0]['dm_id'],
                                        'start': 10})
    assert response_2.status_code == AccessError.code
    
    # invalid dm_id
    response_3 = requests.get(url + 'dm/messages/v1',
                              params = {'token': -1,
                                        'dm_id': invalid_dm_id[0],
                                        'start': 0})
    assert response_3.status_code == AccessError.code
    
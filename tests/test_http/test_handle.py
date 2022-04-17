import pytest
import requests
from src.config import url


def test_handle_1():
    '''
    
    This test is to test some special situations of handle
    
    Assumption:
        auth/register/v2 is working well
        user/profile/v1 is working well
        
    '''
    requests.delete(f"{url}clear/v1", json = {})    # clear all info in server
    register_1 = requests.post(f"{url}auth/register/v2",
                               json = { 'email': 'z5374603@unsw.com',
                                        'password': '123456',
                                        'name_first': 'Steve',
                                        'name_last': 'Yang0'}).json()
    register_2 = requests.post(f"{url}auth/register/v2",
                               json = { 'email': 'z5374602@unsw.com',
                                        'password': '123456',
                                        'name_first': 'Steve',
                                        'name_last': 'Yang'}).json()
    response_1 = requests.get(url + "user/profile/v1", 
                              params = {
                                  'token': register_1['token'],
                                  'u_id': register_1['auth_user_id']
                              }).json()
    response_2 = requests.get(url + "user/profile/v1", 
                              params = {
                                  'token': register_2['token'],
                                  'u_id': register_2['auth_user_id']
                              }).json()
    assert response_1['user']['handle_str'] == 'steveyang0'
    assert response_2['user']['handle_str'] == 'steveyang1'
    
def test_handle_2():    
    '''
    
    This test is to test some special situations of handle
    
    Assumption:
        auth/register/v2 is working well
        user/profile/v1 is working well
        
    '''
    requests.delete(f"{url}clear/v1", json = {})    # clear all info in server
    register_3 = requests.post(f"{url}auth/register/v2",
                               json = { 'email': 'z5374601@unsw.com',
                                        'password': '123456',
                                        'name_first': 'Stev',
                                        'name_last': 'Yang01'}).json()
    register_4 = requests.post(f"{url}auth/register/v2",
                               json = { 'email': 'z5374600@unsw.com',
                                        'password': '123456',
                                        'name_first': 'Stev',
                                        'name_last': 'Yang01'}).json()
    response_3 = requests.get(url + "user/profile/v1", 
                              params = {
                                  'token': register_3['token'],
                                  'u_id': register_3['auth_user_id']
                              }).json()
    response_4 = requests.get(url + "user/profile/v1", 
                              params = {
                                  'token': register_4['token'],
                                  'u_id': register_4['auth_user_id']
                              }).json()
    assert response_3['user']['handle_str'] == 'stevyang01'
    assert response_4['user']['handle_str'] == 'stevyang02'
    
def test_handle_3():    
    '''
    
    This test is to test some special situations of handle
    
    Assumption:
        auth/register/v2 is working well
        user/profile/v1 is working well
        
    '''
    requests.delete(f"{url}clear/v1", json = {})    # clear all info in server
    register_5 = requests.post(f"{url}auth/register/v2",
                               json = { 'email': 'z537460@unsw.com',
                                        'password': '123456',
                                        'name_first': 'Stevee',
                                        'name_last': 'Yang16'}).json()
    register_6 = requests.post(f"{url}auth/register/v2",
                               json = { 'email': 'z537@unsw.com',
                                        'password': '123456',
                                        'name_first': 'Stevee',
                                        'name_last': 'Yang16'}).json()
    response_5 = requests.get(url + "user/profile/v1", 
                              params = {
                                  'token': register_5['token'],
                                  'u_id': register_5['auth_user_id']
                              }).json()
    response_6 = requests.get(url + "user/profile/v1", 
                              params = {
                                  'token': register_6['token'],
                                  'u_id': register_6['auth_user_id']
                              }).json()
    assert response_5['user']['handle_str'] == 'steveeyang16'
    assert response_6['user']['handle_str'] == 'steveeyang17'
    
def test_handle_4(): 
    '''
    
    This test is to test some special situations of handle
    
    Assumption:
        auth/register/v2 is working well
        user/profile/v1 is working well
        
    '''
    requests.delete(f"{url}clear/v1", json = {})    # clear all info in server
    register_1 = requests.post(f"{url}auth/register/v2",
                               json = { 'email': 'z5374603@unsw.com',
                                        'password': '123456',
                                        'name_first': 'Steve',
                                        'name_last': 'Yang'}).json()
    register_2 = requests.post(f"{url}auth/register/v2",
                               json = { 'email': 'z5374602@unsw.com',
                                        'password': '123456',
                                        'name_first': 'Steve',
                                        'name_last': 'Yang'}).json()
    register_3 = requests.post(f"{url}auth/register/v2",
                               json = { 'email': 'z5374601@unsw.com',
                                        'password': '123456',
                                        'name_first': 'Steve',
                                        'name_last': 'Yang'}).json()
    response_1 = requests.get(url + "user/profile/v1", 
                              params = {
                                  'token': register_1['token'],
                                  'u_id': register_1['auth_user_id']
                              }).json()
    response_2 = requests.get(url + "user/profile/v1", 
                              params = {
                                  'token': register_2['token'],
                                  'u_id': register_2['auth_user_id']
                              }).json()
    response_3 = requests.get(url + "user/profile/v1", 
                              params = {
                                  'token': register_3['token'],
                                  'u_id': register_3['auth_user_id']
                              }).json()
    assert response_1['user']['handle_str'] == 'steveyang'
    assert response_2['user']['handle_str'] == 'steveyang0'
    assert response_3['user']['handle_str'] == 'steveyang1'
    
def test_handle_5(): 
    '''
    
    This test is to test some special situations of handle
    
    Assumption:
        auth/register/v2 is working well
        user/profile/v1 is working well
        
    '''
    requests.delete(f"{url}clear/v1", json = {})    # clear all info in server
    register_1 = requests.post(f"{url}auth/register/v2",
                               json = { 'email': 'z5374603@unsw.com',
                                        'password': '123456',
                                        'name_first': 'Steve',
                                        'name_last': 'Yang15'}).json()
    register_2 = requests.post(f"{url}auth/register/v2",
                               json = { 'email': 'z5374602@unsw.com',
                                        'password': '123456',
                                        'name_first': 'Steve',
                                        'name_last': 'Yang156'}).json()
    register_3 = requests.post(f"{url}auth/register/v2",
                               json = { 'email': 'z5374601@unsw.com',
                                        'password': '123456',
                                        'name_first': 'Steve',
                                        'name_last': 'Yang15'}).json()
    response_1 = requests.get(url + "user/profile/v1", 
                              params = {
                                  'token': register_1['token'],
                                  'u_id': register_1['auth_user_id']
                              }).json()
    response_2 = requests.get(url + "user/profile/v1", 
                              params = {
                                  'token': register_2['token'],
                                  'u_id': register_2['auth_user_id']
                              }).json()
    response_3 = requests.get(url + "user/profile/v1", 
                              params = {
                                  'token': register_3['token'],
                                  'u_id': register_3['auth_user_id']
                              }).json()
    assert response_1['user']['handle_str'] == 'steveyang15'
    assert response_2['user']['handle_str'] == 'steveyang156'
    assert response_3['user']['handle_str'] == 'steveyang157'
    
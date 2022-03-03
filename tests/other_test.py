
import pytest
from src.other import clear_v1
from src.data_store import data_store

# adding user and channel and test if clear_v1 resets it
def clear_v1_test():
    store = data_store.get()
    store['users'].append("users_test")      
    store['channels'].append('chann_test')
    store['messages'].append("msg_test")

    clear_v1()
    assert store['users'] == []
    assert store['channels'] == []
    assert store['messages'] == []
    
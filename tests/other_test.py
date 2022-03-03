
import pytest
from src.other import clear_v1
from src.data_store import data_store

def clear_v1_test():
    store = data_store.get()
    users = store['users']
    chann = store['channels']
    users.append("users_test")
    chann.append('chann_test')
    clear_v1()
    assert store['users'] == []
    assert store['channels'] == []
    
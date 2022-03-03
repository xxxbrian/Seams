from src.data_store import data_store

# resets all data
# subject to change if dictionary keys expand in the initial object from data_store.py

def clear_v1():
    store = data_store.get()
    store['users'] = []
    store['channels'] = []
    store['messages'] = []
    data_store.set(store)

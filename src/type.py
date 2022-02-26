from src import data_store
from data_store import data_store

store = data_store.get()


class User():

    def __init__(self, email, password, name_first, name_last) -> None:
        self.email = email
        self.password = password
        self.name_first = name_first
        self.name_last = name_last
        self.handle = self.generat_handle()

from curses.ascii import US
from plistlib import UID
from src import data_store
from data_store import data_store

store = data_store.get()


class User():

    def __init__(self, email, password, name_first, name_last) -> None:
        '''
        
        '''
        self.u_id = User.get_last_uid()
        self.email = email
        self.password = password
        self.name_first = name_first
        self.name_last = name_last
        self.handle = self.generat_handle()

    @staticmethod
    def find_by_uid(u_id):
        return User

    @staticmethod
    def get_last_uid() -> int:
        users = store['users'].reverse()
        u_id = users[0].u_id if len(users) > 0 else 0
        return u_id

import re
import string
import jwt
import hashlib
import time
import pickle
import os

from src.data_store import data_store

from src.config import SECRET

store = data_store.get()


def pickelsave(func):

    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        with open('data_store.pickle', 'wb') as f:
            pickle.dump(store, f)
        return result

    return wrapper


class User():
    '''
    Every user will be store in data_store:[(object) Datastore] as an User object

    Attributes:
        u_id:        (int) user's auth id
        email:       (str) user's email
        password:    (str) user's password
        name_first:  (str) user's first name
        name_last:   (str) user's last name
        handle_str:      (str) generated by user's name

    Example usage:
        # Import
        from src.type import User

        # Instantiate a User object
        new_user = User(email, password, name_first, name_last)

        # Store user to store
        new_user.add_to_store()

        # Find user by u_id
        myuser = User.find_by_id(u_id)
    '''

    def __init__(self, email: str, password: str, name_first: str,
                 name_last: str) -> None:
        self.u_id = User.get_last_id() + 1
        self.email = email
        self.password = User.encrypt(password)
        self.name_first = name_first
        self.name_last = name_last
        self.handle_str = self.generat_handle()
        self.group_id = 500 if self.u_id else 0
        self.notification = []

    # def __setattr__(self, key, value):
    #     self.__dict__[key] = value

    # COVERAGE
    def __str__(self):
        info = 'User object:\n'+\
            f' - u_id:       {self.u_id}\n' + \
            f' - email:      {self.email}\n' + \
            f' - password:   {self.password}\n' + \
            f' - name:       {self.name_first} {self.name_last}\n' + \
            f' - handle:     {self.handle_str}\n' + \
            f' - group_id:   {self.group_id}'
        return info

    def todict(self,
               show={'u_id', 'email', 'name_first', 'name_last',
                     'handle_str'}):
        return {
            key: value
            for key, value in self.__dict__.items() if key in show
        }

    @staticmethod
    def find_by_id(u_id: int, only_active=True):
        '''
        Find user by user's u_id

        Args:
            u_id

        Return:
            user
        '''

        for user in store['users']:
            if user.u_id == u_id and (not only_active or user.is_active()):
                return user
        return None

    @staticmethod
    def find_by_email(email: str, only_active=True):
        '''
        Find user by user's email

        Args:
            email

        Return:
            User
        '''

        for user in store['users']:
            if user.email == email and (not only_active or user.is_active()):
                return user
        return None

    @staticmethod
    def clear() -> None:
        """clear user"""
        store['users'].clear()
        store['login_token'].clear()

    @staticmethod
    def get_last_id() -> int:
        """return last user id"""
        users = list(reversed(store['users']))
        u_id = users[0].u_id if len(users) > 0 else -1
        return u_id

    def add_to_store(self) -> None:
        """add user"""
        store['users'].append(self)

    @staticmethod
    def __generat_20fullname(name_first: str, name_last: str) -> str:
        """generate 20 lowercase full names"""

        fullname = (name_first + name_last).lower()
        fullname = ''.join(list(filter(str.isalnum, fullname)))[:20]
        return fullname

    @staticmethod
    def __generat_fullname_text(fullname) -> str:
        fullname_text = ''
        for i in range(len(fullname)):
            if fullname[i:].isdigit() and int(fullname[i]) != 0:
                break
            fullname_text += fullname[i]
        if len(fullname_text) == len(fullname):
            return fullname.rstrip(string.digits)
        else:
            return fullname_text

    def generat_handle(self) -> str:
        fullname = self.__generat_20fullname(self.name_first, self.name_last)
        fullname_text = self.__generat_fullname_text(fullname)
        fullname_digits = -1
        if len(fullname_text) != len(fullname):
            fullname_digits = int(fullname[len(fullname_text):])

        for user in list(reversed([i for i in store['users']
                                   if i.is_active()])):
            last_text = user.handle_str[:len(fullname_text)]
            last_digit_str = user.handle_str[len(fullname_text):]
            last_digit = int(
                last_digit_str) if last_digit_str.isdigit() else -1
            if fullname_text == last_text and (last_digit_str.isdigit()
                                               or last_digit_str == ''):
                fullname_digits = max(last_digit + 1, fullname_digits)

        if fullname_digits >= 0:
            fullname_text += str(fullname_digits)

        return fullname_text

    def generat_token(self) -> str:
        payload = {
            'u_id': self.u_id,
            'exp': int(time.time() * 1000000),
        }
        token = jwt.encode(payload=payload, key=SECRET, algorithm='HS256')
        store['login_token'].append(token)
        return token

    @staticmethod
    def find_by_token(token):
        if User.token_in_store(token):
            preload = jwt.decode(token, SECRET, algorithms=['HS256'])
            return User.find_by_id(preload['u_id'])
        return None

    @staticmethod
    def token_in_store(token):
        return token in store['login_token']

    @staticmethod
    def remove_token(token):
        store['login_token'].remove(token)

    @staticmethod
    def find_all():
        return [i for i in store['users'] if i.is_active()]

    def del_account(self):
        self.group_id = -1
        self.name_first = 'Removed'
        self.name_last = 'user'
        for msg in store['messages']:
            if msg.u_id == self.u_id:
                msg.content = 'Removed user'

    def is_active(self):
        return self.group_id >= 0

    def is_admin(self):
        return self.group_id == 0

    @staticmethod
    def check_handle_been_used(handle_str: str) -> bool:
        all_handle = [user.handle_str for user in store['users']]
        return handle_str in all_handle

    @staticmethod
    def check_handle_content_invalid(handle_str: str) -> bool:
        return not handle_str.isalnum()

    @staticmethod
    def check_handle_length_invalid(handle_str: str) -> bool:
        return len(handle_str) < 3 or len(handle_str) > 20

    @staticmethod
    def check_email_invalid(email: str) -> bool:
        """Check whether the email address is valid"""
        regx = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'
        return not re.fullmatch(regx, email)

    @staticmethod
    def check_email_been_used(email: str) -> bool:
        """Check whether the user's email is been used"""
        return User.find_by_email(email) is not None

    @staticmethod
    def check_password_invalid(password: str) -> bool:
        """Check whether the password is satisfy the length request"""
        return len(password) < 6

    @staticmethod
    def check_name_invalid(name: str) -> bool:
        """Check whether the length of user name is satisfy length request"""
        return len(name) < 1 or len(name) > 50

    @staticmethod
    def match_email_password(email: str, password: str):
        """Check whether the input email and password are match"""
        user = User.find_by_email(email)
        return user.password == User.encrypt(password)

    @staticmethod
    def encrypt(password: str):
        return hashlib.sha256(password.encode()).hexdigest()

    def add_notification(self, notification):
        self.notification.insert(0, notification)

    def get_notification(self):
        return self.notification


class Channel():
    '''
    Every channel will be store in data_store:[(object) Datastore] as an Channel object

    Attributes:
        name:         (str)   channel's name
        owners:       (list)  channel's owners
        members:      (list)  channel's members
        channel_id:   (int)   channel's id
        is_public:    (bool)  channel is public or not

    Example usage:
        # Import
        from src.type import Channel

        # Instantiate a Channel object
        new_channel = Channel(u_id, name, is_public)

        # Store channel to store
        new_channel.add_to_store()
    '''

    def __init__(self, u_id: int, name: str, is_public: bool = True) -> None:
        self.name = name
        self.owners = [User.find_by_id(u_id)]
        self.members = [User.find_by_id(u_id)]
        self.channel_id = Channel.get_last_id() + 1
        self.is_public = is_public
        self.messages = []

    # def __setattr__(self, key, value):
    #     self.__dict__[key] = value

    # COVERAGE
    def __str__(self):
        channel_type = 'public' if self.is_public else 'privte'
        info = 'Channel object:\n'+\
            f' - name:        {self.name}\n'+\
            f' - channel_id:  {self.channel_id}\n'+\
            f' - type:        {channel_type}\n'+\
            f' - members:     {len(self.members)} ({len(self.owners)}owners)'
        return info

    def todict(self, show={'channel_id', 'name', 'is_public'}):
        info_dict = {
            key: value
            for key, value in self.__dict__.items() if key in show
        }
        if 'owner_members' in show:
            info_dict['owner_members'] = list(user.todict()
                                              for user in self.owners
                                              if user.is_active())
        if 'all_members' in show:
            info_dict['all_members'] = list(user.todict()
                                            for user in self.members
                                            if user.is_active())

        return info_dict

    @staticmethod
    def get_last_id() -> int:
        channel = list(reversed(store['channels']))
        channel_id = channel[0].channel_id if len(channel) > 0 else -1
        return channel_id

    @staticmethod
    def find_by_id(channel_id):
        '''
        Find channel by channel's channel_id

        Args:
            channel_id

        Return:
            Channel
        '''

        for channel in store['channels']:
            if channel.channel_id == channel_id:
                return channel
        return None

    @staticmethod
    def clear() -> None:
        store['channels'].clear()

    def add_to_store(self) -> None:
        store['channels'].append(self)

    def has_user(self, user: User) -> bool:
        return user in self.members

    def addowner(self, user: User) -> None:
        self.owners.append(user)

    def removeowner(self, user: User) -> None:
        self.owners.remove(user)

    def leave(self, user: User) -> None:
        self.members.remove(user)

    def join(self, user: User) -> None:
        self.members.append(user)

    @staticmethod
    def check_name_invalid(name: str) -> bool:
        """
        Check whether the length of channel name is satisfy length request
        """
        return len(name) < 1 or len(name) > 20

    @staticmethod
    def get_all() -> list:
        return store['channels']

    def get_messages(self, start: int, end: int) -> list:
        all_message = [msg for msg in self.messages if msg.is_active]
        end = len(all_message) if end < 0 else end
        return all_message[start:end]

    def add_message(self, msg):
        self.messages.insert(0, msg)

    def has_owner(self, user: User):
        return user in self.owners or user.is_admin()


class DM():

    def __init__(self, u_id: int, u_ids: list) -> None:
        self.name = self.generat_name(u_ids)
        self.owner = User.find_by_id(u_id)
        self.members = [User.find_by_id(u_id) for u_id in u_ids]
        self.dm_id = DM.get_last_id() + 1
        self.messages = []
        self.is_active = True

    # def __setattr__(self, key, value):
    #     self.__dict__[key] = value

    # COVERAGE
    def __str__(self):
        info = 'DM object:\n'+\
            f' - name:        {self.name}\n'+\
            f' - DM_id:       {self.dm_id}\n'+\
            f' - owner:       id({self.owner.u_id})\n'+\
            f' - members:     {len(self.members)}'
        return info

    def todict(self, show={'dm_id', 'name'}):
        info_dict = {
            key: value
            for key, value in self.__dict__.items() if key in show
        }
        if 'owner' in show:
            info_dict['owner'] = self.owner.todict()
        if 'members' in show:
            info_dict['members'] = list(user.todict() for user in self.members
                                        if user.is_active())

        return info_dict

    @staticmethod
    def get_last_id() -> int:
        dm = list(reversed(store['dms']))
        dm_id = dm[0].dm_id if len(dm) > 0 else -1
        return dm_id

    def generat_name(self, u_ids: list) -> str:
        name_list = [User.find_by_id(u_id).handle_str for u_id in u_ids]
        name_list.sort()
        return ', '.join(name_list)

    @staticmethod
    def find_by_id(dm_id):
        '''
        Find dm by dm's dm_id

        Args:
            dm_id

        Return:
            DM
        '''

        for dm in store['dms']:
            if dm.dm_id == dm_id and dm.is_active:
                return dm
        return None

    @staticmethod
    def clear() -> None:
        store['dms'].clear()

    def add_to_store(self) -> None:
        store['dms'].append(self)

    def has_user(self, user: User) -> bool:
        return user in self.members

    def leave(self, user: User) -> None:
        self.members.remove(user)

    def get_messages(self, start: int, end: int) -> list:
        all_message = [msg for msg in self.messages if msg.is_active]
        end = len(all_message) if end < 0 else end
        return all_message[start:end]

    @staticmethod
    def get_all() -> list:
        return [dm for dm in store['dms'] if dm.is_active]

    def add_message(self, msg):
        self.messages.insert(0, msg)

    def has_owner(self, user: User):
        return user is self.owner

    def remove(self):
        self.is_active = False


class Message():

    def __init__(self, u_id: int, content: str, time_sent: int, sup) -> None:
        self.message_id = Message.get_last_id() + 1
        self.u_id = u_id
        self.sender = User.find_by_id(u_id)
        self.content = content
        self.time_sent = time_sent
        self.is_active = True
        self.sup = sup
        self.react_dict = {1: []}
        self.is_pinned = False

    def __setattr__(self, key, value):
        self.__dict__[key] = value

    def todict(self,
               show={
                   'message_id', 'u_id', 'message', 'time_sent', 'reacts',
                   'is_pinned'
               },
               auth_user=None):
        info_dict = {
            key: value
            for key, value in self.__dict__.items() if key in show
        }
        if 'message' in show:
            info_dict['message'] = self.content
        if 'reacts' in show:
            # for id, users in self.react_dict.values():
            #     {'react_id':id,'u_ids':[user.u_id for user in users],'is_this_user_reacted':auth_user in users}
            info_dict['reacts'] = [{
                'react_id': id,
                'u_ids': [user.u_id for user in users],
                'is_this_user_reacted': auth_user in users
            } for id, users in self.react_dict.items()]
        return info_dict

    @staticmethod
    def get_last_id() -> int:
        msg = store['messages']
        message_id = msg[0].message_id if len(msg) > 0 else -1
        return message_id

    @staticmethod
    def find_by_id(message_id):
        '''
        Find message by message's message_id

        Args:
            message

        Return:
            Message
        '''
        for msg in store['messages']:
            if msg.message_id == message_id and msg.is_active:
                return msg
        return None

    @staticmethod
    def clear() -> None:
        store['messages'].clear()

    def add_to_store(self) -> None:
        store['messages'].insert(0, self)
        self.sup.add_message(self)
        # if type(self.sup) is Channel:
        #     self.add_to_channel(self.sup)
        # if type(self.sup) is DM:
        #     self.add_to_dm(self.sup)

    # def add_to_channel(self, channel: Channel) -> None:
    #     channel.messages.insert(0, self)

    # def add_to_dm(self, dm: DM) -> None:
    #     dm.messages.insert(0, self)

    @staticmethod
    def check_length_invalid(msg: str) -> bool:
        return len(msg) < 1 or len(msg) > 1000

    def remove(self):
        self.is_active = False

    @staticmethod
    def check_query_str_invalid(query_str: str) -> bool:
        return len(query_str) < 1 or len(query_str) > 1000


class Notification:

    def __init__(self, sup, content: str) -> None:
        self.sup = sup
        self.content = content

    def todict(self, show={'channel_id', 'dm_id', 'notification_message'}):
        info_dict = {
            key: value
            for key, value in self.__dict__.items() if key in show
        }
        if 'channel_id' in show:
            info_dict['channel_id'] = self.sup.channel_id if type(
                self.sup) is Channel else -1
        if 'dm_id' in show:
            info_dict['dm_id'] = self.sup.dm_id if type(self.sup) is DM else -1
        if 'notification_message' in show:
            info_dict['notification_message'] = self.content
        return info_dict


if os.path.exists('data_store.pickle'):
    with open('data_store.pickle', 'rb') as f:
        store = pickle.load(f)
    print('Reload Cache...')
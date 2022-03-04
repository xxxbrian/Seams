from src.data_store import data_store

import re

store = data_store.get()


class User():
    '''
    Every user will be store in data_store:[(object) Datastore] as an User object

    Attributes:
        u_id:        (int) user's auth id
        email:       (str) user's email
        password:    (str) user's password
        name_first:  (str) user's first name
        name_last:   (str) user's last name
        handle:      (str) generated by user's name
    
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
        self.password = password
        self.name_first = name_first
        self.name_last = name_last
        self.handle_str = self.generat_handle()

    def __str__(self):
        info = 'User object:\n'+\
            f' - u_id:     {self.u_id}\n'+\
            f' - email:    {self.email}\n'+\
            f' - password: {self.password}\n'+\
            f' - name:     {self.name_first} {self.name_first}\n'+\
            f' - handle:   {self.handle_str}'
        return info

    def todict(self,
               show={'u_id', 'email', 'name_first', 'name_last',
                     'handle_str'}):
        return {
            key: value
            for key, value in self.__dict__.items() if key in show
        }

    @staticmethod
    def find_by_id(u_id: int):
        '''

        Find user by user's u_id

        Args: 
            u_id

        Return:
            User
        '''
        for user in store['users']:
            if user.u_id == u_id:
                return user
        return None

    @staticmethod
    def find_by_email(email: str):
        '''

        Find user by user's email

        Args: 
            email

        Return:
            User
        '''
        for user in store['users']:
            if user.email == email:
                return user
        return None

    @staticmethod
    def clear() -> None:
        store['users'] = []

    @staticmethod
    def get_last_id() -> int:
        users = list(reversed(store['users']))
        u_id = users[0].u_id if len(users) > 0 else -1
        return u_id

    def add_to_store(self) -> None:
        store['users'].append(self)

    @staticmethod
    def generat_20fullname(name_first: str, name_last: str) -> str:
        fullname = (name_first + name_last).lower()
        fullname = ''.join(list(filter(str.isalnum, fullname)))[:20]
        return fullname

    def generat_handle(self) -> str:
        fullname = self.generat_20fullname(self.name_first, self.name_last)

        lastend = ''
        for user in list(reversed(store['users'])):
            if self.generat_20fullname(user.name_first,
                                       user.name_last) == fullname:
                lastend = user.handle[(len(fullname)):]
                break

        lastend = str(int(lastend) + 1) if lastend != '' else lastend
        return fullname + lastend

    @staticmethod
    def check_email_invalid(email: str) -> bool:
        """
        Check whether the email address is valid
        """
        regx = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'
        return not re.fullmatch(regx, email)

    @staticmethod
    def check_email_been_used(email: str) -> bool:
        """
        Check whether the user's email is been used
        """
        return (User.find_by_email(email) != None)

    @staticmethod
    def check_password_invalid(password: str) -> bool:
        """
        Check whether the password is satisfy the length request
        """
        return len(password) < 6

    @staticmethod
    def check_name_invalid(name: str) -> bool:
        """
        Check whether the length of user name is satisfy length request
        """
        return len(name) < 1 or len(name) > 50

    @staticmethod
    def match_email_password(email: str, password: str):
        """
        Check whether the input email and password are match
        """
        user = User.find_by_email(email)
        if user:
            return user.password == password
        return False


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
        self.channel_id = Channel.get_last_id()
        self.is_public = is_public
        self.messages = []

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
                                              for user in self.owners)
        if 'all_members' in show:
            info_dict['all_members'] = list(user.todict()
                                            for user in self.members)

        return info_dict

    @staticmethod
    def get_last_id() -> int:
        users = list(reversed(store['channels']))
        channel_id = users[0].channel_id if len(users) > 0 else 0
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
        store['channels'] = []

    def add_to_store(self) -> None:
        store['channels'].append(self)

    def has_user(self, user: User) -> bool:
        return user in self.members

    def join(self, user: User) -> None:
        self.members.append(user)

    @staticmethod
    def check_name_invalid(name: str) -> bool:
        """
        Check whether the length of channel name is satisfy length request
        """
        return len(name) < 1 or len(name) > 20

    @staticmethod
    def get_allchannel() -> list:
        """
        Check whether the length of user is satisfy length request
        """
        return store['channels']

    def get_messages(self, start: int, end: int) -> list:
        end = len(self.messages) if end < 0 else end
        return self.messages[start:end]


class Message():

    def __init__(self, u_id: int, content: str, time_sent: int) -> None:
        self.message_id = Message.get_last_id() + 1
        self.u_id = u_id
        self.content = content
        self.time_sent = time_sent

    def todict(self, show={'message_id', 'u_id', 'message', 'time_sent'}):
        info_dict = {
            key: value
            for key, value in self.__dict__.items() if key in show
        }
        if 'message' in show:
            info_dict['message'] = list(content.todict()
                                        for content in self.content)

    def get_last_id() -> int:
        users = list(reversed(store['messages']))
        channel_id = users[0].channel_id if len(users) > 0 else 0
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
        store['messages'] = []

    def add_to_store(self) -> None:
        store['messages'].append(self)

    def add_to_channel(self, channel: Channel) -> None:
        channel.messages.append(self)
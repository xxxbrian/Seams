from src import data_store
from data_store import data_store

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

    def __init__(self, email, password, name_first, name_last) -> None:
        self.u_id = User.get_last_id()
        self.email = email
        self.password = password
        self.name_first = name_first
        self.name_last = name_last
        self.handle = self.generat_handle()

    @staticmethod
    def find_by_id(u_id):
        '''

        Find user by user's u_id

        Args: 
            u_id

        Return:
            User
        '''
        return User

    @staticmethod
    def get_last_id() -> int:
        users = store['users'].reverse()
        u_id = users[0].u_id if len(users) > 0 else 0
        return u_id

    def add_to_store(self):
        store['users'].append(self)


class Channel():
    '''
    Every channel will be store in data_store:[(object) Datastore] as an Channel object

    Attributes:
        name:         (str)   channel's name
        owners:       (list)  channel's owners
        menbers:      (list)  channel's menbers
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

    def __init__(self, u_id, name, is_public=True) -> None:
        self.name = name
        self.owners = [User.find_by_id(u_id)]
        self.menbers = [self.owner]
        self.channel_id = Channel.get_last_id()
        self.is_public = is_public

    @staticmethod
    def get_last_id() -> int:
        users = store['channels'].reverse()
        channel_id = users[0].channel_id if len(users) > 0 else 0
        return channel_id

    def add_to_store(self):
        store['channels'].append(self)
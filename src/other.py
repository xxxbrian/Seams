from src.type import User, Channel, Message

def clear_v1():
    """Resets the internal data of the application
        to its initial state"""

    User.clear()
    Channel.clear()
    Message.clear()
    return {}

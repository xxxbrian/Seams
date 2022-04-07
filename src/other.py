from src.type import User, Channel, DM, Message
from src.type import pickelsave


@pickelsave
def clear_v1():
    """Resets the internal data of the application
        to its initial state"""
    User.clear()
    Channel.clear()
    DM.clear()
    Message.clear()
    return {}

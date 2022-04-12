from src.type import Seams, User, Channel, DM, Message
from src.type import pickelsave


@pickelsave
def clear_v1():
    """Resets the internal data of the application
        to its initial state"""
    Seams.clear()
    User.clear()
    Channel.clear()
    DM.clear()
    Message.clear()
    return {}

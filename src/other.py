from src.type import User, Channel, Message

# resets all data


def clear_v1():
    User.clear()
    Channel.clear()
    Message.clear()

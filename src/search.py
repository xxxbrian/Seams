from src.type import User, Channel, DM, Message
from src.error import InputError, AccessError
from functools import reduce


def search_v1(token, query_str: str):
    user = User.find_by_token(token)
    if user is None:
        raise AccessError(description='Permission denied')
    if Message.check_query_str_invalid(query_str):
        raise InputError(description='query_str length invalid')
    msg_lists = [
        sup.messages for sup in Channel.get_all() + DM.get_all()
        if sup.has_user(user)
    ]
    all_msgs = reduce(lambda x, y: x + y, msg_lists)
    return {
        'messages': [
            msg.todict() for msg in all_msgs
            if query_str.lower() in msg.content.lower()
        ]
    }

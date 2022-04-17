from src.type import User, Channel, DM, Message, Notification
from src.error import InputError, AccessError


def notifications_get_v1(token):
    user = User.find_by_token(token)
    if user is None:
        raise AccessError(description='Permission denied')
    nfs = user.get_notification()
    print(f'cov-{[nf.todict({}) for nf in nfs[0:20]]}')
    return {'notifications': [nf.todict() for nf in nfs[0:20]]}

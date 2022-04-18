from src.type import User, Channel, DM, Message, Notification
from src.error import InputError, AccessError


def notifications_get_v1(token):
    """Return the user's most recent 20 notifications, 
    ordered from most recent to least recent.

    Args:
        token (str): user's token

    Raises:
        AccessError: if token is invalid

    Returns:
        dict: dictionary of notifications
    """
    user = User.find_by_token(token)
    if user is None:
        raise AccessError(description='Permission denied')
    nfs = user.get_notification()
    print(f'cov-{[nf.todict({}) for nf in nfs[0:20]]}')
    return {'notifications': [nf.todict() for nf in nfs[0:20]]}

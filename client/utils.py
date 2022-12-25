import json
from socket import socket
import time
from client.settings import ENCODING

def get_unix_time_utf() -> float:
    """
    текущее время UTC в формате unix timestamp
    :return: UTC time
    """
    return time.time() + time.altzone


def send_msg(soc: socket, data: dict):
    jim = json.dumps(data)
    soc.send(jim.encode(ENCODING))


def read_msg(msg: bytes):
    try:
        jim = msg.decode(ENCODING)
        data = json.loads(jim)
        return data
    except UnicodeDecodeError as err:
        print(err)
    except json.decoder.JSONDecodeError as err:
        print(err)


def auth_user_msg(user: str, password: str):
    # print(user, password)
    # После подключения при необходимости авторизации клиент должен отправить сообщение с
    # логином/паролем, например:
    # {
    #     "action": "authenticate",
    #     "time": "<unix timestamp>",
    #     "user": {"account_name": "user1",
    #              "password": "mySUperPasssword"}
    # }
    return {
        "action": "authenticate",
        "time": get_unix_time_utf(),
        "user": {"account_name": user,
                 "password": password}
    }


def presence_msg(user: str) -> dict:
    # Каждый пользователь при подключении к серверу отсылает сервисное сообщение о присутствии —
    # presence с необязательным полем type:
    # {
    #     "action": "presence",
    #     "time": "<unix timestamp>",
    #     "type": "status",
    #     "user": {"account_name": "user1",
    #              "status": "Yep, I am here!"}
    # }
    return {
        "action": "presence",
        "time": get_unix_time_utf(),
        "type": "status",
        "user": {"account_name": user,
                 "status": "Yep, I am here!"}
    }


def quit_user_msg(user: str):
    return {
        "action": "quit",
        "time": get_unix_time_utf(),
        "user": {"account_name": user}
    }

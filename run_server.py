import argparse
import os
from socket import socket, AF_INET, SOCK_STREAM
from typing import Tuple

from server.settings import (DEFAULT_ADDRESS, DEFAULT_PORT,
                             MAX_CONNECTIONS, MAX_PACKAGE_LENGTH,
                             SERVER_LOGGER)
from server.utils import send_msg, read_msg, presence, check_auth, quit_user
from server.decorators import log


@log
def get_settings() -> Tuple[str, int]:
    parser = argparse.ArgumentParser(prog='run_server',
                                     description='Run server',
                                     epilog='epilog my progs'
                                     )
    parser.add_argument('-p', '-port', type=int, dest='port',
                        default=DEFAULT_PORT,
                        metavar='<port>',
                        help='port 1024...65535 (default: %(default)s)')
    parser.add_argument('-a', '-addr', dest='addr',
                        type=str,
                        default=DEFAULT_ADDRESS,
                        metavar='<address>',
                        help='hostname or ip address (default: %(default)s)')
    args = parser.parse_args()
    if not (1024 <= args.port <= 65535):
        SERVER_LOGGER.warning(f'port: {str(args.port)}')
        print('введите значение port в диапазоне 1024...65535')
        exit(1)
    SERVER_LOGGER.debug(f'address: {str(args.addr)}, port: {str(args.port)}')
    return args.addr, args.port


@log
def accept_connections(s: socket) -> None:
    auth_users = set()
    # print('connected users:', *auth_users)
    while True:
        conn, addr = s.accept()
        # print(f"Connected by {addr}")
        SERVER_LOGGER.debug(f'Connected by {str(addr)}')
        try:
            while True:
                income_data = conn.recv(MAX_PACKAGE_LENGTH)
                # print(income_data)
                if income_data:
                    SERVER_LOGGER.debug(f'income_data: {str(income_data)}')
                    data = read_msg(income_data)
                    SERVER_LOGGER.debug(f'data: {str(data)}')
                    if data.get('action'):
                        if data.get('action') == 'authenticate':
                            res = check_auth(data.get('user'), auth_users)
                            # print('res:', res)
                            response, user = res
                            if user:
                                auth_users.add(user)
                                connected_msg = f'{user} connected'
                                print(connected_msg)
                                SERVER_LOGGER.debug(connected_msg)
                            send_msg(conn, response)
                            # print('connected users:', *auth_users)
                            SERVER_LOGGER.debug(f'connected users: {auth_users}')
                        elif data.get('action') == 'presence':
                            # print(presence(data))
                            presence_data = presence(data)
                            SERVER_LOGGER.info(f'{presence_data}')
                        elif data.get('action') == 'msg':
                            print('Пока не реализована')
                        elif data.get('action') == 'join':
                            print('Пока не реализована')
                        elif data.get('action') == 'leave':
                            print('Пока не реализована')
                        elif data.get('action') == 'quit':
                            # print('connected users:', *auth_users)
                            user_quit = quit_user(data.get('user'), auth_users)
                            # print(user_quit)
                            if user_quit:
                                auth_users.remove(user_quit)
                                print(user_quit, 'disconnected')
                                SERVER_LOGGER.info(f'{user_quit} disconnected')
                                conn.close()
                                break
        except Exception as err:
            # print(err)
            SERVER_LOGGER.exception(f'exception: {err}')
        finally:
            conn.close()


@log
def create_socket(address_port: Tuple[str, int]) -> None:
    # Создает сокет TCP:
    s = socket(AF_INET, SOCK_STREAM)

    try:
        # привязываем адрес и порт:
        s.bind(address_port)
        # прослушиваем соединение:
        s.listen(MAX_CONNECTIONS)
        # print('pid:', os.getpid())
        # print('Сервер запущен на:', *address_port)
        print('Сервер запущен на:', address_port[0], address_port[1])
        # SERVER_LOGGER.debug(f'pid: {os.getpid()}. Сервер запущен на: {address_port[0]} {address_port[1]}')
        SERVER_LOGGER.debug(f'pid: {os.getpid()}. Сервер запущен на: {address_port}')
        accept_connections(s)
    except Exception as err:
        # print('create_socket', err)
        SERVER_LOGGER.exception(f'create_socket error: {err}')
    finally:
        s.close()


@log
def main():
    address_port = get_settings()
    create_socket(address_port)

if __name__ == '__main__':
    main()

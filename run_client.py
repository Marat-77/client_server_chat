import argparse
from socket import socket, AF_INET, SOCK_STREAM
import sys
import time
from typing import Tuple

from client.settings import DEFAULT_PORT, MAX_PACKAGE_LENGTH, TIMEOUT, CLIENT_LOGGER
from client.utils import presence_msg, send_msg, auth_user_msg, read_msg, quit_user_msg

def get_settings() -> Tuple[str, int]:
    # вернуть кортеж address_port (addr, port)
    arg_lst = sys.argv
    usage_msg = 'usage: run_client.py <address> [<port>]\n'
    usage_msg += 'for help: run_client.py -h'
    help_msg = usage_msg + '\n'
    help_msg += 'arguments:\n'
    help_msg += '  <address>\thostname or ip address\n'
    help_msg += 'options:\n'
    help_msg += f'  <port>\tport 1024...65535 (default: {DEFAULT_PORT})\n'
    if len(arg_lst) == 1:
        print(usage_msg)
        CLIENT_LOGGER.debug(f'{arg_lst}')
        exit(1)
    elif len(arg_lst) == 2 and (arg_lst[1] == '-h' or arg_lst[1] == '--help'):
        print(help_msg)
        CLIENT_LOGGER.debug(f'{arg_lst}')
        exit(1)
    elif len(arg_lst) == 2:
        addr = arg_lst[1]
        port = DEFAULT_PORT
        CLIENT_LOGGER.debug(f'args: {arg_lst} return: {addr}, {port}')
        return addr, port
    elif len(arg_lst) == 3:
        addr = arg_lst[1]
        try:
            port = int(arg_lst[2])
            if not (1024 <= port <= 65535):
                print(usage_msg)
                CLIENT_LOGGER.debug(f'{arg_lst}')
                print('введите значение port в диапазоне 1024...65535')
                exit(1)
            return addr, port
        except ValueError as err:
            # err - для лога
            print(usage_msg)
            CLIENT_LOGGER.debug(f'{arg_lst}')
            print('введите значение port в диапазоне 1024...65535')
            exit(1)
    else:
        print(usage_msg,
              '\nerror: unrecognized arguments:',
              ' '.join(arg_lst[1:]))
        CLIENT_LOGGER.debug(f'{arg_lst}')
        exit(1)


# вариант с argparse
def get_argparse_settings() -> Tuple[str, int]:
    parser = argparse.ArgumentParser(# prog='run_client',
                                     # prefix_chars='',
                                     description='Run client',
                                     usage='%(prog)s [-h] <address> [-port <port>]',
                                     epilog='epilog my progs')
    parser.add_argument('addr',
                        # dest='addr',
                        type=str,
                        # default=DEFAULT_ADDRESS,
                        metavar='<address>',
                        help='hostname or ip address')
    parser.add_argument('-port', type=int,
                        # required=False,
                        # required=True,
                        # dest='port',
                        default=DEFAULT_PORT,
                        metavar='<port>',
                        help='port 1024...65535 (default: %(default)s)')
    args = parser.parse_args()
    if args.port < 1024 or args.port > 65535:
        print('введите значение port в диапазоне 1024...65535')
        exit(1)
    return args.addr, args.port


def create_connection(address_port: Tuple[str, int]):
    # Создать сокет TCP
    s = socket(AF_INET, SOCK_STREAM)
    s.settimeout(TIMEOUT)
    try:
        s.connect(address_port)
        CLIENT_LOGGER.debug(f'Соединение с {address_port} установлено')

        # Пишем сообщение серверу:

        # пробуем авторизоваться:

        # # 1 неверный пользователь
        # wrong_user = 'wrong'
        # wrong_password = '12345678'
        # auth_msg = auth_user_msg(wrong_user, wrong_password)
        # send_msg(s, auth_msg)
        # # Получаем сообщение от сервера:
        # income_data = s.recv(MAX_PACKAGE_LENGTH)
        # data = read_msg(income_data)
        #
        # # 2 неверный пароль
        # user = 'user1'
        # wrong_password = '12345678'
        # auth_msg = auth_user_msg(user, wrong_password)
        # send_msg(s, auth_msg)
        # # Получаем сообщение от сервера:
        # income_data = s.recv(MAX_PACKAGE_LENGTH)
        # data = read_msg(income_data)

        # 3 верный пользователь и пароль
        user = 'user1'
        password = 'mypasword123'
        auth_msg = auth_user_msg(user, password)
        send_msg(s, auth_msg)

        # Получаем сообщение от сервера:
        income_data = s.recv(MAX_PACKAGE_LENGTH)
        # print(income_data)
        # print(len(income_data))
        if income_data:
            # print('is income_data')
            # print(f'1/income_data: {income_data}')
            CLIENT_LOGGER.debug(f'income_data: {income_data}')
            data = read_msg(income_data)
            print('data:\n', data)
        else:
            print('NOT income_data')

        # отправляем presence:
        msg = presence_msg(user)
        send_msg(s, msg)
        time.sleep(1)

        # отправляем quit
        msg = quit_user_msg(user)
        send_msg(s, msg)

    except ConnectionRefusedError as err:
        # print(err)
        CLIENT_LOGGER.exception(f'exception: {err}')
        # [Errno 111] Connection refused
    except TimeoutError as err:
        # print(err)
        CLIENT_LOGGER.exception(f'exception: {err}')
        # timed out
    finally:
        s.close()


def main():
    address_port = get_settings()
    print(address_port)
    create_connection(address_port)


if __name__ == '__main__':
    main()


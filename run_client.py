import argparse
import concurrent.futures
import random
from socket import socket, AF_INET, SOCK_STREAM
import sys
from threading import Event
import time
from typing import Tuple

from client.settings import DEFAULT_PORT, MAX_PACKAGE_LENGTH, TIMEOUT, CLIENT_LOGGER
from client.utils import (presence_msg, send_msg, auth_user_msg,
                          read_msg, quit_user_msg, message_msg)

def get_settings() -> Tuple[str, int]:
    # deprecated

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
def get_argparse_settings() -> Tuple[Tuple[str, int], str]:
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
    # deprecated
    # parser.add_argument('-mode', type=str,
    #                     # required=False,
    #                     # required=True,
    #                     dest='mode',
    #                     default='reader',
    #                     choices=['reader', 'writer'],
    #                     metavar='<mode>',
    #                     help='mode reader | writer (default: %(default)s)')
    args = parser.parse_args()
    if args.port < 1024 or args.port > 65535:
        print('введите значение port в диапазоне 1024...65535')
        exit(1)
    return args.addr, args.port


def create_connection(address_port: Tuple[str, int]) -> socket:
    # Создать сокет TCP
    s = socket(AF_INET, SOCK_STREAM)
    s.settimeout(TIMEOUT)
    try:
        s.connect(address_port)
        CLIENT_LOGGER.debug(f'Соединение с {address_port} установлено')
        return s
    except ConnectionRefusedError as err:
        # print(err)
        CLIENT_LOGGER.exception(f'exception: {err}')
        # [Errno 111] Connection refused
    except TimeoutError as err:
        # print(err)
        CLIENT_LOGGER.exception(f'exception: {err}')
        # timed out
    # finally:
    #     s.close()

def client_reader(s: socket, event: Event):
    while True:
        if event.is_set():
            break
        # Получаем сообщение от сервера:
        income_data = s.recv(MAX_PACKAGE_LENGTH)
        if income_data:
            CLIENT_LOGGER.debug(f'income_data: {income_data}')
            data = read_msg(income_data)
            print('data:\n', data)


def client_writer(s: socket, message):
    # отправляем message:
    msg = message_msg('user', message)
    send_msg(s, msg)

def user_msg():
    message = input('Input message: ')
    return message


def user_input(s: socket):
    while True:
        user_choice = input('Input "1" to write message, "q" to exit: ')
        if user_choice == '1':
            msg = user_msg()
            print(msg)
            client_writer(s, msg)
        elif user_choice == 'q':
            print('Exit')
            break
        else:
            print('Repeat input')
    return True

def main():
    address_port = ('127.0.0.1', 7777)
    print(address_port)
    sock = create_connection(address_port)
    print(sock)
    if not sock:
        print('exit')
        exit()
    event = Event()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        f1 = executor.submit(client_reader, sock, event)
        f2 = executor.submit(user_input, sock)
        if f2.result() is True:
            event.set()
            print('---exit---')


if __name__ == '__main__':
    main()


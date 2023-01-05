from select import select
import socket
from socket import SocketType
from typing import List


def create_socket() -> SocketType:
    serv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serv_socket.bind(('', 7777))
    serv_socket.listen()
    print('socket file no:', serv_socket.fileno())
    print(type(serv_socket))
    return serv_socket


def accept_connection(sockets_list: List[SocketType]):
    print('before accept')
    client_socket, addr = server_socket.accept()
    print('connection from', addr)
    print(type(client_socket))

    sockets_list.append(client_socket)


def send_message(client_socket: SocketType, sockets_list: List[SocketType]):
    request = client_socket.recv(1024)
    if request:
        print(request.decode('utf-8'))
        response = 'Hello!!!\n'.encode()
        print('online_clients:', sockets_list)
        for client in sockets_list:
            if client is not server_socket:
                client.send(response)
                client.send(request)
    else:
        client_socket.close()


def main_loop():
    sockets_list: List[SocketType] = [server_socket]

    while True:
        reads:List[SocketType] = []
        time_wait = 2
        try:
            print('sockets_list:', sockets_list)
            reads, _, _ = select(sockets_list, [], [], time_wait)
            print('\nreads:', reads)
        except Exception as err:
            print(err)
            print(sockets_list)
            sockets_list = list(filter(lambda x: x.fileno() > 0, sockets_list))
            print(sockets_list)

        for soc in reads:
            if soc is server_socket:
                accept_connection(sockets_list)
            else:
                try:
                    send_message(soc, sockets_list)
                except Exception as err:
                    print(err)


if __name__ == '__main__':
    server_socket = create_socket()
    main_loop()



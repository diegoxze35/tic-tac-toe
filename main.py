import sys
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
from network.new_connection import on_new_client

import logging

logging.basicConfig(level=logging.INFO, format='(%(threadName)-10s) %(message)s')
if __name__ == '__main__':
    ip: str
    port: int
    if len(sys.argv) == 3:
        ip = sys.argv[1]
        port = int(sys.argv[2])
    else:
        exit('Usage: python main.py <ip> <port>')
    with socket(AF_INET, SOCK_STREAM) as s:
        s.setblocking(True)
        s.bind((ip, port))
        s.listen()
        while True:
            conn, addr = s.accept()
            logging.info(f'{addr} connected')
            t = Thread(target=on_new_client, args=(conn,))
            t.start()
            logging.info(f'{t.name} created to handle new connection {addr}')

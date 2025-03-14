from datetime import date
import sys
from socket import socket, AF_INET, SOCK_STREAM
import pickle

from network.GameRoom import GameRoom
from network.create_game_room import create_game_room

if __name__ == '__main__':

    date_1 = date(day=12, month=9, year=2002)
    date_2 = date(day=29, month=8, year=2004)
    march_10_2025 = date(day=10, month=3, year=2025)
    lived_days_1 = (march_10_2025 - date_1).days
    lived_days_2 = (march_10_2025 - date_2).days
    print(lived_days_1 % 3, lived_days_2 % 3)

    ip: str
    port: int
    if len(sys.argv) == 3:
        ip = sys.argv[1]
        port = int(sys.argv[2])
    else:
        exit('Usage: python main.py <ip> <port>')
    with socket(AF_INET, SOCK_STREAM) as s:
        s.bind((ip, port))
        s.listen()
        print('Waiting for connection...')
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            msg, params = pickle.loads(conn.recv(2048))
            room: GameRoom
            match msg:
                case 'START':
                    difficulty = params['difficulty']
                    square = params['square']
                    room = create_game_room(difficulty=difficulty, square=square, user_socket=conn)
                    room.run()
                case 'JOIN':
                    raise NotImplementedError

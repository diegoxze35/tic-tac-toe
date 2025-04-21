from socket import socket
from typing import Literal

from game.HumanPlayer import HumanPlayer
from network.GameRoom import GameRoom
from network.create_game_room import create_game_room
from random import randint
from threading import current_thread

import logging

logging.basicConfig(level=logging.INFO, format='(%(threadName)-10s) %(message)s')
"""
    KEY = room code -> int
    VALUE = (GameRoom, Thread, [socket, socket]) -> tuple
"""
rooms = {}


def on_end_game(code: int):
    global rooms
    t = rooms[code][1]
    logging.info(f'thread {t.name} ended')
    logging.info(f'room with code {code} ended')
    del rooms[code]


def start_game(difficulty: int, square: Literal['X', 'O'], user_socket: socket, single_player: bool):
    global rooms
    code = randint(1000, 9999)
    room = create_game_room(
        difficulty=difficulty,
        square=square,
        user_socket=user_socket,
        single_player=single_player,
        on_end_game=lambda: on_end_game(code)
    )
    logging.info(f'{user_socket} has created a {'single player' if single_player else 'multiplayer'} room with code {code}')
    if not single_player:
        user_socket.send(f'SHAC,{code},00'.encode())
    rooms[code] = (room, current_thread(), [user_socket])
    room.run()


def on_new_client(conn: socket):
    global rooms
    command = conn.recv(10).decode()
    msg = command.split(',')
    room: GameRoom
    match msg[0]:
        case 'GAME':
            """
            Recivimos la instrucción del cliente de jugar contra la máquina con la dificultad
            y casilla 'X' o 'O' escojidas
            """
            difficulty, square, single_player = msg[1:]
            start_game(difficulty, square, conn, bool(int(single_player)))
        case 'JOIN':  # Mensaje reservado para que otro jugador humano entre a una partida con otro jugador humano
            code = int(msg[1])
            if not rooms.get(code):
                logging.critical(f'{conn} has a invalid code')
                bad_code = -1
                conn.send(bad_code.to_bytes(length=1, byteorder='big', signed=True))
            else:
                room = rooms[code][0]
                player = HumanPlayer(square=room.get_available_square(), user_socket=conn,
                                     is_valid_move=room.is_valid_move())
                room.set_missing_player(player)
                n = room.get_board_lenght()
                rooms[code][2].append(conn)
                logging.info(f'{conn} has joined a room with code {code}')
                conn.send(n.to_bytes(length=1, byteorder='big', signed=True))
                room.condition.acquire()
                room.condition.notify()
                room.condition.release()

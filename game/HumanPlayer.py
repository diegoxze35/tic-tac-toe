from socket import socket
from typing import Callable, override
from game.Player import Player

import logging

logging.basicConfig(level=logging.INFO, format='(%(threadName)-10s) %(message)s')

class HumanPlayer(Player):
    """
    Implementación de la clase jugador, un jugador humano
    realiza sus movimiento en el tabloro a travez de un socket
    """

    def __init__(self, square: str, user_socket: socket, is_valid_move: Callable[[tuple[int, int]], tuple[str, bool]]):
        """

        :param square: Simbolo de la casilla del jugador
        :param user_socket: Socket de este jugador
        :param is_valid_move: Función que verifica si el movimiento del jugador es valido
        """
        super().__init__(square)
        self.user_socket = user_socket
        self.__is_valid_move = is_valid_move
        self.__move_message = str()
        self.__current_move_is_valid = False

    @override
    def _notify_move(self, move: tuple[int, int]) -> None:
        if self.__current_move_is_valid:
            command = f'MOVE,{move[0]},{move[1]}, {self.square} '
        else:
            command = f'INMV,{self.__move_message}'
        self.user_socket.send(command.encode())

    @override
    def make_move(self) -> tuple[int, int, bool]:
        self.user_socket.send(f'TURN,0,0, {self.square} '.encode())
        #move = self.__user_socket.recv(1024).decode().split(',')
        x_bytes = self.user_socket.recv(32) #Bytes de la coordenada X
        y_bytes = self.user_socket.recv(32) #Bytes de la coordenada Y
        x = int.from_bytes(x_bytes, byteorder='big', signed=True)
        y = int.from_bytes(y_bytes, byteorder='big', signed=True)
        real_move = (x - 1, y - 1)
        #real_move = (int(move[0]) - 1, int(move[1]) - 1)
        self.__move_message, self.__current_move_is_valid = self.__is_valid_move(real_move)
        self._notify_move(real_move)
        return real_move + (self.__current_move_is_valid, )

    @override
    def end_game(self, winner: str, time_taken: float) -> None:
        command = f'ENDG,{winner},{round(time_taken, 7)}'
        self.user_socket.send(command.encode())
        self.user_socket.close()
        logging.info(f'Game ended: {winner}')
        logging.info(f'{self.user_socket} has left the server')

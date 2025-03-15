from socket import socket
from typing import Callable

from game.Player import Player


class HumanPlayer(Player):

    def __init__(self, square: str, user_socket: socket, is_valid_move: Callable[[tuple[int, int]], bool]):
        super().__init__(square)
        self.__user_socket = user_socket
        self.__is_valid_move = is_valid_move
        self.__current_move_is_valid = False

    def _notify_move(self, move: tuple[int, int]) -> None:
        if self.__current_move_is_valid:
            command = f'MOVE,{move[0]},{move[1]}, {self.square} '
        else:
            command = f'INMV,{move[0]},{move[1]}, {self.square} '
        self.__user_socket.send(command.encode())

    def make_move(self) -> tuple[int, int, bool]:
        self.__user_socket.send(f'TURN,0,0, {self.square} '.encode())
        move = self.__user_socket.recv(6).decode().split(',')
        real_move = (int(move[0]) - 1, int(move[1]) - 1)
        self.__current_move_is_valid = self.__is_valid_move(real_move)
        self._notify_move(real_move)
        return real_move + (self.__current_move_is_valid, )

    def end_game(self, winner: str, time_taken: float) -> None:
        command = f'ENDG,{winner},{round(time_taken, 7)}'
        self.__user_socket.send(command.encode())

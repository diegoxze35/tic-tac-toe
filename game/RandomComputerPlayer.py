from typing import override

from game.TicTacToeBoard import TicTacToeBoard
from game.Player import Player
import random
from socket import socket

class RandomComputerPlayer(Player):


    def __init__(self, board, square: str, player_socket: socket):
        super().__init__(square)
        self.__board: TicTacToeBoard = board
        self.__player_socket = player_socket

    @override
    def make_move(self) -> tuple[int, int, bool]:
        moves = self.__board.get_available_moves()
        selected_move = random.choice(moves)
        self._notify_move(selected_move)
        return selected_move + (True, )

    @override
    def _notify_move(self, move: tuple[int, int]) -> None:
        command = f'MOVE,{move[0]},{move[1]}, {self.square} '
        self.__player_socket.send(command.encode())
        print(f'Computer\'s move = {move}')

    @override
    def end_game(self, winner: str, time_taken: float) -> None:
        print(f'Winner {winner}')
        print(f'Time taken: {time_taken} seconds')

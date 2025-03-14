from game.TicTacToeBoard import TicTacToeBoard
from game.Player import Player
import random
import pickle
from socket import socket

class RandomComputerPlayer(Player):


    def __init__(self, board, square: str, player_socket: socket):
        super().__init__(square)
        self.__board: TicTacToeBoard = board
        self.__player_socket = player_socket

    def make_move(self) -> tuple[int, int]:
        moves = self.__board.get_available_moves()
        selected_move = random.choice(moves)
        self._notify_move(selected_move)
        return selected_move

    def _notify_move(self, move: tuple[int, int]) -> None:
        command = ('OPONNET_MOVE', {'coordinates': move, 'square': f' {self.square} '})
        self.__player_socket.send(pickle.dumps(command))
        print(f'Computer\'s move = {move}')

    def end_game(self, winner: str, time_taken: float) -> None:
        print(f'Winner {winner}')
        print(f'Time taken: {time_taken} seconds')

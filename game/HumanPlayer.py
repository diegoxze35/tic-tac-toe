from socket import socket

from game.Player import Player
import pickle

class HumanPlayer(Player):

    def __init__(self, square: str, user_socket: socket):
        super().__init__(square)
        self.__user_socket = user_socket

    def _notify_move(self, move: tuple[int, int]) -> None:
        command = ('MOVE', {'coordinates': move, 'square': f' {self.square} '})
        self.__user_socket.send(pickle.dumps(command))

    def make_move(self) -> tuple[int, int]:
        move = pickle.loads(self.__user_socket.recv(56))
        real_move = (move[0] - 1, move[1] - 1)
        self._notify_move(real_move)
        return real_move

    def end_game(self, winner: str, time_taken: float) -> None:
        command = ('END', {'winner': winner, 'time_taken': time_taken})
        self.__user_socket.send(pickle.dumps(command))

from socket import socket
from threading import Condition
from typing import Callable

from game.TicTacToeBoard import TicTacToeBoard
from game.HumanPlayer import HumanPlayer
from game.Player import Player
from game.RandomComputerPlayer import RandomComputerPlayer
from network.GameRoom import GameRoom


def create_game_room(difficulty, square, user_socket: socket, single_player=True, on_end_game: Callable = lambda : None):
    board = TicTacToeBoard(n=3 if int(difficulty) == 1 else 5)
    player_1: Player = HumanPlayer(square, user_socket, is_valid_move=board.is_valid_move)
    player_2: Player
    if square == 'X':
        player_2 = RandomComputerPlayer(board, square='O', player_socket=user_socket) if single_player else None
        return GameRoom(x=player_1, o=player_2, board=board, condition=Condition(), on_end_game=on_end_game)
    else:
        player_2 = RandomComputerPlayer(board, square='X', player_socket=user_socket) if single_player else None
        return GameRoom(x=player_2, o=player_1, board=board, condition=Condition(), on_end_game=on_end_game)

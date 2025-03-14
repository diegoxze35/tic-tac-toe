from time import time
from game.TicTacToeBoard import TicTacToeBoard
from game.Player import Player


class GameRoom:

    def __init__(self, x: Player, o: Player, board: TicTacToeBoard):
        self.__players = [x, o]
        self.__current_player = self.__players[0]
        self.__board = board

    def __change_turn(self):
        self.__current_player = self.__players[0] if self.__current_player == self.__players[1] else self.__players[1]

    def run(self):
        start = time()
        winner = None
        while not winner:
            valid_move = None
            while not valid_move:
                move = self.__current_player.make_move()
                valid_move = self.__board.make_move(move, self.__current_player.square)
            self.__change_turn()
            winner = self.__board.check_win()
        end = time()
        for p in self.__players:
            p.end_game(winner=winner, time_taken=end - start)

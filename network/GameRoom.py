from game.Board import Board
from network.Player import Player
from socket import socket, AF_INET, SOCK_STREAM

class GameRoom:

    def __init__(self, x: Player, o: Player, board: Board):
        self.__players = [x, o]
        self.__current_player = x
        self.__board = board
        self.__socket = socket(AF_INET, SOCK_STREAM)

    def __change_turn(self):
        self.__current_player = self.__players[0] if self.__current_player == self.__players[1] else self.__players[1]

    def __turn(self, coordinates):
        #self.__change_turn()
        self.__current_player.move(coordinates)

    def run(self):
        while self.__board.there_are_moves():
            pass

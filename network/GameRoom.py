from threading import Condition
from time import time
from typing import Callable

from game.HumanPlayer import HumanPlayer
from game.TicTacToeBoard import TicTacToeBoard
from game.Player import Player


class GameRoom:
    """
    Clase que representa una partida actual entre 2 jugadores
    """
    def __init__(self, x: Player, o: Player, board: TicTacToeBoard, condition: Condition, on_end_game: Callable):
        """
        Constructor de la sala de juego
        :param x: Jugador 'X' de la partida
        :param o: Jugador 'O' de la partida
        :param board: Tablero de ls jugadores
        """
        self.condition = condition
        self.__players = [x, o]
        self.__current_player = self.__players[0] #El primer jugador en tirar siempre es 'X'
        self.__another_player = self.__players[1]
        self.__board = board
        self.__on_end_game = on_end_game

    def __change_turn(self):
        self.__another_player = self.__current_player
        self.__current_player = self.__players[0] if self.__current_player == self.__players[1] else self.__players[1]

    def run(self):
        self.condition.acquire()
        self.condition.wait_for(lambda : all(map(lambda player: player is not None, self.__players)))
        self.condition.release()
        for p in filter(lambda player: isinstance(player, HumanPlayer), self.__players):
            p.user_socket.send(f'REDY,0000000'.encode())
        start = time() #Obtenemos el tiempo al empezar la partida
        winner = None
        while not winner: #Mientras no halla un ganador, el juego continua
            if isinstance(self.__current_player, HumanPlayer) and isinstance(self.__another_player, HumanPlayer):
                self.__another_player.user_socket.send(f'WAIT,{self.__current_player.square},00000'.encode())
            valid_move = False
            x: int = -1
            y: int = -1
            while not valid_move: #Mientras el movimiento del jugador actual no sea valido, se solicitará su movimiento
                x, y, valid_move = self.__current_player.make_move()
            if isinstance(self.__current_player, HumanPlayer) and isinstance(self.__another_player, HumanPlayer):
                self.__another_player.user_socket.send(f'MOVE,{x},{y}, {self.__current_player.square} '.encode())
            self.__board.make_move((x, y), self.__current_player.square)
            self.__change_turn()
            winner = self.__board.check_win()
        end = time()
        for p in self.__players:
            p.end_game(winner=winner, time_taken=end - start)
        self.__on_end_game()

    def get_available_square(self):
        return 'O' if self.__players[0] else 'X'

    def set_missing_player(self, player: Player):
        if not self.__current_player:
            self.__current_player = player
        if not self.__another_player:
            self.__another_player = player
        self.__players[self.__players.index(None)] = player

    def is_valid_move(self):
        return self.__board.is_valid_move

    def get_board_lenght(self):
        return len(self.__board)
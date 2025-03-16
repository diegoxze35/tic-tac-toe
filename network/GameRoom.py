from time import time
from game.TicTacToeBoard import TicTacToeBoard
from game.Player import Player


class GameRoom:
    """
    Clase que representa una partida actual entre 2 jugadores
    """
    def __init__(self, x: Player, o: Player, board: TicTacToeBoard):
        """
        Constructor de la sala de juego
        :param x: Jugador 'X' de la partida
        :param o: Jugador 'O' de la partida
        :param board: Tablero de ls jugadores
        """
        self.__players = [x, o]
        self.__current_player = self.__players[0] #El primer jugador en tirar siempre es 'X'
        self.__board = board

    def __change_turn(self):
        self.__current_player = self.__players[0] if self.__current_player == self.__players[1] else self.__players[1]

    def run(self):
        start = time() #Obtenemos el tiempo al empezar la partida
        winner = None
        while not winner: #Mientras no halla un ganador, el juego continua
            valid_move = False
            x: int = -1
            y: int = -1
            while not valid_move: #Mientras el movimiento del jugador actual no sea valido, se solicitará su movimiento
                x, y, valid_move = self.__current_player.make_move()
            self.__board.make_move((x, y), self.__current_player.square)
            self.__change_turn()
            winner = self.__board.check_win()
        end = time()
        for p in self.__players:
            p.end_game(winner=winner, time_taken=end - start)

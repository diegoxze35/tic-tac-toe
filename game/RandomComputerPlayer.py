from typing import override

from game.TicTacToeBoard import TicTacToeBoard
from game.Player import Player
import random
from socket import socket

class RandomComputerPlayer(Player):
    """
    Implementación de un jugador que realiza movimientos aleatorios
    """

    def __init__(self, board, square: str, player_socket: socket):
        """
        Constructor
        :param board: Referencia al tablero de la partida donde esta unido este jugador
        :param square: Casilla que se asignó al jugador
        :param player_socket: Socket del jugadr humano que juega contra este jugador
        """
        super().__init__(square)
        self.__board: TicTacToeBoard = board
        self.__player_socket = player_socket

    @override
    def make_move(self) -> tuple[int, int, bool]:
        """
        Este jugador siempre realiza jugadas validas
        :return: Una tupla con las coordenadas de tiro, el tercer elemento de la tupla siempre es True
        """
        moves = self.__board.get_available_moves()
        selected_move = random.choice(moves)
        self._notify_move(selected_move)
        return selected_move + (True, )

    @override
    def _notify_move(self, move: tuple[int, int]) -> None:
        command = f'MOVE,{move[0]},{move[1]}, {self.square} '
        self.__player_socket.send(command.encode()) #Enviar movimiento al jugador humano
        print(f'Computer\'s move = {move}')

    @override
    def end_game(self, winner: str, time_taken: float) -> None:
        print(f'Winner {winner}')
        print(f'Time taken: {time_taken} seconds')

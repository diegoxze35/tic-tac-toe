from abc import ABC, abstractmethod

class Player(ABC):
    """
    Clase que representa un jugador
    Puede ser un jugador humano, o la computadora
    """

    def __init__(self, square: str):
        """
        Constructor de la clase
        :param square: Simbolo de la casilla que tiene este jugador
        """
        self.square = square

    @abstractmethod
    def make_move(self) -> tuple[int, int, bool]:
        """
        Obtiene el movimiento de este jugador
        :return: Unta tupla con dos enteros
        que son las coordenadas del movimiento
        y un booleano que indica si el movimiento es valido
        o no
        """
        pass

    @abstractmethod
    def _notify_move(self, move: tuple[int, int]) -> None:
        """
        Metodo protegido que sirve para notificar
        que el jugador realizó un movimiento en
        el tablero

        :param move: Tupla con dos enteros que representa
        el movimiento
        :return: None
        """
        pass

    @abstractmethod
    def end_game(self, winner: str, time_taken: float) -> None:
        """
        Metodo para notificar al jugador que terminó el juego
        :param winner: Simbolo del jugador que ganó
        :param time_taken: Tiempo total de la partida
        :return: None
        """
        pass
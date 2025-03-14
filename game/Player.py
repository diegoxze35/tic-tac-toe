from abc import ABC, abstractmethod

class Player(ABC):

    def __init__(self, square: str):
        self.square = square

    @abstractmethod
    def make_move(self) -> tuple[int, int]:
        pass

    @abstractmethod
    def _notify_move(self, move: tuple[int, int]) -> None:
        pass

    @abstractmethod
    def end_game(self, winner: str, time_taken: float) -> None:
        pass
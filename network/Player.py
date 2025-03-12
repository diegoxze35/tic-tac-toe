from abc import ABC, abstractmethod


class Player(ABC):

    @abstractmethod
    def move(self, move: (int, int)) -> str:
        pass

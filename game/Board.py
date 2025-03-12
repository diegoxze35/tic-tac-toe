from game.Square import Square

class Board:

    def __init__(self, n: int = 3):
        self.__squares: list[list[Square]] = [[Square.EMPTY for _ in range(n)] for _ in range(n)]

    def get_available_squares(self) -> list[Square]:
        from itertools import chain
        all_squares = chain(*self.__squares)
        return list(filter(lambda square: square == Square.EMPTY, all_squares))

    def there_are_moves(self) -> bool:
        return len(self.get_available_squares()) != 0
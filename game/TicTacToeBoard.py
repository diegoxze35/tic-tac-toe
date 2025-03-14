import itertools

from game.Square import Square


class TicTacToeBoard:

    def __init__(self, n: int = 3):
        self.__squares: list[list[Square]] = [[Square.EMPTY for _ in range(n)] for _ in range(n)]

    def __is_valid_move(self, move: tuple[int, int]) -> bool:
        x, y = move
        n = len(self.__squares)
        if (0 <= x < n) and (0 <= y < n):
            if self.__squares[x][y] == Square.EMPTY:
                return True
        return False

    def make_move(self, move: tuple[int, int], square: str) -> tuple[int, int] | None:
        if not self.__is_valid_move(move):
            return None
        self.__squares[move[0]][move[1]] = Square(square)
        return move

    def get_available_moves(self) -> list[tuple[int, int]]:
        moves: list[tuple[int]] = []
        n = len(self.__squares)
        for i in range(n):
            for j in range(n):
                if self.__squares[i][j] == Square.EMPTY:
                    moves.append((i, j))
        return moves

    def check_win(self) -> str | None:
        """
        Verificar el ganador del juego
        :return: 'X' si el jugador X ganó, 'O' si el jugador O ganó, 'Tie' si es un empate o None si aún no hay ganador
        """
        # Verificando las filas
        for row in self.__squares:
            if all(map(lambda square: square == Square.X, row)):
                return 'X'
            if all(map(lambda square: square == Square.O, row)):
                return 'O'
        # Verificando las filas

        n = len(self.__squares)

        # Verificando las columnas
        for i in range(n):
            #for column in [self.__squares[i][j] for j in range(n)]:
            if all(map(lambda square: square == Square.X, [self.__squares[i][j] for j in range(n)])):
                return 'X'
            if all(map(lambda square: square == Square.O, [self.__squares[i][j] for j in range(n)])):
                return 'O'
        # Verificando las columnas

        # Verificando diagonales

        if all(map(lambda square: square == Square.X, [self.__squares[i][i] for i in range(n)])):
            return 'X'
        if all(map(lambda square: square == Square.O, [self.__squares[i][i] for i in range(n)])):
            return 'O'
        if all(map(lambda square: square == Square.X, [self.__squares[i][(n - 1) - i] for i in range(n)])):
            return 'X'
        if all(map(lambda square: square == Square.O, [self.__squares[i][(n - 1) - i] for i in range(n)])):
            return 'O'
        # Verificando diagonales

        # Verificando si aún no hay ganador
        all_squares = itertools.chain(*self.__squares)
        if any(filter(lambda square: square == Square.EMPTY, all_squares)):
            return None
        # Verificando si aún no hay ganador

        return 'Tie'

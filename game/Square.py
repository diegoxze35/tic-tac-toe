from enum import Enum
"""
Enumeración para representar los simbolos
que puede tener una casilla del tablero,
"""
class Square(Enum):
    EMPTY = ' '
    X = 'X'
    O = 'O'
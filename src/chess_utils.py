from collections import deque
from typing import Deque

E = "E"
W = "W"
B = "B"


def translate_fe(fe_notation: str):
    """
    Translates Forysyth-Edwards notation to simple 8x8 chess board disregarding the chess piece type.
      Only the color and the position of the chess piece is kept resulting in 3 labels:

        - E for an empty field
        - W for a white piece
        - B for a black piece

    As an example let's take 4x4 chess board with a black King in top right corner and a white Rook
      in the opposite corner:

    Visualized FE notation 3k-4-4-R3':

        [E, E, E, k]
        [E, E, E, E]
        [E, E, E, E]
        [R, E, E, E]

    Translated chess board:

        [E, E, E, B]
        [E, E, E, E]
        [E, E, E, E]
        [W, E, E, E]

    More on the notation: https://en.wikipedia.org/wiki/Forsyth%E2%80%93Edwards_Notation
    """

    simple_chess_board = []
    rows = fe_notation.split("-")
    for fe_row in rows:
        simple_chess_board.append(_translate_fe_row(fe_row))

    return simple_chess_board


def _translate_fe_row(FE_row: str):
    converted_row: Deque[str]= deque()

    for id in range(0, len(FE_row)):
        el = FE_row[id]
        if el.isdigit():
            for _ in range(0, int(el)):
                converted_row.append(E)

        elif el.isupper():
            converted_row.append(W)

        elif el.islower():
            converted_row.append(B)

    return converted_row

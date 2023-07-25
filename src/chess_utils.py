import os
from typing import List
import csv
from PIL import Image

# Chess board states
E = "E"
W = "W"
B = "B"


class Board:
    def __init__(self, board: List[int]):
        self.board = board

    def to_str(self):
        string_representation = ''
        for row in self.board:
            string_representation = f'{string_representation}-{row}'
        return string_representation


def translate_fe_notation(fe_notation: str) -> str:
    """
    Translates Forysyth-Edwards notation where chess type is disregarded - WBE notation.

     Any white piece will be replaced with "W" and any black piece will be replaced with "B", an empty field will be
     replaced with "E".
    """
    WBE_notation = ''
    for row in fe_notation.split('-'):
        for el in row:
            if el.isdigit():
                WBE_notation = f'{WBE_notation}{"E" * int(el)}'
            if el.isupper():
                WBE_notation = f'{WBE_notation}W'
            elif el.islower():
                WBE_notation = f'{WBE_notation}B'

        WBE_notation = f'{WBE_notation}-'

    return WBE_notation[:-1]  # get rid of the last "-"


def translate_fe_to_int_notation(WBE_notation: str) -> List[int]:
    """Replace W with 1 B with -1 and E with 0"""
    int_notation = []
    for row in WBE_notation.split('-'):
        for el in row:
            if el == 'W':
                int_notation.append(1)
            elif el == 'B':
                int_notation.append(-1)
            else:
                int_notation.append(0)

    return int_notation


def one_hot_wbe(int_notation):
    """For neural network input of 8x8 board we have 64 inputs, each of them is a single chessboard tile with either of the values - 'W"(1), 'E'(0), 'B'(-1)
    This function converts the 64 input numbers 192 neuron representation where:
     - first 64 neurons represent one hot encoded white pieces
     - next 64 neurons represent one hot encoded 'empty' places
     - last 64 neurons represent one hot encoded black pieces
    """
    white = []
    empty = []
    black = []
    for id in range(len(int_notation)):
        if int_notation[id] == 1:
            white.append(1)
            empty.append(0)
            black.append(0)
        elif int_notation[id] == -1:
            white.append(0)
            empty.append(0)
            black.append(1)
        else:
            white.append(0)
            empty.append(1)
            black.append(0)

    for w, e, b in zip(white, empty, black):
        assert w + e + b == 1, f"WBE encoidng failed, w: {w}, e: {e}, b: {b}"
    return white, empty, black

# img_names_to_csv(img_names)

# for filename in os.listdir(small_data_dir):
#     fe_label = os.path.splitext(filename)[0]
#     print(fe_label)
#     label = board_to_str(translate_fe(fe_label))
#     label_dir = f'small_data/labels/{label}'
#     # print(f'label {label_dir}')


#     try:
#         os.makedirs(label_dir)
#     except FileExistsError:
#         continue

# parent_dir = '/Users/my_Username/Desktop/'
# old_name = 'foo.txt'
# new_name = 'bar.txt'

# with os.open(parent_dir, os.O_RDONLY) as fd:
#     os.replace(old_name, new_name, src_dir_fd=fd)


    # finally:
    #     old_path = f"{small_data_dir}{filename}"
    #     old_path = os.path.abspath(old_path)
    #     # print(old_path)
    #     # Image.open(old_path).show()
        
    #     new_path = f"{label_dir}/{filename}"
    #     new_path = os.path.abspath(new_path)
    #     # print (new_path)
    #     os.replace(os.path.abspath(old_path), os.path.abspath(new_path))

    #     continue


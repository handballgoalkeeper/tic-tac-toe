import re


def validate_board_layout(board):
    layout_str = "".join(["".join(row) for row in board.layout])

    if re.match(r"^[-XO]{9}$", layout_str) is None:
        raise ValueError("Board can only contain X, O or -(empty cell).")


def valid_move(board, row, col) -> bool:
    if (row > 0 and row <= 3) and (col > 0 and col <= 3) and board.layout[row - 1][col - 1] == "-":
        return True
    return False

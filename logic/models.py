import enum
from dataclasses import dataclass
from .validators import validate_board_layout, valid_move
from random import randint


class Mark(str, enum.Enum):
    X = "X"
    O = "O"

    @property
    def other(self) -> "Mark":
        return Mark.O if self is Mark.X else Mark.X


@dataclass
class Board:
    layout: list[list[str]]

    def __post_init__(self):
        validate_board_layout(self)

    def check_win(self, mark: Mark):
        # Check row wins

        for row in self.layout:
            if row[0] == row[1] == row[2] == mark:
                return True

        # Check column wins by transposing the board matrix and checking the rows
        for row in [list(i) for i in zip(*self.layout)]:
            if row[0] == row[1] == row[2] == mark:
                return True

        # Diagonal win check
        x_pos = 0
        y_pos = 0

        if self.layout[x_pos][y_pos] == self.layout[x_pos + 1][y_pos + 1] == self.layout[x_pos + 2][y_pos + 2] == mark:
            return True
        elif self.layout[x_pos][y_pos + 2] == self.layout[x_pos + 1][y_pos + 1] == self.layout[x_pos + 2][y_pos] == mark:
            return True

    def show(self):
        print(f'''
   1 2 3 
-----------
A| {self.layout[0][0]}|{self.layout[0][1]}|{self.layout[0][2]} 
B| {self.layout[1][0]}|{self.layout[1][1]}|{self.layout[1][2]} 
C| {self.layout[2][0]}|{self.layout[2][1]}|{self.layout[2][2]} 
        ''')


@dataclass
class Player:
    name: str
    turn_id: int = None
    sign: Mark = Mark.X
    count = 0

    def __post_init__(self):
        self.id = Player.count
        Player.count += 1
        if self.turn_id == 1:
            self.sign = self.sign.other

    def move(self, board: Board, row: int, col: int):
        if valid_move(board, row, col):
            board.layout[row - 1][col - 1] = self.sign
            board.show()
            return True
        return False


@dataclass
class Game:
    board: Board
    players: list[Player]

    def play(self) -> None:
        turn = 0
        while True:
            for player in self.players:
                if player.turn_id == turn % 2:
                    while True:
                        print(
                            f"{player.name} its you'r turn, whats you'r move?row(1 - 3)column(1 - 3)")
                        try:
                            row = int(input("Row(1 - 3): "))
                            col = int(input("Column(1 - 3): "))
                            if player.move(self.board, row, col):
                                if self.board.check_win(player.sign):
                                    print(f"{player.name} you have WON!")
                                    exit()
                                turn += 1
                                break
                        except ValueError:
                            print(
                                "Value for row and column must be NUMBER between 1 and 3, please try again!")

    @staticmethod
    def init_players() -> list[Player]:
        first_to_play = randint(0, 1)
        players: list[Player] = []
        for i in range(2):
            name = input(
                f"Please input you'r name Player{i + 1}: ").strip(" ").title()
            p = Player(name)
            if first_to_play != p.id:
                p.turn_id = 1
                p.sign = p.sign.other
            else:
                p.turn_id = 0
            players.append(p)
        return players

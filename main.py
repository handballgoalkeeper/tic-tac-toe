import os
from logic.models import Board, Game

b = Board([
    ["-", "-", "-"],
    ["-", "-", "-"],
    ["-", "-", "-"]
])

game = Game(b, Game.init_players())
game.play()

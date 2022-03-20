
from Position import Position
import random


class Player:

    def choose_move(self, position: Position):
        pass


class RandomPlayer(Player):

    def __init__(self):
        pass

    def choose_move(self, position: Position):
        moves = position.valid_moves()
        if len(moves) == 1:
            return moves[0]
        return moves[random.randint(0, len(moves)-1)]


class Perch1(Player):
    # First layer - 


    def __init__(self):
        pass

    def choose_move(self, position: Position):
        pass

    def eval_pos(self, position: Position):
        pass


from position.position import Position
import random


class Player:

    def __init__(self, name="Player"):
        self.name = name

    def choose_move(self, position: Position):
        pass


class RandomPlayer(Player):

    def __init__(self, name="RandomPlayer"):
        super(RandomPlayer, self).__init__(name)

    def choose_move(self, position: Position):
        moves = position.valid_moves()
        if len(moves) == 0:
            return None
        if len(moves) == 1:
            return moves[0]
        return moves[random.randint(0, len(moves)-1)]

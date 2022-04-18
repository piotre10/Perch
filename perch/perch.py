import torch
import numpy as np
import torch.nn as nn
from copy import deepcopy

from position.position import Position
from perch.player import Player
from utils.convert import pos_list_to_tensor


class Perch1(Player):
    input_size = 33
    queen_value = 3

    def __init__(self, layers=None):
        if layers is None:
            self.lin1 = nn.Linear(self.input_size, 8)
            self.act1 = nn.Tanh()
            self.lin2 = nn.Linear(8, 8)
            self.act2 = nn.Tanh()
            self.lin3 = nn.Linear(8, 1)
            self.last = nn.Sigmoid()

        else:
            self.lin1 = nn.Linear(self.input_size, layers[0])
            self.act1 = nn.Tanh()
            self.lin2 = nn.Linear(layers[0], layers[1])
            self.act2 = nn.Tanh()
            self.lin3 = nn.Linear(layers[1], 1)
            self.last = nn.Sigmoid()

    def choose_move(self, position: Position):  # Need moves[best] won't work (wrong type fix later)
        with torch.no_grad():
            positions = []
            moves = position.valid_moves()
            if len(moves) == 0:
                return None
            if len(moves) == 1:
                return moves[0]
            for mv in moves:
                temp = deepcopy(position)
                temp.move(mv)
                positions.append(temp)
            pos_tensor = pos_list_to_tensor(positions)
            evals = self.eval_positions(pos_tensor)
            if position.whos_move == 1:
                best = torch.argmax(evals)
            else:
                best = torch.argmin(evals)
        return moves[best]

    def eval_positions(self, positions_tensor: torch.tensor):
        ''' input: matrix 33 x n of n vectorized positions '''
        return self.foward(positions_tensor)

    def eval_pos(self, position: Position):
        input = np.array([position.get_as_vector()], dtype='float32').T
        input = torch.from_numpy(input)
        eval = self.foward(input)
        return eval

    def foward(self, inp: torch.tensor):
        res = self.lin1(inp)
        res = self.act1(res)
        res = self.lin2(res)
        res = self.act2(res)
        res = self.lin3(res)
        res = self.last(res)
        return res




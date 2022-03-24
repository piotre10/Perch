
from Position import Position
import random
import numpy as np


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

EPS = 0.5

def add_bias_term(matrix: np.array):
    """ Takes np matrix and adds bias term vector of 1's (horizontal) at the start of it """
    cols = matrix.shape[1]
    ones = np.ones((1, cols), dtype='float32')
    return np.vstack((ones, matrix))


def sigmoid(array: np.array):
    return 1 / (1+np.exp(-array))


def vectorize_positions(pos_list: list) -> np.array:
    res = np.array([pos_list[0].get_as_vector()], dtype='float32').T
    for i in range(1,len(pos_list)):
        next = np.array([pos_list[0].get_as_vector()], dtype='float32').T
        res = np.hstack(res,next)
    return res


class Perch1(Player):
    # First layer - 8 x 34
    # Second layer - 8 x 9
    # Third layer - 1 x 9


    def __init__(self, layers = None):
        if layers is None:
            self.FirstLayer = (np.random.rand(8, 34) - 0.5)*EPS
            self.SecondLayer = (np.random.rand(8, 9) - 0.5)*EPS
            self.ThirdLayer = (np.random.rand(1, 9) - 0.5)*EPS
        else:
            self.FirstLayer = layers[0]
            self.SecondLayer = layers[1]
            self.ThirdLayer = layers[2]

    def choose_move(self, position: Position): # Need moves[best] won't work (wrong type fix later)
        positions = []
        moves = position.valid_moves()
        for mv in moves:
            temp = position
            temp.move(mv[0], mv[1])
            positions.append(temp)
        evals = self.eval_positions(positions)
        if position.whos_move == 1:
            best = np.where(evals == np.amax(evals))
        else:
            best = np.where(evals == np.amin(evals))
        return moves[best]


    def eval_positions(self, positions_matrix: np.array):
        ''' input: matrix 33 x n of n vectorized positions'''
        return self.process_input(positions_matrix)

    def eval_pos(self, position: Position):
        input = np.array([position.get_as_vector()], dtype='float32').T
        print(input.shape)
        input = add_bias_term(input)
        eval = self.process_input(input)
        return eval

    def process_input(self, inp: np.array):
        t1 = sigmoid(np.matmul(self.FirstLayer, inp))
        t1 = add_bias_term(t1)
        t2 = sigmoid(np.matmul(self.SecondLayer, t1))
        t2 = add_bias_term(t2)
        return sigmoid(np.matmul(self.ThirdLayer, t2))



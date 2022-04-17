import torch

from position.position import Position
from pickle import HIGHEST_PROTOCOL


class PosDict:
    def __init__(self, name="PosDict"):
        self.positions = {}
        self.name = name

    def add_game(self, move_list: list, who_won: int):
        who_won = who_won*2 - 3

        pos = Position()
        for mv in move_list:
            pos.move(mv)
            temp = tuple(pos.get_as_vector())
            if temp in self.positions.keys():
                self.positions[temp][0] += who_won
                self.positions[temp][1] += 1
            else:
                self.positions[temp] = [who_won, 1]

    def save(self):
        torch.save(self.positions, f'saves/pos_dict_{self.name}.pth', pickle_protocol=HIGHEST_PROTOCOL)

    def load(self):
        self.positions = torch.load(f'saves/pos_dict_{self.name}.pth')

    def get_dict(self):
        return self.positions



from position.position import Position
from position.display import DispWindow
from perch.player import Player


class HumanPlayer(Player):

    def __init__(self, name="Human"):
        super(HumanPlayer, self).__init__(name)

    def choose_move(self, WIN: DispWindow):
        pass

from position.position import Position
from position.display import DispWindow
from perch.player import Player


class HumanPlayer(Player):

    def __init__(self, name="Human"):
        super(HumanPlayer, self).__init__(name)

    def choose_move(self, pos: Position, WIN = None):
        if WIN == None:
            moves = pos.valid_moves()
            while True:
                print(moves)
                try:
                    move_index = int(input('Choose move index (starting with 0): '))
                except:
                    print('Error please try again')
                    continue
                if 0 <= move_index < len(moves):
                    return moves[move_index]
                else:
                    print(f'Wrong index please choose value between 0 and {len(moves)}')
        else:
            mv = WIN.get_move(pos)
            return mv

import copy
from math import copysign
import random

STARTING_POS = [1, 1, 1, 1,
                1, 1, 1, 1,
                1, 1, 1, 1,
                0, 0, 0, 0,
                0, 0, 0, 0,
                2, 2, 2, 2,
                2, 2, 2, 2,
                2, 2, 2, 2]
DEFAULT_PAWNS = [[0,1,2,3,4,5,6,7,8,9,10,11],[20,21,22,23,24,25,26,27,28,29,30,31], [], []]
# move = ((START_POS,END_POS),(KILL1, KILL2, ...))
# all above are tuples (y, x) as cordinates in position matrix
# whos_move: white - 0 black - 1


class Position:

    __slots__ = ['pos_vec', 'whos_move', 'twenty_move_rule', 'pawns']

    def __init__(self, pos_vec=None, whos_move=1):
        self.pawns = [[], [], [], []]
        if pos_vec is None:
            self.pos_vec = copy.deepcopy(STARTING_POS)
            self.pawns = copy.copy(DEFAULT_PAWNS)
        else:
            self.pos_vec = copy.deepcopy(pos_vec)
            for index, pawn_id in enumerate(self.pos_vec):
                if pawn_id != 0:
                    self.pawns[pawn_id - 1].append(index)

        self.whos_move = whos_move
        self.twenty_move_rule = 0

    def __repr__(self):
        return str(self.whos_move)+' '+str(self.twenty_move_rule)+' '+repr(self.pos_vec)

    def __str__(self):
        return str(self.whos_move) + ' ' + str(self.twenty_move_rule) + '\n' + str(self.pos_vec)

    def randomize(self):
        self.pos_vec = [random.randint(0, 4)*random.randint(0, 1) for i in range(0, 32)]
        self.whos_move = random.randint(0, 1)

    def move(self, move: tuple):  # input move as specified at the start of file
        start, dest = move[0]
        kills = move[1]
        if self.pos_vec[start] > 2 and len(kills) == 0:
            self.twenty_move_rule += 1
        else:
            self.twenty_move_rule = 0

        pawn_id = self.pos_vec[start]
        self.pos_vec[start] = 0
        self.pawns[pawn_id - 1].remove(start)

        for kill in kills:
            killed_id = self.pos_vec[kill]
            self.pawns[killed_id-1].remove(kill)
            self.pos_vec[kill] = 0

        if (dest > 27 and pawn_id == 1) or (dest < 4 and pawn_id == 2):  # queening
            pawn_id += 2

        self.pos_vec[dest] = pawn_id
        self.pawns[pawn_id - 1].append(dest)

        self.whos_move = (self.whos_move + 1) % 2

    def valid_moves(self):   # consider possible moves()
        if self.capture_is_possible():
            return self.all_possible_captures()
        moves = []
        for pawn_pos in self.pawns[self.whos_move]:  # Pawn moves
            function_tuple = (self.go_up_left, self.go_up_right) if self.whos_move == 1 else (self.go_down_left,
                                                                                              self.go_down_right)
            for func in function_tuple:
                dest = func(pawn_pos)
                if dest is None:
                    continue
                if self.pos_vec[dest] == 0:
                    moves.append( ((pawn_pos, dest), ()) )

        for queen_pos in self.pawns[self.whos_move + 2]:   # Queen moves
            function_tuple = (self.go_up_left, self.go_down_left, self.go_up_right, self.go_down_right)
            for func in function_tuple:
                dest = func(queen_pos)
                while True:
                    if dest is None or self.pos_vec[dest] != 0:
                        break
                    else:
                        moves.append(((queen_pos, dest), ()))
                        dest = func(dest)

        return moves

    def set_starting_pos(self):
        self .pos_vec = copy.deepcopy(STARTING_POS)
        return self.pos_vec

    def all_possible_captures(self):
        capture_list = []
        for pawn_pos in self.pawns[self.whos_move] + self.pawns[self.whos_move+2]:
            captures = self.possible_captures(pawn_pos)
            if not captures:
                continue
            capture_list.extend(captures)

        return capture_list

    def move_is_valid(self, move: list):  # currently does NOT work
        print("Warning: Function is not working properly (work in progress)")
        start = move[0][0]
        dest = move[0][1]
        if not self.is_valid_tile_id(start) or not self.is_valid_tile_id(dest):
            return 0
        pawn_id = self.pos_vec[start]
        if (pawn_id + 1) % 2 != self.whos_move:
            return 0
        if self.pos_vec[dest] != 0:
            return 0
        if pawn_id == 0:
            return 0  # 0-black 1-white
        if pawn_id < 3:  # pawn
            if len(move[1]) == 1:  # one capture
                killed_pos = move[1][0]
                killed_pawn_id = self.matrix[killed_pos[0]][killed_pos[1]]
                if killed_pawn_id == 0:
                    return 0
                diag = self.is_on_same_diagonal(start, killed_pos)
                if diag == self.is_on_same_diagonal(dest, killed_pos) and diag != 0:  # same diagonal
                    if start[0]+dest[0] == 2 * killed_pos[0]:  # killed between start and end
                        if abs(start[0] - dest[0]) == 2:  # start and end two tiles apart
                            if killed_pawn_id % 2 != self.whos_move:  # dont capture own pawn
                                return 1
            elif len(move[1]) == 0:  # zero captures
                if self.is_on_same_diagonal(start, dest):  # is the same diagonal
                    if dest[0] - start[0] == 2 * self.whos_move - 1:  # one tile apart in good direction
                        return 1

        else:  # queen
            if len(move[1]) == 0:  # zero captures
                if self.is_on_same_diagonal(start, dest):  # same diagonal
                    return 1
            elif len(move[1]) == 1:  # one capture
                killed_pos = move[1][0]
                diag = self.is_on_same_diagonal(start, killed_pos)
                if diag == self.is_on_same_diagonal(dest, killed_pos) and diag != 0:  # same diagonal
                    if copysign(1, start[0]-killed_pos[0]) == copysign(1, killed_pos[0]-dest[0]):
                        # killed between start and end
                        return 1
        return 0

    def possible_jumps(self, pawn_pos, pawn_id=None):
        """return list of avilable jumps if there is possible capture from pawn_pos and empty list if not"""
        jumps = []  # list of available jumps as: [move1, move2, move3,...]
        if pawn_id is None:
            pawn_id = self.pos_vec[pawn_pos]
        if pawn_id == 0:
            return []
        function_tuple = (self.go_up_left, self.go_down_left, self.go_up_right, self.go_down_right)
        if pawn_id < 3:
            for func in function_tuple:
                killed = func(pawn_pos)
                if killed is None or self.tile_is_empty(killed) or self.is_pawns_move(killed):
                    continue
                dest = func(killed)
                if dest is not None and self.pos_vec[dest] == 0:
                    jumps.append(((pawn_pos, dest), (killed,)))
        else:
            for func in function_tuple:
                pos = func(pawn_pos)
                kills = []
                while pos is not None:
                    temp_pawn_id = self.pos_vec[pos]
                    if self.is_pawns_move(pos):
                        break
                    elif temp_pawn_id == 0:
                        if kills:
                            jumps.append(((pawn_pos, pos), tuple(kills)))
                        pos = func(pos)
                        continue
                    else:
                        killed_pos = pos
                        pos = func(pos)
                        if self.pos_vec[pos] == 0:
                            kills.append(killed_pos)
                            continue
                        else:
                            break
        print(jumps)
        return jumps

    def possible_moves(self, pawn_pos: int, pawn_id=None):
        if self.possible_jumps(pawn_pos, pawn_id):
            return None

        if pawn_id is None:
            pawn_id = self.pos_vec[pawn_pos]

        moves = []
        if pawn_id < 3:
            function_tuple = (self.go_up_left, self.go_up_right) if (pawn_id + 1) % 2 == 1 else (self.go_down_left,
                                                                                                 self.go_down_right)
            for func in function_tuple:
                dest = func(pawn_pos)
                if dest is None:
                    continue
                if self.pos_vec[dest] == 0:
                    moves.append(((pawn_pos, dest), ()))

        else:
            function_tuple = (self.go_up_left, self.go_down_left, self.go_up_right, self.go_down_right)
            for func in function_tuple:
                dest = func(pawn_pos)
                while True:
                    if dest is None or self.pos_vec[dest] != 0:
                        break
                    else:
                        moves.append(((pawn_pos, dest), ()))
                        dest = func(dest)
        return moves

    def possible_captures(self, pawn_pos, pawn_id=None):
        if pawn_id is None:
            pawn_id = self.pos_vec[pawn_pos]
        if not self.possible_jumps(pawn_pos, pawn_id):
            return None
        captures = self.possible_jumps(pawn_pos, pawn_id)
        all_captures = []
        for capture in captures:
            start, dest = capture[0]
            temp = copy.deepcopy(self)
            temp.move(capture)
            temp.toggle_whos_move()
            next_captures = temp.possible_captures(dest, pawn_id)
            if next_captures is None:
                if capture not in all_captures:
                    all_captures.append(capture)
                continue
            for capt in next_captures:
                new_dest = capt[0][1]
                new_capture = ((start, new_dest), capture[1] + capt[1])
                if new_capture not in all_captures:
                    all_captures.append(new_capture)
        if not all_captures:
            return None
        return all_captures

    def capture_is_possible(self):  # returns 0 if there is no possible capture and 1 otherwise
        for pawn_pos in self.pawns[self.whos_move+2] + self.pawns[self.whos_move]:
            if self.possible_jumps(pawn_pos):
                return 1
        return 0

    def is_win(self):
        """last_move is color of last player who moved, returns 0 if there is no win 1 if black wins 2 if white wins"""
        if len(self.valid_moves()) == 0:
            return self.whos_move + 1
        return 0

    def is_end(self):
        """returns 1 if black wins 2 if white wins 0 if game ended in a draw and -1 if game shall proceed"""
        if self.is_win():
            return self.is_win()

        elif self.twenty_move_rule == 20:
            return 0

        return -1

    def get_as_vector(self):
        return [self.whos_move] + self.pos_vec

    def is_pawns_move(self, pawn_pos):
        return self.pos_vec[pawn_pos] != 0 and (self.pos_vec[pawn_pos] + 1) % 2 == self.whos_move

    def tile_is_empty(self, pos):
        return self.pos_vec[pos] == 0

    def toggle_whos_move(self):
        self.whos_move = (self.whos_move + 1) % 2

    @classmethod
    def is_on_same_diagonal(cls, pos1, pos2):  # pos are tuples as dicriebed above
        #  returns 1 or 2 if true (depending on direction diagonal is pointing) 0 if false
        if pos1[0]//2 + pos1[1] == pos2[0]//2 + pos2[1]:  # right diagonal -> ///
            return 1
        if (pos1[0] + 1) // 2 - pos1[1] == (pos2[0] + 1) // 2 - pos2[1]:  # left diagonal -> \\\
            return 2
        return 0

    @classmethod
    def is_valid_tile_id(cls, tested_id: int):
        return 0 <= tested_id < 32

    @classmethod
    def go_up_left(cls, pos: int):
        if pos < 4 or pos % 8 == 4:  # either top or left side of the board
            return None
        temp = 1 if pos % 8 > 3 else 0
        new_pos = pos - 4 - temp
        return new_pos

    @classmethod
    def go_up_right(cls, pos: int):
        if pos < 4 or pos % 8 == 3:  # either top or right side of the board
            return None
        temp = 1 if pos % 8 > 3 else 0
        new_pos = pos - 3 - temp
        return new_pos

    @classmethod
    def go_down_left(cls, pos: int):
        if pos > 27 or pos % 8 == 4:  # either bottom or left side of the board
            return None
        temp = 1 if pos % 8 > 3 else 0
        new_pos = pos + 4 - temp
        return new_pos

    @classmethod
    def go_down_right(cls, pos: int):
        if pos > 27 or pos % 8 == 3:  # either bottom or right side of the board
            return None
        temp = 1 if pos % 8 > 3 else 0
        new_pos = pos + 5 - temp
        return new_pos

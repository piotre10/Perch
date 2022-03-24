import copy
from math import copysign

STARTING_POS = [[1, 1, 1, 1],
                [1, 1, 1, 1],
                [1, 1, 1, 1],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [2, 2, 2, 2],
                [2, 2, 2, 2],
                [2, 2, 2, 2]]

# move = [[START_POS,END_POS],[KILL1, KILL2, ...]]
# all above are tuples (y, x) as cordinates in position matrix
# whos_move: white - 1 black - 0


class Position:

    __slots__ = ['matrix', 'whos_move', 'twenty_move_rule']

    def __init__(self, matrix=STARTING_POS, whos_move = 0):
        self.matrix = copy.deepcopy(matrix)
        self.whos_move = whos_move
        self.twenty_move_rule = 0

    def __repr__(self):
        return str(self.whos_move)+' '+str(self.twenty_move_rule)+' '+repr(self.matrix)

    def __str__(self):
        return str(self.whos_move) + ' ' + str(self.twenty_move_rule) + '\n' + str(self.matrix)

    def move(self, move: list, kills):  # input to lista z dwoma krotkami
        x, y = move[0]
        z, w = move[1]
        if self.matrix[x][y] > 2 and len(kills) == 0:
            self.twenty_move_rule += 1
        else:
            self.twenty_move_rule = 0
        self.matrix[z][w] = self.matrix[x][y]
        self.matrix[x][y] = 0
        if z == 7 and self.matrix[z][w] == 1:
            self.matrix[z][w] = 3
        if z == 0 and self.matrix[z][w] == 2:
            self.matrix[z][w] = 4
        for kill in kills:
            self.matrix[kill[0]][kill[1]] = 0
        self.whos_move = (self.whos_move + 1) % 2
        return self.matrix

    def valid_moves(self):    #Queen moves!!!!
        if self.capture_is_possible():
            return self.possible_captures()
        pos_moves = []
        for x in range(0, 4):
            for y in range(0, 8):
                if self.matrix[y][x] == 0 or self.matrix[y][x] % 2 != self.whos_move:
                    continue  # empty tile or enemy pawn so go next
                start_pos = (y, x)
                function_tuple = (self.go_up_left, self.go_down_left, self.go_up_right, self.go_down_right)
                if self.matrix[y][x] < 3:  # Pawn moves
                    for func in function_tuple:
                        end_pos = func(start_pos)
                        if end_pos != 0 and (end_pos[0]-start_pos[0])*(2*self.whos_move - 1) > 0:
                            if self.matrix[end_pos[0]][end_pos[1]] != 0:
                                continue
                            pos_moves.append([[start_pos, end_pos], []])
                else:  # Queen moves
                    for func in function_tuple:
                        end_pos = func(start_pos)
                        while True:
                            if end_pos == 0 or self.matrix[end_pos[0]][end_pos[1]] != 0:
                                break
                            else:
                                pos_moves.append([[start_pos, end_pos], []])
                                end_pos = func(end_pos)

        return pos_moves

    def set_starting_pos(self):
        self.matrix = copy.deepcopy(STARTING_POS)
        return self.matrix

    def possible_captures(self):
        capture_list = []
        for x in range(0, 4):
            for y in range(0, 8):
                if self.matrix[y][x] == 0 or self.matrix[y][x] % 2 != self.whos_move:
                    continue  # empty tile or enemy pawn so go next
                start_pos = (y, x)
                captures = self.possible_jumps(start_pos)
                if len(captures) == 0:
                    continue
                for capture in captures:
                    temp = copy.deepcopy(self)
                    temp.move(capture[0],capture[1])
                    jumps = temp.possible_jumps(capture[0][1], self.matrix[y][x])
                    for jump in jumps:
                        new_capture = [[capture[0][0], jump[0][1]], capture[1]+jump[1]]
                        captures.append(new_capture)
                    if len(jumps) != 0:
                        captures.remove(capture)

                capture_list.extend(captures)

        return capture_list

    def move_is_valid(self, move: list):  # works if there wasnt multiple captures! (to add recursive multiple captures)
        start_pos = move[0][0]
        end_pos = move[0][1]
        if not self.is_valid_tile_id(start_pos) or not self.is_valid_tile_id(end_pos):
            return 0
        pawn_id = self.matrix[start_pos[0]][start_pos[1]]
        if pawn_id % 2 != self.whos_move:
            return 0
        if self.matrix[end_pos[0]][end_pos[1]] != 0:
            return 0
        if pawn_id == 0:
            return 0
        whos_move = pawn_id % 2  # 0-black 1-white
        if pawn_id < 3:  # pawn
            if len(move[1]) == 1:  # one capture
                killed_pos = move[1][0]
                killed_pawn_id = self.matrix[killed_pos[0]][killed_pos[1]]
                if killed_pawn_id == 0:
                    return 0
                diag = self.is_on_same_diagonal(start_pos, killed_pos)
                if diag == self.is_on_same_diagonal(end_pos, killed_pos) and diag != 0:  # same diagonal
                    if start_pos[0]+end_pos[0] == 2 * killed_pos[0]:  # killed between start and end
                        if abs(start_pos[0] - end_pos[0]) == 2:  # start and end two tiles apart
                            if killed_pawn_id % 2 != whos_move:  # dont capture own pawn
                                return 1
            elif len(move[1]) == 0:  # zero captures
                if self.is_on_same_diagonal(start_pos, end_pos):  # is the same diagonal
                    if end_pos[0] - start_pos[0] == 2 * whos_move - 1:  # one tile apart in good direction
                        return 1

        else:  # queen
            if len(move[1]) == 0:  # zero captures
                if self.is_on_same_diagonal(start_pos, end_pos):  # same diagonal
                    return 1
            elif len(move[1]) == 1:  # one capture
                killed_pos = move[1][0]
                diag = self.is_on_same_diagonal(start_pos, killed_pos)
                if diag == self.is_on_same_diagonal(end_pos, killed_pos) and diag != 0:  # same diagonal
                    if copysign(1, start_pos[0]-killed_pos[0]) == copysign(1, killed_pos[0]-end_pos[0]):
                        # killed between start and end
                        return 1
        return 0

    def possible_jumps(self, pawn_pos, pawn_id=-1):
        """return list of avilable jumps if there is possible capture from pawn_pos and empty list if not"""
        res = []  # list of available jumps as: [move1, move2, move3,...]
        if pawn_id == -1:
            pawn_id = self.matrix[pawn_pos[0]][pawn_pos[1]]
        if pawn_id == 0:
            return []
        if pawn_id < 3:
            possible_ends = [(pawn_pos[0]-2, pawn_pos[1]-1), (pawn_pos[0]-2, pawn_pos[1]+1),
                             (pawn_pos[0]+2, pawn_pos[1]-1), (pawn_pos[0]+2, pawn_pos[1]+1)]
            for end_pos in possible_ends:
                if self.is_valid_tile_id(end_pos):
                    if self.matrix[end_pos[0]][end_pos[1]] == 0:
                        killed_pos = (int((pawn_pos[0] + end_pos[0]) / 2),
                                      int((pawn_pos[1] + end_pos[1]) // 2 + ((pawn_pos[0] + 1) % 2)))
                        killed_pawn_id = self.matrix[killed_pos[0]][killed_pos[1]]
                        if killed_pawn_id == 0:
                            continue
                        if killed_pawn_id % 2 == (pawn_id+1) % 2:
                            res.append([[pawn_pos, end_pos], [killed_pos]])
        else:
            function_tuple = (self.go_up_left, self.go_down_left, self.go_up_right, self.go_down_right)
            for func in function_tuple:
                pos = pawn_pos
                pos = func(pos)
                while pos:
                    temp_pawn_id = self.matrix[pos[0]][pos[1]]
                    if temp_pawn_id == 0:
                        pos = func(pos)
                        continue
                    if temp_pawn_id % 2 == (pawn_id+1) % 2:
                        killed_pos = pos
                        pos = func(pos)
                        while pos and self.matrix[pos[0]][pos[1]] == 0:
                            res.append([[pawn_pos, pos], [killed_pos]])
                            pos = func(pos)
                    break
        return res

    def capture_is_possible(self):  # returns 0 if there is no possible capture and 1 otherwise
        for row in range(0, 8):
            for col in range(0, 4):
                if self.matrix[row][col] == 0:
                    continue
                if self.matrix[row][col] % 2 == self.whos_move:
                    if self.possible_jumps((row, col)):
                        return 1
        return 0

    def is_win(self):
        """last_move is color of last player who moved, returns 0 if there is no win 1 if black wins 2 if white wins"""
        if len(self.valid_moves()) == 0:
            return (self.whos_move + 1) % 2 + 1
        return 0

    def is_end(self):
        """returns 1 if black wins 2 if white wins 0 if game ended in a draw and -1 if game shall proceed"""
        if self.is_win():
            return self.is_win()

        elif self.twenty_move_rule == 20:
            return 0

        return -1

    @classmethod
    def is_on_same_diagonal(cls, pos1, pos2):  # pos are tuples as dicriebed above
        #  returns 1 or 2 if true (depending on direction diagonal is pointing) 0 if false
        if pos1[0]//2 + pos1[1] == pos2[0]//2 + pos2[1]:  # right diagonal -> ///
            return 1
        if (pos1[0] + 1) // 2 - pos1[1] == (pos2[0] + 1) // 2 - pos2[1]:  # left diagonal -> \\\
            return 2
        return 0

    @classmethod
    def is_valid_tile_id(cls, tested_id: tuple):
        x = tested_id[1]
        y = tested_id[0]
        return (x >= 0) and (x < 4) and (y >= 0) and (y < 8)

    @classmethod
    def go_up_left(cls, pos):
        new_pos = (pos[0]-1, pos[1]-(pos[0] % 2))
        if cls.is_valid_tile_id(new_pos):
            return new_pos
        return 0

    @classmethod
    def go_up_right(cls, pos):
        new_pos = (pos[0]-1, pos[1]-(pos[0] % 2)+1)
        if cls.is_valid_tile_id(new_pos):
            return new_pos
        return 0

    @classmethod
    def go_down_left(cls, pos):
        new_pos = (pos[0] + 1, pos[1] - (pos[0] % 2))
        if cls.is_valid_tile_id(new_pos):
            return new_pos
        return 0

    @classmethod
    def go_down_right(cls, pos):
        new_pos = (pos[0] + 1, pos[1] - (pos[0] % 2) + 1)
        if cls.is_valid_tile_id(new_pos):
            return new_pos
        return 0

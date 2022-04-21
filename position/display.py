import copy

import pygame
import os
from position.position import Position

#  General game constants
WIDTH, HEIGHT = 900, 700

FPS = 30

# Colors
BACKGROUND_COLOR = (181, 146, 96)
BLACK = (0, 0, 0)

# Board and pawns constants definitions
BOARD_SIZE = 600
BOARD_POS = (0, 50)
BOARD_PICTURE = pygame.image.load(os.path.join('Pictures', "board.jpg"))
BOARD = pygame.transform.scale(BOARD_PICTURE, (BOARD_SIZE, BOARD_SIZE))
BOARD_BORDER_WIDTH = BOARD_SIZE*22/1000  # Size of the board's border (it takes 22/1000 of original image)
TILE_SIZE = (BOARD_SIZE-(2*BOARD_BORDER_WIDTH))/8
TILE_FRAME_PICTURE = pygame.image.load(os.path.join('Pictures', "tile_frame.png"))
TILE_FRAME = pygame.transform.scale(TILE_FRAME_PICTURE, (int(TILE_SIZE)+2, int(TILE_SIZE)+1))
#                                                        Don't know why bot works just perfect with 2 and 1
PAWN_SIZE = int(TILE_SIZE * 0.8)
FIRST_PAWN_DIST = BOARD_BORDER_WIDTH+((TILE_SIZE-PAWN_SIZE)/2)  # distance from border of the board to
#                                                                pawn pos such the pawn is centered on the tile
WHITE_PAWN_PICTURE = pygame.image.load(os.path.join('Pictures', "white_pawn.png"))
WHITE_PAWN = pygame.transform.scale(WHITE_PAWN_PICTURE, (PAWN_SIZE, PAWN_SIZE))
WHITE_QUEEN_PICTURE = pygame.image.load(os.path.join('Pictures', "white_queen.png"))
WHITE_QUEEN = pygame.transform.scale(WHITE_QUEEN_PICTURE, (PAWN_SIZE, PAWN_SIZE))
BLACK_PAWN_PICTURE = pygame.image.load(os.path.join('Pictures', "black_pawn.png"))
BLACK_PAWN = pygame.transform.scale(BLACK_PAWN_PICTURE, (PAWN_SIZE, PAWN_SIZE))
BLACK_QUEEN_PICTURE = pygame.image.load(os.path.join('Pictures', "black_queen.png"))
BLACK_QUEEN = pygame.transform.scale(BLACK_QUEEN_PICTURE, (PAWN_SIZE, PAWN_SIZE))

#  TUPLES
PAWN_TUPLE = (WHITE_PAWN, BLACK_PAWN, WHITE_QUEEN, BLACK_QUEEN)
WHOS_MOVE_TUPLE = ("White", "Black")

#  Fonts
pygame.font.init()
WHOS_MOVE_FONT = pygame.font.SysFont('cambria', 16)
USER_FONT = pygame.font.SysFont('comicsans', 20)

# Defining user events and errors
FATAL_ERROR = pygame.USEREVENT + 1
EXCEPTION = pygame.USEREVENT + 2
WHITE_WINS = pygame.USEREVENT + 3
BLACK_WINS = pygame.USEREVENT + 4
ENDED_IN_DRAW = pygame.USEREVENT + 5
WRONG_TILE_ID = (-1, -1)
INVALID_MOVE = [[WRONG_TILE_ID, WRONG_TILE_ID], []]

# Higlighting

TILE_RECT = pygame.Rect((BOARD_POS[0] + BOARD_BORDER_WIDTH, BOARD_POS[1] + BOARD_BORDER_WIDTH),
                              (TILE_SIZE + 2, TILE_SIZE + 3))
FRAME_COLOR = (252, 219, 3)
SHADOW_COLOR = (245, 117, 100)

# User display constants
USER_IMAGE_SIZE = 48


class DispWindow:
    def __init__(self, width=WIDTH, height=HEIGHT):
        self.width = width
        self.height = height
        self.WINDOW = None

    def open(self):
        pygame.display.init()
        self.WINDOW = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Checkers!")

    @staticmethod
    def close():
        pygame.display.quit()

    def update(self, game_position: Position, tiles_to_highlight = (), tiles_to_shadow = ()):
        self.WINDOW.fill(BACKGROUND_COLOR)
        self.WINDOW.blit(BOARD, BOARD_POS)
        for tile in tiles_to_shadow:
            self.__tile_put_shadow(tile)
        self.__display_position(game_position)
        for tile in tiles_to_highlight:
            self.__tile_highlight(tile)
        self.__display_who_to_move(game_position.whos_move)
        pygame.display.update()

    @staticmethod
    def quit_event():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 1
        return 0

    def get_move(self, pos: Position):
        self.update(pos)
        highlights = []
        shadows = []
        move_dict = {}
        is_first_click = True
        is_locked = False
        start = dest = -1
        kills = []
        temp = copy.deepcopy(pos)
        while True:
            self.update(temp, highlights, shadows)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.close()
                if event.type == pygame.MOUSEBUTTONUP:
                    clicked = self.__id_of_tile(pygame.mouse.get_pos())
                    if is_first_click:
                        if clicked is not None and pos.is_pawns_move(clicked):
                            start = clicked
                            highlights = [clicked]
                            move_dict = self.__get_shadows(pos, clicked)
                            shadows = list(move_dict.keys())

                            is_first_click = False
                    else:

                        if clicked is None or clicked not in shadows:
                            if not is_locked:
                                highlights = []
                                move_dict = {}
                                shadows = []
                                is_first_click = True
                            continue

                        move = move_dict[clicked]

                        if not move[1]:
                            return move
                        else:
                            kills.extend(move[1])
                            dest = move[0][1]
                            temp.move(move)
                            temp.toggle_whos_move()
                            highlights = [dest]
                            move_dict = self.__get_shadows(temp, move[0][1], kill=1)
                            shadows = list(move_dict.keys())
                            is_locked = True
                            if not shadows:
                                mv = ((start, dest), tuple(kills))
                                return mv



    @staticmethod
    def __get_shadows(pos: Position, pawn_pos: int, kill=0):
        moves = []
        if pos.capture_is_possible():
            moves = pos.possible_jumps(pawn_pos)
        elif not kill:
            moves = pos.possible_moves(pawn_pos)

        return {move[0][1]: move for move in moves}

    @staticmethod
    def __id_of_tile(cord):
        if cord[0] > BOARD_POS[0] + BOARD_BORDER_WIDTH and cord[1] > BOARD_POS[1] + BOARD_BORDER_WIDTH:
            x = (cord[0] - (BOARD_POS[0] + BOARD_BORDER_WIDTH)) // TILE_SIZE
            y = (cord[1] - (BOARD_POS[1] + BOARD_BORDER_WIDTH)) // TILE_SIZE
            if 0 <= x < 8 and 0 <= y < 8:
                if (x + y) % 2 == 1:
                    return 4*int(y) + int(x)//2
        return None

    def __tile_highlight(self, tile_id: int):
        ''' highlights black tile defined by tile_id (if such exists) '''
        if tile_id is None:
            return
        if Position.is_valid_tile_id(tile_id):
            pygame.draw.rect(self.WINDOW, FRAME_COLOR, self.__move_rect_on_tile(TILE_RECT, tile_id), 2)

    def __tile_put_shadow(self, tile_id: int):
        if tile_id is None:
            return
        if Position.is_valid_tile_id(tile_id):
            pygame.draw.rect(self.WINDOW, SHADOW_COLOR, self.__move_rect_on_tile(TILE_RECT, tile_id))

    def __display_position(self, game_position: Position):
        position = game_position.pos_vec
        for row in range(0, 8):
            for col in range(0, 4):
                pawn_id = position[4*row+col]
                if pawn_id != 0:
                    try:
                        pawn = PAWN_TUPLE[pawn_id - 1]
                    except IndexError:
                        print("Invalid position")
                        break
                    self.WINDOW.blit(pawn, (BOARD_POS[0] + FIRST_PAWN_DIST + ((2 * col + ((row + 1) % 2)) * TILE_SIZE),
                                            BOARD_POS[1] + FIRST_PAWN_DIST + (row * TILE_SIZE)))

    def __display_who_to_move(self, whos_move):  # 1-black 0-white
        text = "{} to move".format(WHOS_MOVE_TUPLE[whos_move])
        draw_text = WHOS_MOVE_FONT.render(text, True, BLACK)
        self.WINDOW.blit(draw_text,
                        (BOARD_POS[0] + BOARD_SIZE + 50, BOARD_POS[1] + (BOARD_SIZE - draw_text.get_height()) / 2))
        # 50 is padding
        self.WINDOW.blit(PAWN_TUPLE[whos_move],
                     (BOARD_POS[0] + BOARD_SIZE + 50 + (draw_text.get_width() - PAWN_SIZE) / 2,
                      BOARD_POS[1] + (BOARD_SIZE / 2) + draw_text.get_height()))

    @staticmethod
    def __move_rect_on_tile(rect: pygame.Rect, tile_id):
        y = tile_id // 4
        temp = 0
        if tile_id % 8 < 4:
            temp = 1
        x = 2 * (tile_id % 4) + temp
        return rect.move(x*TILE_SIZE, y*TILE_SIZE)

from Position import *
import Perch
import pygame
import os
import time




#  General game constants
WIDTH, HEIGHT = 900, 700
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Checkers!")
FPS = 30

# Colors
BACKGROUND_COLOR = (181, 146, 96)
BLACK = (0, 0, 0)

# Board and pawns constants definitions
BOARD_SIZE = 500
BOARD_POS = (0, 100)
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
WHOS_MOVE_TUPLE = ("Black", "White")

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

# User display constants
USER_IMAGE_SIZE = 48

# TESTING
TESTING_POS = [[1, 1, 1, 1],
               [1, 1, 1, 1],
               [1, 0, 1, 1],
               [0, 1, 2, 0],
               [0, 0, 0, 0],
               [2, 0, 2, 2],
               [2, 2, 2, 2],
               [2, 2, 2, 2]]

def update_window(game_position: Position):
    WINDOW.fill(BACKGROUND_COLOR)
    WINDOW.blit(BOARD, BOARD_POS)
    display_position(game_position)
    display_who_to_move(game_position.whos_move)
    pygame.display.update()

def throw_error(error_message: str):
    print("Fatal Error: {}".format(error_message))
    pygame.event.post(pygame.event.Event(FATAL_ERROR))


def throw_exception(exception_message: str):
    print("Exception: {}".format(exception_message))
    pygame.event.post((pygame.event.Event(EXCEPTION)))


def display_position(game_position: Position):
    position = game_position.matrix
    for row in range(0, 8):
        for col in range(0, 4):
            pawn_id = position[row][col]
            if pawn_id != 0:
                try: pawn = PAWN_TUPLE[pawn_id-1]
                except IndexError:
                    throw_error("Invalid position")
                    break
                WINDOW.blit(pawn, (BOARD_POS[0]+FIRST_PAWN_DIST + ((2 * col+((row + 1) % 2)) * TILE_SIZE),
                                   BOARD_POS[1]+FIRST_PAWN_DIST + (row * TILE_SIZE)))


def display_who_to_move(whos_move):  # 0-black 1-white
    text = "{} to move".format(WHOS_MOVE_TUPLE[whos_move])
    draw_text = WHOS_MOVE_FONT.render(text, True, BLACK)
    WINDOW.blit(draw_text, (BOARD_POS[0]+BOARD_SIZE+50, BOARD_POS[1]+(BOARD_SIZE-draw_text.get_height())/2))
    # 50 is padding
    WINDOW.blit(PAWN_TUPLE[not whos_move], (BOARD_POS[0]+BOARD_SIZE+50+(draw_text.get_width()-PAWN_SIZE)/2,
                                        BOARD_POS[1] + (BOARD_SIZE/2) + draw_text.get_height()))


if __name__ == '__main__':
    player1 = Perch.RandomPlayer()
    player2 = Perch.RandomPlayer()

    player_tuple = (player1, player2)

    game_position = Position(TESTING_POS, 1)

    run = True
    clock = pygame.time.Clock()

    FPS = 30
    update_window(game_position)
    time.sleep(1)
    while run:
        clock.tick(FPS)

        if game_position.is_end() != -1:
            run = False
            continue
        update_window(game_position)
        move = player_tuple[game_position.whos_move].choose_move(game_position)
        print(move)
        game_position.move(move[0], move[1])
        update_window(game_position)
        time.sleep(0.5)

    print(game_position.is_end())

from position.position import *
from position.display import DispWindow
import perch.perch as Perch
import pygame
import os
import time



# TESTING
TESTING_POS = [[4, 0, 0, 0],
               [0, 0, 0, 0],
               [4, 0, 0, 0],
               [0, 0, 1, 0],
               [0, 0, 2, 0],
               [3, 0, 0, 1],
               [0, 2, 0, 0],
               [0, 0, 1, 0]]


def speed_of_moves(player: Perch.Player, noMoves = 1000):
    t = 0
    for i in range(0, noMoves):
        position = Position()
        position.randomize()
        start = time.time()
        player.choose_move(position)
        end = time.time()
        t += end - start
    return t


if __name__ == '__main__':

    player1 = Perch.RandomPlayer()
    player2 = Perch.RandomPlayer()

    player_tuple = (player1, player2)

    game_position = Position()

    run = True
    clock = pygame.time.Clock()

    FPS = 30
    WIN = DispWindow()
    WIN.init_window()
    WIN.update_window(game_position)
    time.sleep(1)
    while run:
        clock.tick(FPS)

        if game_position.is_end() != -1:
            run = False
            continue
        WIN.update_window(game_position)
        move = player_tuple[game_position.whos_move].choose_move(game_position)
        game_position.move(move[0], move[1])
        WIN.update_window(game_position)
        time.sleep(0.1)

    print(game_position.is_end())
    WIN.close_window()

    #print(speed_of_moves(Perch.Perch1(), 32000))

import copy
import timeit
from statistics import mean
import pygame
import time

import torch
import sqlite3

import bitstruct
from position.display import DispWindow
from position.position import Position
from perch.player import Player, RandomPlayer
from perch.perch import Perch1
import utils.game as gm
from perch.human import HumanPlayer
from utils.posdict import PosDict
from utils.posdb import PosDB
from utils.convert import pos_vec_turn_normal_to_bias
import matplotlib.pyplot as plt
from torch.utils.tensorboard import SummaryWriter
import keyboard

# TESTING
TESTING_POS = [1, 4, 0, 2, 0, 1, 0, 1, 0, 1, 0, 0, 3, 0, 3, 0, 1, 1, 0, 0, 2, 0, 0, 0, 2, 2, 2, 2, 0, 2, 0, 0]


def speed_of_moves(player: Player, noMoves = 1000):
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
    setup = '''
import utils.game as gm
from perch.player import RandomPlayer
from position.position import Position

pl1 = RandomPlayer()
pl2 = RandomPlayer()'''

    t = timeit.repeat('gm.fast_game(pl1,pl2)', setup=setup, number=100)
    print(t, mean(t))



"""
    pl1 = RandomPlayer()
    pl2 = RandomPlayer()
    pos_dict = PosDict('random')
    pos_db = PosDB('test2')
    mode = int(input("Choose mode (1-adding games 2-print parameters):"))
    pos_db.create_connection()
    if pos_db.is_connected():
        pos_db.init_cursor()
        pos_db.create_pos_table()
        if mode == 1:
            gm.keep_adding_games(pl1, pl2, pos_db)
        elif mode == 2:
            games_to_test = int(input("How many games to play: "))
            records0 = pos_db.get_num_records()
            print("Playing games")
            t0 = timeit.default_timer()
            gm.add_games(pl1, pl2, pos_db, num_games=games_to_test)
            t1 = timeit.default_timer()
            print("Calculating statistics")
            records = pos_db.get_num_records()
            if games_to_test != 0:
                av_record_growth = (records - records0) / games_to_test
            else:
                av_record_growth = None
            av_game_quantity = pos_db.get_average_num_games()
            single_games = pos_db.get_num_single_games()

            print(f'''Parameters:
                average new records: {av_record_growth}
                average game quantity: {av_game_quantity}
                number of all records: {records}
                single games: {single_games}
                time of adding {games_to_test} games: {t1 - t0}
                speed games/s: {games_to_test / (t1 - t0)}''')
        elif mode == 3:
            t0 = timeit.default_timer()
            print(pos_db.get_num_records())
            t1 = timeit.default_timer()
            print(f'{t1 - t0}')
        pos_db.commit()
        print('Commited')
        pos_db.close_connection()
        print('Closed connection')
"""
    #pl1 = RandomPlayer()
    #pl2 = RandomPlayer()
    #moves, who_won = gm.play_game(pl1, pl2)

    #pos = Position(TESTING_POS, 0)
    #gm.display_position(pos)

    #print(pos.valid_moves())
    #gm.display_position(pos)


    #setup = '''
#import utils.game as gm
#from perch.player import RandomPlayer
#from position.position import Position

#pl1 = RandomPlayer()
#pl2 = RandomPlayer()'''

    #t = timeit.repeat('gm.play_game(pl1,pl2)', setup=setup, number=10000)
    #print(t, mean(t))





'''
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
'''

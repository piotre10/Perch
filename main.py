import timeit

import pygame
import time

import torch
import sqlite3

from position.position import Position
from perch.player import Player, RandomPlayer
from perch.perch import Perch1
import utils.game as gm
from utils.posdict import PosDict
from utils.posdb import PosDB
from utils.convert import pos_vec_turn_normal_to_bias
import matplotlib.pyplot as plt
from torch.utils.tensorboard import SummaryWriter
import keyboard

# TESTING
TESTING_POS = [[4, 0, 0, 0],
               [0, 0, 0, 0],
               [4, 0, 0, 0],
               [0, 0, 1, 0],
               [0, 0, 2, 0],
               [3, 0, 0, 1],
               [0, 2, 0, 0],
               [0, 0, 1, 0]]


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

    big_number = 12345678900
    pl1 = RandomPlayer()
    pl2 = RandomPlayer()
    pos_dict = PosDict('random')
    pos_db = PosDB('test')
    pos_db.create_connection()
    if pos_db.is_connected():
        pos_db.init_cursor()
        pos_db.create_pos_table()
        total_time = 0
        gm.add_games(pl1, pl2, pos_db, num_games=10)

        pos_db.commit()
        pos_db.close_connection()
    #conn = sqlite3.connect('databases/test.db')

    #conn.close()
    #pos_dict.load()
    #gm.keep_adding_games(pl1, pl2, pos_dict)
    #print(len(pos_dict.get_dict().keys()))
    #pos_dict.save()

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

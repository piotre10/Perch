import timeit
from time import sleep
import keyboard

from perch.player import Player
from position.position import Position
from position.display import DispWindow
from utils.posdict import PosDict
from utils.posdb import PosDB


def play_game(player1: Player(), player2: Player()):
    pos = Position()
    players = (player1, player2)
    moves = []
    while pos.is_end() == -1:
        mv = players[pos.whos_move].choose_move(pos)
        pos.move(mv)
        moves.append(mv)

    return moves, pos.is_end()


def display_game(move_list: list):
    WIN = DispWindow()
    pos = Position()
    WIN.open()
    WIN.update(pos)
    sleep(0.5)
    for mv in move_list:
        pos.move(mv)
        WIN.update(pos)
        sleep(0.5)


def add_games(player1: Player, player2: Player, pos_db: PosDict or PosDB, num_games=10000):
    for i in range(num_games):
        moves, who_won = play_game(player1, player2)
        pos_db.add_game(moves, who_won)


def keep_adding_games(player1: Player, player2: Player, pos_dict: PosDict, key='q'):
    print(f"Started loop press {key} to exit")
    while True:
        if keyboard.is_pressed(key):
            break
        moves, who_won = play_game(player1, player2)
        pos_dict.add_game(moves, who_won)






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
        print(pos)
        print(pos.valid_moves())
        mv = players[pos.whos_move].choose_move(pos)
        pos.move(mv)
        moves.append(mv)

    return moves, pos.is_end()


def display_game(move_list: list, sleep_time=0.5):
    WIN = DispWindow()
    pos = Position()
    WIN.open()
    WIN.update(pos)
    sleep(sleep_time)
    for mv in move_list:
        if WIN.quit_event():
            WIN.close()
            break
        pos.move(mv)
        WIN.update(pos)
        sleep(sleep_time)

def display_position(pos: Position):
    WIN = DispWindow()
    WIN.open()
    WIN.update(pos)
    while True:
        if WIN.quit_event():
            WIN.close()
            break


def add_games(player1: Player, player2: Player, pos_db: PosDict or PosDB, num_games=10000):
    new_rows = 0
    for i in range(num_games):
        moves, who_won = play_game(player1, player2)
        new_rows += pos_db.add_game(moves, who_won)
    return new_rows


def keep_adding_games(player1: Player, player2: Player, pos_db: PosDict or PosDB, key='q'):
    print(f"Started loop press {key} to exit")
    added_games = 0
    new_rows = 0
    start_time = timeit.default_timer()
    while True:
        if keyboard.is_pressed(key):
            break
        moves, who_won = play_game(player1, player2)
        new_rows += pos_db.add_game(moves, who_won)
        added_games += 1
    end_time = timeit.default_timer()
    print(f"Adding games ended, added games: {added_games}, time: {end_time - start_time}, new rows: {new_rows}")
    return new_rows







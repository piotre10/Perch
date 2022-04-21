import time
import timeit
from time import sleep
import keyboard

from perch.player import Player
from perch.human import HumanPlayer
from position.position import Position
from position.display import DispWindow
from utils.posdict import PosDict
from utils.posdb import PosDB


def fast_game(player1: Player(), player2: Player()):
    pos = Position()
    players = (player1, player2)
    moves = []
    while pos.is_end() == -1:
        mv = players[pos.whos_move].choose_move(pos)
        pos.move(mv)
        moves.append(mv)
    return moves, pos.is_end()


def play_game(player1: Player(), player2: Player(), with_window=0, sleep_time=0):
    WIN = None
    pos = Position()
    players = (player1, player2)
    if isinstance(player1, HumanPlayer) or isinstance(player2, HumanPlayer):
        with_window = 1
    if with_window:
        WIN = DispWindow()
        WIN.open()

    moves = []
    while pos.is_end() == -1:
        if WIN:
            WIN.update(pos)
        time.sleep(sleep_time)
        mv = players[pos.whos_move].choose_move(pos, WIN)
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
    for i in range(num_games):
        moves, who_won = fast_game(player1, player2)
        pos_db.add_game(moves, who_won)


def keep_adding_games(player1: Player, player2: Player, pos_db: PosDict or PosDB, key='q'):
    print(f"Started loop press {key} to exit")
    start_rows = pos_db.get_num_records()
    added_games = 0
    start_time = timeit.default_timer()
    while True:
        if keyboard.is_pressed(key):
            break
        moves, who_won = fast_game(player1, player2)
        pos_db.add_game(moves, who_won)
        added_games += 1
    end_time = timeit.default_timer()
    end_rows = pos_db.get_num_records()
    print(f"Adding games ended, added games: {added_games}, time: {end_time - start_time}, new rows: {end_rows - start_rows}")


def games_with_statistics(player1: Player(), player2: Player(), num_games=100000):
    results = [0, 0, 0]  # [draws, black_wins, white wins]
    games = num_games//2
    for i in range(games):
        moves, who_won = fast_game(player1, player2)
        results[who_won] += 1

    print(f'''{player1.name} as black:
           games played: {games}
           wins: {results[1]}   ({100*results[1]/games} %)
           loses: {results[2]}  ({100*results[2]/games} %)
           draws: {results[0]}  ({100*results[0]/games} %)''')

    results = [0, 0, 0]
    for i in range(games):
        moves, who_won = fast_game(player1, player2)
        results[who_won] += 1

    print(f'''{player1.name} as white:
               games played: {games}
               wins: {results[2]}   ({100 * results[2] / games} %)
               loses: {results[1]}  ({100 * results[1] / games} %)
               draws: {results[0]}  ({100 * results[0] / games} %)''')

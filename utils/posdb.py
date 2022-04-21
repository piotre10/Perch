
import sqlite3
import timeit

from position.position import Position
from utils.convert import pos_biased_tup_to_byte_arr


class PosDB:

    def __init__(self, name="TestDatabase"):
        self.name = name
        self.con = None
        self.cur = None
        self.next_record = 0

    def create_connection(self):
        self.con = sqlite3.connect(f"databases/{self.name}.db")

    def create_pos_table(self):
        self.cur.execute(""" CREATE TABLE IF NOT EXISTS pos_table (
                            pos BLOB PRIMARY KEY ,
                            result INTEGER NOT NULL,
                            num_games INTEGER NOT NULL,
                            eval REAL NOT NULL ) WITHOUT ROWID;""")

    def add_game(self, move_list, who_won):
        who_won = who_won * 2 - 3
        pos = Position()
        for mv in move_list:
            pos.move(mv)
            pos_arr = pos_biased_tup_to_byte_arr(pos.get_as_biased_tuple())

            tuple_to_insert = (pos_arr, who_won)
            self.cur.execute('''INSERT INTO pos_table(pos, result, num_games, eval) 
                                VALUES (?1, ?2, 1, ?2)
                                ON CONFLICT(pos) DO UPDATE 
                                SET result=result+?2,
                                num_games = num_games + 1,
                                eval = result/CAST(num_games AS REAL);''', tuple_to_insert)

    def get_average_num_games(self):
        self.cur.execute("SELECT SUM(num_games)/CAST(COUNT(*) as REAL) FROM pos_table;")
        row = self.cur.fetchone()
        return row[0]

    def get_num_records(self):
        self.cur.execute("SELECT COUNT(*) FROM pos_table;")
        row = self.cur.fetchone()
        return row[0]

    def get_num_single_games(self):
        self.cur.execute("SELECT COUNT(*) FROM pos_table WHERE num_games==1;")
        row = self.cur.fetchone()
        return row[0]

    def exec_select_query(self, query, args=None):
        if args:
            self.cur.execute(query, args)
        else:
            self.cur.execute(query)
        return self.cur.fetchall()

    def init_cursor(self):
        self.cur = self.con.cursor()

    def is_connected(self):
        return self.con

    def close_connection(self):
        if self.con:
            self.con.close()
        else:
            print("con is None")

    def commit(self):
        self.con.commit()

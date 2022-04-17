
import sqlite3
import timeit

from position.position import Position
from utils.convert import pos_vec_turn_normal_to_bias


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
                            pos TEXT PRIMARY KEY ,
                            result INTEGER NOT NULL,
                            num_games INTEGER NOT NULL,
                            eval REAL NOT NULL );""")

    def add_game(self, move_list, who_won):
        who_won = who_won * 2 - 3

        pos = Position()
        for mv in move_list:
            pos.move(mv)
            temp = str(tuple(pos_vec_turn_normal_to_bias(pos.get_as_vector())))
            self.cur.execute("SELECT rowid FROM pos_table WHERE pos=?;",(temp,))
            row = self.cur.fetchone()
            if row is None:
                tuple_to_insert = (temp, who_won, 1, who_won)
                t4 = timeit.default_timer()
                self.cur.execute("INSERT INTO pos_table VALUES (?, ?, ?, ?);", tuple_to_insert)
                t5 = timeit.default_timer()
                print(f"{t5-t4} (insert)")
            else:
                t4 = timeit.default_timer()
                self.cur.execute("""UPDATE pos_table 
                                    SET result=result+(?),
                                    num_games = num_games+1,
                                    eval = result/CAST(num_games AS REAL)
                                    WHERE pos LIKE ?;""", (who_won, temp))
                t5 = timeit.default_timer()
                print(f"{t5 - t4} (update)")

    def get_average_num_games(self):
        self.cur.execute("SELECT SUM(num_games)/CAST(COUNT(*) as REAL) FROM pos_table;")
        row = self.cur.fetchone()
        return row[0]

    def get_num_records(self):
        self.cur.execute("SELECT COUNT(*) FROM pos_table;")
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

import csv
from sqlite3 import connect


class DBSetup():
    def __init__(self):
        self.dbpath = './db/game.db'
        # import and create our player database
        self.gamedb = connect(self.dbpath)
        self.conn = self.gamedb.cursor()

    def setupdb(self):
        # If you set this to 1, it will print out all data as it populates the datbase.
        # make a database connection to the game database
        conn = connect('./db/game.db')
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS levels(level INTEGER, hp INTEGER, mp INTEGER, attack INTEGER, defense INTEGER, req_xp INTEGER)")

        # insert our levelnotes table in the database
        with open('./csv/levelnotes.csv', 'r') as fin:
            data_reader = csv.reader(fin)
            for i in data_reader:
                cur.execute('INSERT INTO levels VALUES (?,?,?,?,?,?);', i)

        conn.commit()
        # close the database connection to let other operations use it
        conn.close()

    def new_actor(self):
        query = self.conn.execute('SELECT * FROM levels WHERE level = 1;')
        return query.fetchall()[0]

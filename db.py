import sqlite3

class Database():
    def __init__(self, file):
        self.con = self.connect_db(file)
        self.db = self.con.cursor()
        return
    
    def retrieve(self, website, column, rating, delta):
        lowerbound = rating - delta
        upperbound = rating + delta
        res = self.db.execute('SELECT url FROM problems WHERE website="{website}" and chosen="None" and {column} >= {lowerbound} and {column} >= {lowerbound}')
        res = fetchall()
        print(res)
        return res
    
    def create_table(self):
        self.db.execute('CREATE TABLE "problems" (
            "name"	TEXT,
            "url"	TEXT NOT NULL,
            "id"	INTEGER,
            "website"	TEXT,
            "contest"	TEXT,
            "index"	TEXT,
            "diff"	NUMERIC,
            "rating"	NUMERIC,
            PRIMARY KEY("id" AUTOINCREMENT)
        )')
        return
        
class Kattis(Database):
    def __init__(self, file):
        super().__init__(file)
        return
    
    def insert(data):
        self.db.executemany("INSERT INTO problems (name, url, website, diff) VALUES(?, ?, ?, ?)",
                            data)
        self.con.commit()
        return
    
    def retrieve_all(diff=0, delta=10):
        return self.retrieve("kattis", "diff", diff, delta)
    
class Codeforces(Database):
    def __init__(self, file):
        super().__init__(file)
        return
    
    def insert(data):
        self.db.executemany("INSERT INTO problems (name, url, website, contest, index, rating) VALUES(?, ?, ?, ?, ?, ?)",
                            data)
        self.con.commit()
        return
    
    def retrieve_all(rating=0, delta=4000):
        return self.retrieve("codeforces", "rating", rating, delta)

    

    
    
    



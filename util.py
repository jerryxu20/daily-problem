import math
import random
import requests
import sqlite3
from datetime import date

class Database():
    def __init__(self, file):
        self.con = self.connect_db(file)
        self.db = self.con.cursor()
        return
    
    def connect_db(self, file):
        con = sqlite3.connect(file)
        return con

    def retrieve(self, website, column, rating, delta):
        lowerbound = rating - delta
        upperbound = rating + delta
        res = self.db.execute(f'''SELECT url FROM problems WHERE 
                website=? and
                date_used IS NULL and
                {column} >= ? and
                {column} <= ?
        ''', (website, lowerbound, upperbound))
        res = res.fetchall()
        return res
    
    def create_table(self):
        self.db.execute('''CREATE TABLE "problems" (
            "name"	TEXT,
            "url"	TEXT NOT NULL UNIQUE,
            "id"	INTEGER,
            "website"	TEXT,
            "contest"	TEXT,
            "letter"	TEXT,
            "diff"	NUMERIC,
            "rating"	NUMERIC,
            "date_used" TEXT,
            PRIMARY KEY("id" AUTOINCREMENT)
        )''')
        
        self.db.execute('''CREATE TABLE "codeforces" (
            "url"   TEXT NOT NULL UNIQUE,
            "tags" TEXT,
            PRIMARY KEY("url")
        )''')

        return

    def update(self, url):
        d = str(date.today())
        self.db.execute('''UPDATE problems SET date_used=? WHERE url=?  ''', (d, url))
        self.con.commit()

    def close_connection(self):
        self.con.commit()
        self.con.close()
        return

class Kattis(Database):
    def __init__(self, file):
        super().__init__(file)
        return
    
    def insert(self, data):
        self.db.executemany("INSERT OR IGNORE INTO problems (name, url, website, diff) VALUES(?, ?, ?, ?)",
                            data)
        self.con.commit()
        return
    
    def retrieve_all(self, diff=0, delta=10):
        return self.retrieve("kattis", "diff", diff, delta)
    
class Codeforces(Database):
    def __init__(self, file):
        super().__init__(file)
        return
    
    def insert(self, data, tag_data):
        self.db.executemany('''INSERT OR IGNORE INTO problems (
            name, 
            url, 
            website, 
            contest,
            letter,
            rating
        ) VALUES(?, ?, ?, ?, ?, ?)''', data)

        # Values (url, tags)
        self.db.executemany('''INSERT OR IGNORE INTO codeforces 
                            VALUES(?, ?)''', tag_data)
        self.con.commit()
        return
    
    def retrieve_all(self, rating=0, delta=4000):
        return self.retrieve("codeforces", "rating", rating, delta)


def get(url):
    res = requests.get(url)
    res.raise_for_status()
    return res.content

def rand(a, b):
    # Random int in the range [a, b)
    random.seed()
    return math.floor(random.random() * (b - a)) + a

def rand_prob(site, diff=0, delta=10000):
    db = Database('problems.db')
    if site.lower() == "kattis":
        col = "diff"
    if site.lower() in ['cf', "codeforces", "codeforce"]:
        col = "rating"
    res = db.retrieve(site, col, diff, delta)
    i = rand(0, len(res))
    db.update(res[i][0])
    db.close_connection()
    return res[i][0]
    
    

if __name__ == "__main__":
    db = Database('problems.db')
    db.close_connection()



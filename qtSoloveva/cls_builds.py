import sqlite3

class Builds:
    def __init__(self):
        self.con = sqlite3.connect("Builds_Soloveva.db")
        self.cur = self.con.cursor()
        self.cur.execute(
            '''CREATE TABLE IF NOT EXISTS Builds
            (id_build INTEGER PRIMARY KEY UNIQUE NOT NULL,
            Type_Build TEXT)''')
        self.con.commit()

    def __del__(self):
        self.con.close()

    def view(self):
        self.cur.execute("SELECT * FROM Builds")
        return self.cur.fetchall()

    def insert(self, Type_Build):
        self.cur.execute("INSERT INTO Builds VALUES (NULL, ?)", (Type_Build,))
        self.con.commit()

    def search(self, Type_Build):
        self.cur.execute("SELECT * FROM Builds WHERE Type_Build=?", (Type_Build,))
        return self.cur.fetchall()
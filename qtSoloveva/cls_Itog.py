import sqlite3

class Itog:
    def __init__(self):
        self.con = sqlite3.connect("Builds_Soloveva.db")
        self.cur = self.con.cursor()
        self.cur.execute(
            """CREATE TABLE IF NOT EXISTS Itog (
                id INTEGER PRIMARY KEY UNIQUE NOT NULL,
                Build INTEGER NOT NULL,
                Count_Rooms INTEGER NOT NULL,
                Footage REAL NOT NULL,
                Price REAL NOT NULL,
                FOREIGN KEY (Build) REFERENCES Builds(id_build)
            )"""
        )
        self.con.commit()

    def __del__(self):
        self.con.close()

    def view(self):
        self.cur.execute("SELECT * FROM Itog")
        return self.cur.fetchall()

    def view_with_type(self):
        self.cur.execute("""
            SELECT Itog.id, Builds.Type_Build, Itog.Count_Rooms, Itog.Footage, Itog.Price
            FROM Itog
            JOIN Builds ON Itog.Build = Builds.id_build
        """)
        return self.cur.fetchall()

    def insert(self, build_id, count_rooms, footage, price):
        self.cur.execute(
            "INSERT INTO Itog (Build, Count_Rooms, Footage, Price) VALUES (?, ?, ?, ?)",
            (build_id, count_rooms, footage, price))
        self.con.commit()

    def search_by_type(self, type_build):
        self.cur.execute("""
            SELECT Itog.id, Builds.Type_Build, Itog.Count_Rooms, Itog.Footage, Itog.Price
            FROM Itog
            JOIN Builds ON Itog.Build = Builds.id_build
            WHERE Builds.Type_Build = ?
        """, (type_build,))
        return self.cur.fetchall()
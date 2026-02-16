import sqlite3

def create_database():
    conn= sqlite3.connect("./projekts/datubaze.db")
    conn.execute("""CREATE TABLE IF NOT EXISTS lietotaji(
                 id INTEGER PRIMARY KEY,
                 genre TEXT,
                 show TEXT)""")
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()
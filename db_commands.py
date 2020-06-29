import os
import sqlite3
from sqlite3 import Error

db_file = os.getcwd() + "/myData.db"

def create_table_temperatures():
    conn = create_connection(db_file)
    cur = conn.cursor()
    sql_command = """
    DROP TABLE IF EXISTS temperatures;
    CREATE TABLE temperatures (
    id INTEGER,
    temperature REAL,
    humidity TINYINT,
    battery REAL,
    date INTEGER(4) DEFAULT (strftime('%s', 'now')),
    device VARCHAR(5),
    PRIMARY KEY (id));
    """
    cur.executescript(sql_command)
    conn = close_connection(conn)
        

def create_connection(db):
    conn = None
    try:
        conn = sqlite3.connect(db)
    except Error as e:
        print(e)

    return conn

def close_connection(conn):
    conn.commit()
    conn.close()


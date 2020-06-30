import os
import sqlite3
from sqlite3 import Error

db_file = os.getcwd() + "/myData.db"

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

def insert_temperature(data):
    conn = create_connection(db_file)
    cur = conn.cursor()
    cur.execute('INSERT INTO temperatures (temperature, humidity, battery, device) VALUES (?, ?, ?, ?)', data)
    close_connection(conn)

def select_last_temperature():
    conn = create_connection(db_file)
    cur = conn.cursor()
    sql_command = """
    select id
    ,temperature
    ,humidity
    ,datetime(date, 'unixepoch', 'localtime') as localtime
    ,device
    ,battery
    from temperatures
    order by id
    DESC LIMIT 1
    ;
    """
    cur.execute(sql_command)
    data = cur.fetchone()
    close_connection(conn)
    return data
        




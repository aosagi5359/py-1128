import sqlite3
 
CREATE_BEANS_TABLE = """
CREATE TABLE IF NOT EXISTS beans (
    id INTEGER PRIMARY KEY,
    name TEXT,
    method TEXT,
    rating INTEGER
);"""
 
INSERT_BEAN = "INSERT INTO beans (name, method, rating) VALUES (?, ?, ?);"
GET_ALL_BEANS = "SELECT * FROM beans;"
GET_BEANS_BY_NAME = "SELECT * FROM beans WHERE name = ?;"
GET_BEST_PREPARATION_FOR_BEAN = """
SELECT * FROM beans
WHERE name = ?
ORDER BY rating DESC
LIMIT 1;
"""
 #連接資料庫
def connect():
    return sqlite3.connect("data.db")
 #建立資料表
def create_tables(connection):
    with connection:
        connection.execute(CREATE_BEANS_TABLE)
 #在beans資料表中加入資料
def add_bean(connection, name, method, rating):
    with connection:
        connection.execute(INSERT_BEAN, (name, method, rating))
 #取得beans資料表中所有資料
def get_all_beans(connection):
    with connection:
        return connection.execute(GET_ALL_BEANS).fetchall()
 #透過name欄位尋找beans資料中的資料
def get_beans_by_name(connection, name):
    with connection:
        return connection.execute(GET_BEANS_BY_NAME, (name,)).fetchall()
 #透過name欄位尋找beans資料中的資料，並用rating欄位取的最高的評分
def get_best_preparation_for_bean(connection, name):
    with connection:
        return connection.execute(GET_BEST_PREPARATION_FOR_BEAN, (name,)).fetchall()

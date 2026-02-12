import os
import psycopg2
from psycopg2 import pool

connection_pool = pool.SimpleConnectionPool(
    1,
    10,
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)

def get_db():
    return connection_pool.getconn()

def put_db(conn):
    connection_pool.putconn(conn)
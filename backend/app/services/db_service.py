import psycopg2
import os

def get_db_connection():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST", "db"),
        database=os.getenv("DB_NAME", "asm_database"),
        user=os.getenv("DB_USER", "asm_user"),
        password=os.getenv("DB_PASSWORD", "asm_password")
    )
    return conn
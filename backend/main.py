from flask import Flask
from app.api.admin_routes import admin_bp
import psycopg2
import os

app = Flask(__name__)
app.register_blueprint(admin_bp)

def get_db_connection():
    conn = psycopg2.connect(
        host="db",
        database="asm_database",
        user="asm_user",
        password="asm_password"
    )
    return conn

@app.route("/db-test")
def db_test():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT 1;")
    result = cur.fetchone()
    cur.close()
    conn.close()
    return {"db_response": result[0]}

@app.route("/health")
def health():
    return {"status": "ASM backend running"}, 200

if __name__=="__main__":
    app.run(host="0.0.0.0", port=5000)

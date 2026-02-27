from flask import Flask , request , redirect
from app.services.db_service import get_db_connection
from app.api.user_routes import user_bp
from routes.asset_routes import asset_bp
from app.api.discovery_routes import discovery_bp
from app.services.scheduler_service import start_scheduler
from routes.dashboard_routes import dashboard_bp
import psycopg2
import os

app = Flask(__name__)
print("Starting scheduler...........")
start_scheduler()
app.register_blueprint(user_bp, url_prefix="/api")
app.register_blueprint(asset_bp, url_prefix="/api")
app.register_blueprint(discovery_bp, url_prefix="/api")
app.register_blueprint(dashboard_bp)

@app.route("/")
def health():
    return {"status": "ASM backend running"}, 200

@app.route("/db-test")
def db_test():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT 1;")
    result = cur.fetchone()
    cur.close()
    conn.close()
    return {"db_response": result[0]}
 

if __name__=="__main__":
    app.run(host="0.0.0.0", port=5000)
    


    admiral@admiral-vivo:~$ curl -X POST http://localhost:5000/api/login -H "Content-Type: application/json" -d '{"email":"YOUR_EMAIL","password":"YOUR_PASSWORD"}'
{"message":"Invalid credentials"}

asm-backend   | 172.18.0.1 - - [27/Feb/2026 19:31:18] "POST /api/login HTTP/1.1" 401 -

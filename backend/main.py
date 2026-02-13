from flask import Flask
from app.services.db_service import get_db_connection
from app.api.user_routes import user_bp
import psycopg2
import os

app = Flask(__name__)
app.register_blueprint(user_bp)

@app.route("/health")
def health():
    return {"status": "ASM backend running"}, 200

if __name__=="__main__":
    app.run(host="0.0.0.0", port=5000)

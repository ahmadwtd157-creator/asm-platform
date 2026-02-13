from app.services.db_service import get_db_connection

@app.route("/db-test")
def db_test():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT 1;")
    result = cur.fetchone()
    cur.close()
    conn.close()
    return {"db_response": result[0]}
    
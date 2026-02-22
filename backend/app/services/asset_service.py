from app.services.db_service import get_db_connection

def create_asset(user_id, domin, ip_address):
    conn = get_db_connection
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO assets (user_id, domain, ip_address)
        VALUES (%s, %s, %s)
        RETURNING id;
        """
    ,
    (user_id,domin,ip_address)
    )
asset_id = cur.fetchone()[0]
conn.commit()
cur.close()
conn.close()
return asset_id

import socket

from app.engines.discovery_engine import run_subfinder
from app.services.db_service import get_db_connection


def discover_subdomains(asset_id):

    conn = get_db_connection()
    cur = conn.cursor()

    # get root domain + user
    cur.execute("""
        SELECT domain, user_id
        FROM assets
        WHERE id=%s
    """, (asset_id,))

    row = cur.fetchone()

    if not row:
        cur.close()
        conn.close()
        return {"discovered": 0}

    domain = row[0]
    user_id = row[1]

    # run passive discovery
    subdomains = run_subfinder(domain)

    discovered = 0

    for sub in subdomains:

        try:
            ip = socket.gethostbyname(sub)
        except Exception:
            ip = None

        cur.execute("""
            INSERT INTO assets (domain, ip_address, user_id)
            SELECT %s,%s,%s
            WHERE NOT EXISTS (
                SELECT 1 FROM assets WHERE domain=%s
            )
        """, (sub, ip, user_id, sub))

        if cur.rowcount > 0:
            discovered += 1

    conn.commit()

    cur.close()
    conn.close()

    return {"discovered": discovered}
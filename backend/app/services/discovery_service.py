from app.services.db_service import get_db_connection
from app.engines.discovery_engine import run_subfinder

def discover_subdomains(asset_id, domain):
    subdomains = run_subfinder(domain)
    conn = get_db_connection()
    cur = conn.cursor

    inserted = []

    for sub in subdomains:
        try:
            cur.execute(
                """
                INSERT INTO subdomains (asset_id, subdomain)
                VALUES (%s, %s)
                ON CONFLICT DO NOTHING
                RETURNING id;
                """,
                (asset_id, sub)
            )

            result = cur.fetchone()
            if result:
                inserted.append(sub)

        except Exception:
            continue
    conn.commit()
    cur.close()
    conn.close()

    return inserted
    
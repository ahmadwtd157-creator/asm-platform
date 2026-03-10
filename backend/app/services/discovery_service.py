from app.services.db_service import get_db_connection
from app.engines.discovery_engine import run_subfinder

def discover_subdomains(asset_id: int, domain: str):

    subdomains = run_subfinder(domain)

    conn = get_db_connection()
    cur = conn.cursor()

    inserted = []

    # احضار user صاحب الـ asset
    cur.execute(
        "SELECT user_id FROM assets WHERE id=%s",
        (asset_id,)
    )

    owner = cur.fetchone()

    if not owner:
        cur.close()
        conn.close()
        return []

    user_id = owner[0]

    for sub in subdomains:

        try:

            # حفظ في جدول subdomains
            cur.execute(
                """
                INSERT INTO subdomains (asset_id, subdomain)
                VALUES (%s,%s)
                ON CONFLICT (asset_id, subdomain) DO NOTHING
                RETURNING id
                """,
                (asset_id, sub)
            )

            result = cur.fetchone()

            if result:
                inserted.append(sub)

                # تحويله الى asset جديد
                cur.execute(
                    """
                    INSERT INTO assets (user_id, domain)
                    VALUES (%s,%s)
                    ON CONFLICT DO NOTHING
                    """,
                    (user_id, sub)
                )

        except Exception:
            continue

    conn.commit()

    cur.close()
    conn.close()

    return inserted


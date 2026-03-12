import socket
from app.engines.discovery_engine import run_subfinder
from app.services.db_service import get_db_connection


def discover_subdomains(asset_id):

    conn = get_db_connection()
    cur = conn.cursor()

    try:

        # الحصول على الدومين
        cur.execute("""
        SELECT domain, user_id
        FROM assets
        WHERE id=%s
        """, (asset_id,))

        row = cur.fetchone()

        if not row:
            return {"discovered": 0}

        domain = row[0]
        user_id = row[1]

        if not domain:
            return {"discovered": 0}

        # تشغيل subfinder
        try:
            subdomains = run_subfinder(domain)
        except Exception as e:
            print("Subfinder error:", e, flush=True)
            return {"discovered": 0}

        if not subdomains:
            return {"discovered": 0}

        discovered = 0

        for sub in subdomains:

            sub = sub.strip().lower()

            if sub.startswith("*."):
                sub = sub.replace("*.", "")

            # DNS resolve
            try:
                ip = socket.gethostbyname(sub)
            except Exception:
                continue

            # إدخال الأصل إذا غير موجود
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

        return {"discovered": discovered}

    except Exception as e:

        print("Discovery service error:", e, flush=True)
        return {"discovered": 0}

    finally:

        cur.close()
        conn.close()
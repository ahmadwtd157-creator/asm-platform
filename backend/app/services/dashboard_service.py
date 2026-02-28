#AI
from app.services.db_service import get_db_connection


class DashboardService:

    @staticmethod
    def get_summary():
        conn = get_db_connection()
        cur = conn.cursor()

        # Total Assets
        cur.execute("SELECT COUNT(*) FROM assets;")
        total_assets = cur.fetchone()[0]

        # Latest Risk Per Asset
        cur.execute("""
        SELECT a.id,
               a.domain,
               COALESCE(s.risk_score, 0)
        FROM assets a
        LEFT JOIN LATERAL (
            SELECT risk_score
            FROM scans
            WHERE asset_id = a.id
            ORDER BY created_at DESC
            LIMIT 1
        ) s ON true;
        """)

        rows = cur.fetchall()

        low = medium = high = 0

        for _, _, risk in rows:
            if risk < 30:
                low += 1
            elif risk < 70:
                medium += 1
            else:
                high += 1

        cur.close()
        conn.close()

        return {
            "total_assets": total_assets,
            "low_risk": low,
            "medium_risk": medium,
            "high_risk": high
        }
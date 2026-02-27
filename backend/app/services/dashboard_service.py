#AI
from app.services.db_service import get_db_connection


class DashboardService:

    @staticmethod
    def get_summary():
        connection = get_db_connection()
        cursor = connection.cursor()

        # 1) Total Assets
        cursor.execute("SELECT COUNT(*) FROM assets;")
        total_assets = cursor.fetchone()[0]

        # 2) Latest risk per asset
        cursor.execute("""
            SELECT a.id, COALESCE(s.risk_score, 0) AS risk_score
            FROM assets a
            LEFT JOIN LATERAL (
                SELECT risk_score
                FROM scans
                WHERE asset_id = a.id
                ORDER BY created_at DESC
                LIMIT 1
            ) s ON TRUE;
        """)

        rows = cursor.fetchall()

        low = medium = high = 0

        for _, risk in rows:
            if risk < 30:
                low += 1
            elif risk < 70:
                medium += 1
            else:
                high += 1

        cursor.close()
        connection.close()

        return {
            "total_assets": total_assets,
            "low": low,
            "medium": medium,
            "high": high
        }
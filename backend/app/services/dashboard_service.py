from app.services.db_service import get_db_connection


class DashboardService:

    @staticmethod
    def get_summary(user_id):

        conn = get_db_connection()
        cur = conn.cursor()

        # -----------------------------
        # Total Assets for this user
        # -----------------------------
        cur.execute("""
            SELECT COUNT(*)
            FROM assets
            WHERE user_id=%s
        """, (user_id,))

        total_assets = cur.fetchone()[0]

        # -----------------------------
        # Latest Risk Score per Asset
        # -----------------------------
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
            ) s ON true
            WHERE a.user_id=%s
        """, (user_id,))

        rows = cur.fetchall()

        low = 0
        medium = 0
        high = 0

        for _, _, risk in rows:

            risk = risk or 0

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
            "low": low,
            "medium": medium,
            "high": high
        }
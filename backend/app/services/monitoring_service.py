from datetime import datetime
from app.services.port_scan_service import PortScanService
from app.services.db_service import get_db_connection
from app.services.risk_scoring_service import RiskScoringService

class MonitoringService:

    @staticmethod
    def run_daily_scan():
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT id, ip_address FROM assets")
        assets = cursor.fetchall()

        for asset_id, ip in assets:
            MonitoringService.scan_and_compare(asset_id, ip, connection)

        connection.commit()
        cursor.close()
        connection.close()
        print("==== SCHEDULER RUN ====", datetime.utcnow(), flush=True)
        
    @staticmethod
    def scan_and_compare(asset_id, ip,connection):
        cursor = connection.cursor()

        cursor.execute(
            """INSERT INTO scans (asset_id, status, created_at) 
            VALUES (%s, %s, NOW()) 
            RETURNING id;
            """,
            (asset_id, "completed")

        )
        scan_id = cursor.fetchone()[0]
#تشغيل الفحص 
        new_ports = PortScanService.scan(ip)
        
        cursor.execute("""
        SELECT port FROM scan_results
        WHERE scan_id IN (
            SELECT id FROM scans
            WHERE asset_id = %s
            ORDER BY created_at DESC
            LIMIT 1 OFFSET 1
            );
            """ , (asset_id,)
        )
        

        old_ports = {row[0] for row in  cursor.fetchall()}
        new_ports_set = {p["port"] for p in new_ports}

        new_open_ports = new_ports_set - old_ports
        closed_ports = old_ports - new_ports_set

        print(f"[Asset {ip}] New Ports:{new_open_ports}")
        print(f"[Asset {ip}] Closed Ports:{closed_ports}")

        for port_data in new_ports:
                cursor.execute("""
                INSERT INTO scan_results (
                scan_id,
                port,
                service,
                banner,
                is_open
                )
                VALUES (%s,%s,%s,%s,%s);
                """, (scan_id, port_data["port"],port_data["service"],port_data["banner"], True)
                )

        for port in closed_ports:
            cursor.execute(
                """
                INSERT INTO scan_results (
                scan_id,
                port,
                service,
                is_open
                )
                VALUES (%s,%s,%s,%s);
                """,
                (scan_id,port,"unknown",False)
            )

        risk_score = RiskScoringService.calculate(new_ports)
        cursor.execute(
            """
            UPDATE scans
            SET risk_score = %s
            WHERE id=%s;
            """,
            (risk_score,scan_id)
        )
        cursor.close()
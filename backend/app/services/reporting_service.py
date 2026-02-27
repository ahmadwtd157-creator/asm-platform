#AI
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib import fonts
from reportlab.platypus import Table
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime
from app.services.db_service import get_db_connection
import os


class ReportingService:

    @staticmethod
    def generate_executive_report(output_path="executive_report.pdf"):

        connection = get_db_connection()
        cursor = connection.cursor()

        # 1️⃣ Total Assets
        cursor.execute("SELECT COUNT(*) FROM assets;")
        total_assets = cursor.fetchone()[0]

        # 2️⃣ Latest Risk per Asset
        cursor.execute("""
            SELECT a.id, a.domain, s.risk_score
            FROM assets a
            LEFT JOIN LATERAL (
                SELECT risk_score
                FROM scans
                WHERE asset_id = a.id
                ORDER BY created_at DESC
                LIMIT 1
            ) s ON true;
        """)

        asset_risks = cursor.fetchall()

        # 3️⃣ Risk Distribution
        low = medium = high = 0

        for _, _, risk in asset_risks:
            if risk is None:
                continue
            if risk < 30:
                low += 1
            elif risk < 70:
                medium += 1
            else:
                high += 1

        # 4️⃣ Recent Exposure Changes (آخر 10 تغييرات)
        cursor.execute("""
            SELECT a.domain, sr.port, sr.is_open, s.created_at
            FROM scan_results sr
            JOIN scans s ON sr.scan_id = s.id
            JOIN assets a ON s.asset_id = a.id
            ORDER BY s.created_at DESC
            LIMIT 10;
        """)

        recent_changes = cursor.fetchall()

        cursor.close()
        connection.close()

        # 🧾 إنشاء PDF
        doc = SimpleDocTemplate(output_path)
        elements = []

        styles = getSampleStyleSheet()
        title_style = styles["Heading1"]
        normal_style = styles["Normal"]

        elements.append(Paragraph("Executive Security Report", title_style))
        elements.append(Spacer(1, 0.5 * inch))

        elements.append(Paragraph(f"Generated: {datetime.utcnow()}", normal_style))
        elements.append(Spacer(1, 0.3 * inch))

        # Summary Section
        elements.append(Paragraph("1. Asset Summary", styles["Heading2"]))
        elements.append(Spacer(1, 0.2 * inch))

        summary_data = [
            ["Total Assets", total_assets],
            ["Low Risk Assets", low],
            ["Medium Risk Assets", medium],
            ["High Risk Assets", high],
        ]

        summary_table = Table(summary_data, colWidths=[3 * inch, 2 * inch])
        summary_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("GRID", (0, 0), (-1, -1), 1, colors.grey),
        ]))

        elements.append(summary_table)
        elements.append(Spacer(1, 0.5 * inch))

        # Recent Changes Section
        elements.append(Paragraph("2. Recent Exposure Changes", styles["Heading2"]))
        elements.append(Spacer(1, 0.2 * inch))

        changes_data = [["Asset", "Port", "Status", "Date"]]

        for domain, port, is_open, created_at in recent_changes:
            status = "OPENED" if is_open else "CLOSED"
            changes_data.append([domain, str(port), status, str(created_at)])

        changes_table = Table(changes_data, colWidths=[2 * inch, 1 * inch, 1 * inch, 2 * inch])
        changes_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("GRID", (0, 0), (-1, -1), 1, colors.grey),
        ]))

        elements.append(changes_table)

        doc.build(elements)

        return output_path
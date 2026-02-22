from apscheduler.schedulers.background import BackgroundScheduler
from app.services.monitoring_service import monitoring_service

scheduler = BackgroundScheduler()

def start_scheduler():
    scheduler.add_job(
        func = MonitoringService.run_daily_scan,
        trigger="interval",
        hours=24
    )
    scheduler.start()        
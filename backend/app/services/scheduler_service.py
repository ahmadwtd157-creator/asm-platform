from apscheduler.schedulers.background import BackgroundScheduler
from app.services.monitoring_service import MonitoringService

scheduler = BackgroundScheduler()

def start_scheduler():
    scheduler.add_job(
        func = MonitoringService.run_daily_scan,
        trigger="interval",
        minutes=1
    )
    scheduler.start()        
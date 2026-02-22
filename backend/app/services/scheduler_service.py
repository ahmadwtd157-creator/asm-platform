from apscheduler.schedulers.background import BackgroundScheduler
from app.services.monitoring_service import MonitoringService
import atexit

scheduler = BackgroundScheduler()

def  scheduled_job():
     MonitoringService.run_daily_scan()

def start_scheduler():
    scheduler.add_job(
        scheduled_job,
        trigger="interval",
        seconds=60,
        id="monitoring_job",
        replace_existing=True
    )
    scheduler.start()        
    print("Scheduler started", flush=True)
    atexit.register(lambda: scheduler.shutdown())
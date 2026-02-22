from apscheduler.schedulers.background import BackgroundScheduler
from app.services.monitoring_service import MonitoringService
from datetime import datetime
import atexit

scheduler = BackgroundScheduler()

def  scheduled_job():
     print("====SCHEDULER RUN ====", datetime.utcnow(), flush=True)

def start_scheduler():
    print("Registering...", flush=True)

    scheduler.add_job(
        scheduled_job,
        trigger="interval",
        seconds=30,
        id="Test_job",
        replace_existing=True
    )
    scheduler.start()        
    print("Scheduler started", flush=True)
    atexit.register(lambda: scheduler.shutdown())
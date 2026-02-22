import os 
from app.services.scheduler_service import start_scheduler

if os.environ.get("WERKEUG_RUN_MAIN")=="true":
    start_scheduler()
    
import schedule
import time
from app.task_processor import process_tasks

def start_scheduler():
    schedule.every(5).minutes.do(process_tasks)
    print("Scheduler started. Running process_tasks every 5 minutes...")
    while True:
        schedule.run_pending()
        time.sleep(1)

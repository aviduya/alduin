import logging
import schedule
import time
from app.task_processor import process_tasks

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s'
)
logger = logging.getLogger(__name__)

def start_scheduler():
    """
    Starts the scheduler to run the `process_tasks` function every 3 minutes.
    """
    logger.info("Initializing the scheduler...")
    schedule.every(3).minutes.do(process_tasks)
    logger.info("Scheduler started. Running `process_tasks` every 3 minutes.")

    try:
        while True:
            schedule.run_pending()
            time.sleep(1)  # Sleep to avoid busy waiting
    except KeyboardInterrupt:
        logger.warning("Scheduler stopped manually (KeyboardInterrupt).")
    except Exception as e:
        logger.critical("Unexpected error in the scheduler: %s", e, exc_info=True)

if __name__ == "__main__":
    logger.info("Starting the script...")
    start_scheduler()

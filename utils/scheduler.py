import os
import time
import schedule
import threading
import datetime
from utils.logger import setup_logger

# Setup logger
logger = setup_logger("scheduler")

# Path to the scraper manager
SCRAPER_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "scrapers", "scraper_manager.py")


def run_scraper():
    """
    Executes scraper_manager.py as a subprocess.
    """
    import subprocess
    start_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"🕒 Scraper job started at {start_time}")

    try:
        result = subprocess.run(
            ["python", SCRAPER_PATH],
            capture_output=True,
            text=True,
            check=True
        )
        logger.info(f"✅ Scraper completed successfully:\n{result.stdout}")
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Scraper failed:\n{e.stderr}")
    except Exception as e:
        logger.error(f"⚠️ Unexpected error running scraper: {e}")

    end_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"✅ Job finished at {end_time}\n")


def schedule_job(interval: str = "daily", time_str: str = "02:00"):
    """
    Schedule the scraper based on a given interval.
    
    Args:
        interval (str): "hourly", "daily", "weekly"
        time_str (str): Time in 24-hour format (for daily/weekly jobs)
    """
    if interval == "hourly":
        schedule.every().hour.do(run_scraper)
        logger.info("Scheduled scraper to run hourly.")
    elif interval == "daily":
        schedule.every().day.at(time_str).do(run_scraper)
        logger.info(f"Scheduled scraper to run daily at {time_str}.")
    elif interval == "weekly":
        schedule.every().monday.at(time_str).do(run_scraper)
        logger.info(f"Scheduled scraper to run weekly at {time_str}.")
    else:
        logger.warning(f"Unknown interval '{interval}', defaulting to daily.")
        schedule.every().day.at("02:00").do(run_scraper)


def run_scheduler(interval: str = "daily", time_str: str = "02:00"):
    """
    Launches the scheduler loop in a background thread.
    """
    schedule_job(interval, time_str)
    logger.info("⏳ Scheduler started. Waiting for next run...")

    def loop():
        while True:
            schedule.run_pending()
            time.sleep(30)

    # Run in background so it doesn’t block main app
    thread = threading.Thread(target=loop, daemon=True)
    thread.start()


if __name__ == "__main__":
    # Example usage
    run_scheduler(interval="daily", time_str="01:00")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("🛑 Scheduler stopped manually.")

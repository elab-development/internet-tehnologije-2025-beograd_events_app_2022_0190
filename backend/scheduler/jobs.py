from apscheduler.schedulers.background import BackgroundScheduler
from scraping.tickets_scraper import run_scraping

scheduler = BackgroundScheduler()

def start_scheduler():
    scheduler.add_job(
        run_scraping,
        trigger="interval",
        days=1,
        id="tickets_scraping"
    )
    scheduler.start()
    print("⏰ Scheduler pokrenut (1x dnevno)")

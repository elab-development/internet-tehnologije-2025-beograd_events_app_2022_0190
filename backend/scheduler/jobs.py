from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

from scraping.tickets_scraper import run_scraping
from scraping.beogradrs_scraper import run_beograd_scraping
from scraping.narodno_pozoriste_scraper import run_narodno_scraping
scheduler = BackgroundScheduler()

from notifications.reminders import run_daily_reminders


def start_scheduler(app):
    if scheduler.running:
        return

    scheduler.add_job(
        func=lambda: run_with_context(app, run_scraping),
        trigger="interval",
        hours=1,                 
        next_run_time=datetime.now(),
        id="tickets_scraping",
        replace_existing=True
    )

    scheduler.add_job(
        func=lambda: run_with_context(app, run_beograd_scraping),
        trigger="interval",
        hours=6,                 
        next_run_time=datetime.now(),
        id="beograd_scraping",
        replace_existing=True
    )
    
    scheduler.add_job(
        func=lambda: run_with_context(app, run_narodno_scraping),
        trigger="interval",
        hours=12,                 
        next_run_time=datetime.now(),
        id="narodno_pozoriste_scraping",
        replace_existing=True
    )

    scheduler.add_job(
        func=lambda: run_with_context(app, run_daily_reminders),
        trigger="interval",
        days=1,
        next_run_time=datetime.now(),  
        id="daily_reminders",
        replace_existing=True
    )



    scheduler.start()
    print("Scheduler pokrenut")


def run_with_context(app, job_func):
    with app.app_context():
        job_func()

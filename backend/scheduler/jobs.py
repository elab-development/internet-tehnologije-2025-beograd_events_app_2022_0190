from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

from scraping.tickets_scraper import run_scraping
from scraping.beogradrs_scraper import run_beograd_scraping

scheduler = BackgroundScheduler()

def start_scheduler(app):
    if scheduler.running:
        return

    # 🔹 Tickets.rs – SVAKI 1 MINUT
    scheduler.add_job(
        func=lambda: run_with_context(app, run_scraping),
        trigger="interval",
        minutes=1,                 # ⏱️ SVAKI MINUT
        next_run_time=datetime.now(),
        id="tickets_scraping",
        replace_existing=True
    )

    # 🔹 Beograd.rs – SVAKI 1 MINUT
    scheduler.add_job(
        func=lambda: run_with_context(app, run_beograd_scraping),
        trigger="interval",
        minutes=1,                 # ⏱️ SVAKI MINUT
        next_run_time=datetime.now(),
        id="beograd_scraping",
        replace_existing=True
    )

    scheduler.start()
    print("⏰ Scheduler pokrenut (svaki 1 minut)")


def run_with_context(app, job_func):
    with app.app_context():
        job_func()

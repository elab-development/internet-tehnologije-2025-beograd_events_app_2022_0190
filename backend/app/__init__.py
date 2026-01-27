from flask import Flask
from .config import Config
from .extensions import db, migrate, jwt
from scraping.tickets_scraper import run_scraping
from scheduler.jobs import start_scheduler

from .models import (
    Korisnik,
    Dogadjaj,
    KategorijaDogadjaja,
    PrivatniDogadjaj,
    OmiljeniDogadjaj
)

from .routes import korisnik_bp, dogadjaj_bp, kategorija_bp, omiljeni_bp, privatni_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

   

    start_scheduler(app)

    return app

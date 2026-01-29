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

from flask_cors import CORS
from .routes import korisnik_bp, dogadjaj_bp, kategorija_bp, omiljeni_bp, privatni_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    app.register_blueprint(korisnik_bp)
    app.register_blueprint(dogadjaj_bp)
    app.register_blueprint(kategorija_bp)
    app.register_blueprint(omiljeni_bp)
    app.register_blueprint(privatni_bp)


   

    start_scheduler(app)

    return app

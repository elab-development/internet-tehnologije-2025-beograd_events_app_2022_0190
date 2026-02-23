from flask import Flask
from .config import Config
from .extensions import db, migrate, jwt
from scraping.tickets_scraper import run_scraping
from scheduler.jobs import start_scheduler
from flasgger import Swagger

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


    Swagger(app, template={
    "info": {
        "title": "Beograd Events API",
        "description": "API za upravljanje događajima u Beogradu",
        "version": "1.0.0"
    }
})


    app.register_blueprint(korisnik_bp)
    app.register_blueprint(dogadjaj_bp)
    app.register_blueprint(kategorija_bp)
    app.register_blueprint(omiljeni_bp)
    app.register_blueprint(privatni_bp)

    with app.app_context():
        db.create_all()
        if not KategorijaDogadjaja.query.first():
            kategorije = [
                KategorijaDogadjaja(naziv="Koncert"),
                KategorijaDogadjaja(naziv="Festival"),
                KategorijaDogadjaja(naziv="Pozorište"),
                KategorijaDogadjaja(naziv="Izložba"),
            ]

            db.session.add_all(kategorije)
            db.session.commit()

    start_scheduler(app)

    return app

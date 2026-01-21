from flask import Flask
from .config import Config
from .extensions import db, migrate, jwt

from .models import (
    Korisnik,
    Dogadjaj,
    KategorijaDogadjaja,
    PrivatniDogadjaj,
    OmiljeniDogadjaj
)

from .routes import korisnik_bp, dogadjaj_bp, kategorija_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    app.register_blueprint(korisnik_bp)
    app.register_blueprint(dogadjaj_bp)
    app.register_blueprint(kategorija_bp)


    return app

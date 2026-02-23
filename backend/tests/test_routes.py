import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from app import create_app
from app.extensions import db


@pytest.fixture
def client():
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False
    })

    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()


def test_get_dogadjaji(client):
    response = client.get("/api/dogadjaji")
    assert response.status_code == 200


def test_create_dogadjaj(client):
    response = client.post("/api/dogadjaji", json={
        "naziv": "Test Event",
        "opis": "Opis testa",
        "datum": "2026-06-15",
        "lokacija": "Beograd",
        "kategorija_dogadjaja_id": 1
    })

    assert response.status_code == 201
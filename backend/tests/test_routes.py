import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from datetime import date, timedelta
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


# 1️⃣ Test GET svi dogadjaji
def test_get_dogadjaji(client):
    response = client.get("/api/dogadjaji")
    assert response.status_code == 200


# 2️⃣ Test kreiranja dogadjaja
def test_create_dogadjaj(client):
    response = client.post("/api/dogadjaji", json={
        "naziv": "Test Event",
        "opis": "Opis testa",
        "datum": "2026-06-15",
        "lokacija": "Beograd",
        "kategorija_dogadjaja_id": 1
    })

    assert response.status_code == 201


# 3️⃣ Test da POST vraća id
def test_create_dogadjaj_returns_id(client):
    response = client.post("/api/dogadjaji", json={
        "naziv": "Event With ID",
        "opis": "Opis",
        "datum": "2026-06-15",
        "lokacija": "Beograd",
        "kategorija_dogadjaja_id": 1
    })

    data = response.get_json()

    assert response.status_code == 201
    assert "id" in data


# 4️⃣ Test da vraća samo buduće događaje
def test_returns_only_future_events(client):
    today = date.today()

    # prošli događaj
    client.post("/api/dogadjaji", json={
        "naziv": "Past Event",
        "opis": "Opis",
        "datum": str(today - timedelta(days=1)),
        "lokacija": "Beograd",
        "kategorija_dogadjaja_id": 1
    })

    # budući događaj
    client.post("/api/dogadjaji", json={
        "naziv": "Future Event",
        "opis": "Opis",
        "datum": str(today + timedelta(days=5)),
        "lokacija": "Beograd",
        "kategorija_dogadjaja_id": 1
    })

    response = client.get("/api/dogadjaji")
    data = response.get_json()

    assert len(data) == 1
    assert data[0]["naziv"] == "Future Event"
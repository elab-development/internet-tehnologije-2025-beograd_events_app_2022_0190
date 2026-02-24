from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import Dogadjaj
from datetime import date
from datetime import datetime
import requests
import os

dogadjaj_bp = Blueprint("dogadjaj", __name__, url_prefix="/api/dogadjaji")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")


def get_weather(city=None):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q=Belgrade,RS&appid={OPENWEATHER_API_KEY}&units=metric"
        response = requests.get(url, timeout=3)
        data = response.json()

        if response.status_code == 200:
            return {
                "temperatura": data["main"]["temp"],
                "vreme": data["weather"][0]["description"]
            }
        return None
    except:
        return None

import time


def get_coordinates(location):
    try:
        # 1️⃣ Ako je nevalidna lokacija — vrati centar BG
        if not location or location.lower().strip() in ["više lokacija", "vise lokacija"]:
            return {
                "lat": 44.8170058,
                "lon": 20.4610046
            }

        query = f"{location}, Belgrade"

        url = "https://nominatim.openstreetmap.org/search"
        params = {
            "q": query,
            "format": "json",
            "limit": 1
        }

        headers = {
            "User-Agent": "dogadjaji-app (student project, ni20220190@student.fon.bg.ac.rs)"
        }

        response = requests.get(url, params=params, headers=headers, timeout=5)
        #time.sleep(1)
        data = response.json()

        if response.status_code == 200 and len(data) > 0:
            return {
                "lat": float(data[0]["lat"]),
                "lon": float(data[0]["lon"])
            }

        # 2️⃣ Ako ništa ne nađe — vrati centar Beograda
        return {
            "lat": 44.8170058,
            "lon": 20.4610046
        }

    except Exception as e:
        print("GRESKA KOORDINATE:", e)
        return {
            "lat": 44.8170058,
            "lon": 20.4610046
        }


@dogadjaj_bp.route("", methods=["GET"])
def svi_dogadjaji():
    """
    Vraća sve buduće događaje
    ---
    tags:
      - Dogadjaji
    responses:
      200:
        description: Lista svih budućih događaja
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              naziv:
                type: string
              opis:
                type: string
              datum:
                type: string
              lokacija:
                type: string
              cena:
                type: number
              imageURL:
                type: string
              sourceURL:
                type: string
              kategorija_dogadjaja_id:
                type: integer
              temperatura:
                type: number
              vreme:
                type: string
              lat:
                type: string
              lon:
                type: string
    """
    danas = date.today()
    dogadjaji = Dogadjaj.query.filter(Dogadjaj.datum > danas).all()
    rezultat = []

    for d in dogadjaji:
        weather = get_weather()
        coords = get_coordinates(d.lokacija)

        rezultat.append({
            "id": d.id,
            "naziv": d.naziv,
            "opis": d.opis,
            "datum": str(d.datum),
            "lokacija": d.lokacija,
            "cena": d.cena,
            "imageURL": d.imageURL,
            "sourceURL": d.sourceURL,
            "kategorija_dogadjaja_id": d.kategorija_dogadjaja_id,
            "temperatura": weather["temperatura"] if weather else None,
            "vreme": weather["vreme"] if weather else None,
            "lat": coords["lat"] if coords else None,
            "lon": coords["lon"] if coords else None
        })

    return jsonify(rezultat)


@dogadjaj_bp.route("", methods=["POST"])
def kreiraj_dogadjaj():
    """
    Kreira novi događaj
    ---
    tags:
      - Dogadjaji
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - naziv
            - opis
            - datum
            - lokacija
            - kategorija_dogadjaja_id
          properties:
            naziv:
              type: string
            opis:
              type: string
            datum:
              type: string
              example: "2026-06-15"
            lokacija:
              type: string
            cena:
              type: number
            imageURL:
              type: string
            sourceURL:
              type: string
            kategorija_dogadjaja_id:
              type: integer
    responses:
      201:
        description: Događaj uspešno dodat
    """
    data = request.json

    d = Dogadjaj(
        naziv=data["naziv"],
        opis=data["opis"],
        datum=datetime.strptime(data["datum"], "%Y-%m-%d").date(),
        lokacija=data["lokacija"],
        cena=data.get("cena"),
        imageURL=data.get("imageURL"),
        sourceURL=data.get("sourceURL"),
        kategorija_dogadjaja_id=data["kategorija_dogadjaja_id"]
    )

    db.session.add(d)
    db.session.commit()

    return jsonify({
        "poruka": "Dogadjaj dodat",
        "id": d.id
    }), 201


@dogadjaj_bp.route("/<int:id>", methods=["GET"])
def jedan_dogadjaj(id):
    """
    Vraća jedan događaj po ID-u
    ---
    tags:
      - Dogadjaji
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Jedan događaj
        schema:
          type: object
          properties:
            id:
              type: integer
            naziv:
              type: string
            opis:
              type: string
            datum:
              type: string
            lokacija:
              type: string
            cena:
              type: number
            imageURL:
              type: string
            sourceURL:
              type: string
            kategorija_dogadjaja_id:
              type: integer
            temperatura:
              type: number
            vreme:
              type: string
            lat:
              type: string
            lon:
              type: string
      404:
        description: Događaj nije pronađen
    """
    d = Dogadjaj.query.get_or_404(id)

    weather = get_weather()
    coords = get_coordinates(d.lokacija)

    return jsonify({
        "id": d.id,
        "naziv": d.naziv,
        "opis": d.opis,
        "datum": str(d.datum),
        "lokacija": d.lokacija,
        "cena": d.cena,
        "imageURL": d.imageURL,
        "sourceURL": d.sourceURL,
        "kategorija_dogadjaja_id": d.kategorija_dogadjaja_id,
        "temperatura": weather["temperatura"] if weather else None,
        "vreme": weather["vreme"] if weather else None,
        "lat": coords["lat"] if coords else None,
        "lon": coords["lon"] if coords else None
    })
from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import Dogadjaj
from datetime import date
from datetime import datetime
import requests

dogadjaj_bp = Blueprint("dogadjaj", __name__, url_prefix="/api/dogadjaji")
import os
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

def get_weather(city=None):
    try:
        # UVEK koristimo Beograd
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


def get_coordinates(location):
    try:
        query = f"{location}, Beograd, Srbija"

        url = "https://nominatim.openstreetmap.org/search"
        params = {
            "q": query,
            "format": "json",
            "limit": 1
        }
        headers = {
            "User-Agent": "events-app"
        }

        response = requests.get(url, params=params, headers=headers, timeout=3)
        data = response.json()

        if data:
            return {
                "lat": data[0]["lat"],
                "lon": data[0]["lon"]
            }
        return None
    except:
        return None

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
      404:
        description: Događaj nije pronađen
    """
    d = Dogadjaj.query.get_or_404(id)

    return jsonify({
        "id": d.id,
        "naziv": d.naziv,
        "opis": d.opis,
        "datum": str(d.datum),
        "lokacija": d.lokacija,
        "cena": d.cena,
        "imageURL": d.imageURL,
        "sourceURL": d.sourceURL,
        "kategorija_dogadjaja_id": d.kategorija_dogadjaja_id
    })

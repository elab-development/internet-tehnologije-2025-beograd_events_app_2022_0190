from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import Dogadjaj
from datetime import date

dogadjaj_bp = Blueprint("dogadjaj", __name__, url_prefix="/api/dogadjaji")


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

    return jsonify([
        {
            "id": d.id,
            "naziv": d.naziv,
            "opis": d.opis,
            "datum": str(d.datum),
            "lokacija": d.lokacija,
            "cena": d.cena,
            "imageURL": d.imageURL,
            "sourceURL": d.sourceURL,
            "kategorija_dogadjaja_id": d.kategorija_dogadjaja_id
        } for d in dogadjaji
    ])


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
        datum=data["datum"],
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

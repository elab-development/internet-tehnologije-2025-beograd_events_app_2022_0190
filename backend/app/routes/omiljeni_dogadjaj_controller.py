from flask import Blueprint, request, jsonify
from app import db
from app.models.omiljeni_dogadjaj import OmiljeniDogadjaj
from app.models.dogadjaj import Dogadjaj
from datetime import timedelta

omiljeni_bp = Blueprint(
    "omiljeni",
    __name__,
    url_prefix="/api/omiljeni"
)


@omiljeni_bp.route("", methods=["GET"])
def svi_omiljeni():
    """
    Vraća sve omiljene događaje svih korisnika
    ---
    tags:
      - Omiljeni
    responses:
      200:
        description: Lista svih omiljenih događaja
    """
    omiljeni = OmiljeniDogadjaj.query.all()

    return jsonify([
        {
            "korisnik_id": o.korisnik_id,
            "dogadjaj_id": o.dogadjaj_id,
            "podsetnik": str(o.podsetnik) if o.podsetnik else None,
            "dogadjaj": {
                "id": o.dogadjaj.id,
                "naziv": o.dogadjaj.naziv,
                "datum": str(o.dogadjaj.datum),
                "lokacija": o.dogadjaj.lokacija,
                "cena": o.dogadjaj.cena,
                "imageURL": o.dogadjaj.imageURL
            }
        }
        for o in omiljeni
    ])


@omiljeni_bp.route("/korisnik/<int:korisnik_id>", methods=["GET"])
def omiljeni_korisnika(korisnik_id):
    """
    Vraća sve omiljene događaje određenog korisnika
    ---
    tags:
      - Omiljeni
    parameters:
      - name: korisnik_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Lista omiljenih događaja korisnika
    """
    omiljeni = OmiljeniDogadjaj.query.filter_by(
        korisnik_id=korisnik_id
    ).all()

    return jsonify([
        {
            "dogadjaj_id": o.dogadjaj_id,
            "podsetnik": str(o.podsetnik) if o.podsetnik else None,
            "dogadjaj": {
                "id": o.dogadjaj.id,
                "naziv": o.dogadjaj.naziv,
                "datum": str(o.dogadjaj.datum),
                "lokacija": o.dogadjaj.lokacija,
                "cena": o.dogadjaj.cena
            }
        }
        for o in omiljeni
    ])


@omiljeni_bp.route("/<int:korisnik_id>/<int:dogadjaj_id>", methods=["GET"])
def jedan_omiljeni(korisnik_id, dogadjaj_id):
    """
    Vraća jedan omiljeni događaj po korisniku i događaju
    ---
    tags:
      - Omiljeni
    parameters:
      - name: korisnik_id
        in: path
        type: integer
        required: true
      - name: dogadjaj_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Jedan omiljeni događaj
      404:
        description: Nije pronađen
    """
    o = OmiljeniDogadjaj.query.get_or_404(
        (korisnik_id, dogadjaj_id)
    )

    return jsonify({
        "korisnik_id": o.korisnik_id,
        "dogadjaj_id": o.dogadjaj_id,
        "podsetnik": str(o.podsetnik) if o.podsetnik else None
    })


@omiljeni_bp.route("", methods=["POST"])
def dodaj_omiljeni():
    """
    Dodaje događaj u omiljene
    ---
    tags:
      - Omiljeni
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - korisnik_id
            - dogadjaj_id
          properties:
            korisnik_id:
              type: integer
            dogadjaj_id:
              type: integer
    responses:
      201:
        description: Događaj dodat u omiljene
      400:
        description: Već postoji u omiljenima
    """
    data = request.json

    korisnik_id = data["korisnik_id"]
    dogadjaj_id = data["dogadjaj_id"]

    postoji = OmiljeniDogadjaj.query.get(
        (korisnik_id, dogadjaj_id)
    )

    if postoji:
        return jsonify(
            {"greska": "Dogadjaj je vec u omiljenim"}
        ), 400

    dogadjaj = Dogadjaj.query.get_or_404(dogadjaj_id)

    podsetnik = dogadjaj.datum - timedelta(days=1)

    novi = OmiljeniDogadjaj(
        korisnik_id=korisnik_id,
        dogadjaj_id=dogadjaj_id,
        podsetnik=podsetnik
    )

    db.session.add(novi)
    db.session.commit()

    return jsonify({
        "poruka": "Dogadjaj dodat u omiljene",
        "korisnik_id": korisnik_id,
        "dogadjaj_id": dogadjaj_id,
        "podsetnik": str(podsetnik)
    }), 201


@omiljeni_bp.route("/<int:korisnik_id>/<int:dogadjaj_id>", methods=["DELETE"])
def obrisi_omiljeni(korisnik_id, dogadjaj_id):
    """
    Briše događaj iz omiljenih
    ---
    tags:
      - Omiljeni
    parameters:
      - name: korisnik_id
        in: path
        type: integer
        required: true
      - name: dogadjaj_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Događaj uklonjen iz omiljenih
      404:
        description: Nije pronađen
    """
    o = OmiljeniDogadjaj.query.get_or_404(
        (korisnik_id, dogadjaj_id)
    )

    db.session.delete(o)
    db.session.commit()

    return jsonify({"poruka": "Dogadjaj uklonjen iz omiljenih"})

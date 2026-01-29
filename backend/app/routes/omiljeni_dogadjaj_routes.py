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
    o = OmiljeniDogadjaj.query.get_or_404(
        (korisnik_id, dogadjaj_id)
    )

    db.session.delete(o)
    db.session.commit()

    return jsonify({"poruka": "Dogadjaj uklonjen iz omiljenih"})

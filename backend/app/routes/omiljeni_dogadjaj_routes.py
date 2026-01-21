from flask import Blueprint, request, jsonify
from app import db
from app.models.omiljeni_dogadjaj import OmiljeniDogadjaj

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
            "podsetnik": o.podsetnik
        } for o in omiljeni
    ])



@omiljeni_bp.route("", methods=["POST"])
def dodaj_omiljeni():
    data = request.json

    novi = OmiljeniDogadjaj(
        korisnik_id=data["korisnik_id"],
        dogadjaj_id=data["dogadjaj_id"]
    )

    db.session.add(novi)
    db.session.commit()

    return jsonify({"poruka": "Dogadjaj dodat u omiljene"}), 201

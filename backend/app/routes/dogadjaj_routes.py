from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import Dogadjaj

dogadjaj_bp = Blueprint("dogadjaj", __name__, url_prefix="/api/dogadjaji")


@dogadjaj_bp.route("", methods=["GET"])
def svi_dogadjaji():
    dogadjaji = Dogadjaj.query.all()
    return jsonify([
        {
            "id": d.id,
            "naziv": d.naziv,
            "opis": d.opis,
            "datum": str(d.datum)
        } for d in dogadjaji
    ])


@dogadjaj_bp.route("", methods=["POST"])
def kreiraj_dogadjaj():
    data = request.json

    d = Dogadjaj(
        naziv=data["naziv"],
        opis=data["opis"],
        datum=data["datum"],
        lokacija=data["lokacija"],
        kategorija_dogadjaja_id=data["kategorija_dogadjaja_id"]
    )

    db.session.add(d)
    db.session.commit()

    return jsonify({"poruka": "Dogadjaj dodat"}), 201

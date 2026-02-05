from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import Dogadjaj

dogadjaj_bp = Blueprint("dogadjaj", __name__, url_prefix="/api/dogadjaji")

from datetime import date

@dogadjaj_bp.route("", methods=["GET"])
def svi_dogadjaji():
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

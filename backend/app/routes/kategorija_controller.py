from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import KategorijaDogadjaja

kategorija_bp = Blueprint("kategorija", __name__, url_prefix="/api/kategorije")



@kategorija_bp.route("", methods=["GET"])
def sve_kategorije():
    kategorije = KategorijaDogadjaja.query.all()
    return jsonify([
        {
            "id": k.id,
            "naziv": k.naziv
        } for k in kategorije
    ])


@kategorija_bp.route("", methods=["POST"])
def dodaj_kategoriju():
    data = request.json

    k = KategorijaDogadjaja(naziv=data["naziv"])
    db.session.add(k)
    db.session.commit()

    return jsonify({"poruka": "Kategorija dodata"}), 201

@kategorija_bp.route("/<int:id>", methods=["GET"])
def jedna_kategorija(id):
    kategorija = KategorijaDogadjaja.query.get_or_404(id)

    return jsonify({
        "id": kategorija.id,
        "naziv": kategorija.naziv
    })

from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.privatni_dogadjaj import PrivatniDogadjaj

privatni_bp = Blueprint(
    "privatni",
    __name__,
    url_prefix="/api/privatni-dogadjaji"
)

@privatni_bp.route("", methods=["POST"])
def kreiraj_privatni():
    data = request.json

    novi = PrivatniDogadjaj(
        naziv=data["naziv"],
        opis=data["opis"],
        datum=data["datum"],
        lokacija=data["lokacija"],
        kapacitet=data["kapacitet"],
        korisnik_id=data["korisnik_id"]
    )

    db.session.add(novi)
    db.session.commit()

    return jsonify({
        "poruka": "Privatni događaj uspešno kreiran",
        "id": novi.id
    }), 201

@privatni_bp.route("", methods=["GET"])
def svi_privatni():
    privatni = PrivatniDogadjaj.query.all()

    return jsonify([
        {
            "id": p.id,
            "naziv": p.naziv,
            "opis": p.opis,
            "datum": str(p.datum),
            "lokacija": p.lokacija,
            "kapacitet": p.kapacitet,
            "korisnik_id": p.korisnik_id
        } for p in privatni
    ])

@privatni_bp.route("/<int:id>", methods=["GET"])
def jedan_privatni(id):
    p = PrivatniDogadjaj.query.get_or_404(id)

    return jsonify({
        "id": p.id,
        "naziv": p.naziv,
        "opis": p.opis,
        "datum": str(p.datum),
        "lokacija": p.lokacija,
        "kapacitet": p.kapacitet,
        "korisnik_id": p.korisnik_id
    })
@privatni_bp.route("/korisnik/<int:korisnik_id>", methods=["GET"])
def privatni_po_korisniku(korisnik_id):
    privatni = PrivatniDogadjaj.query.filter_by(
        korisnik_id=korisnik_id
    ).all()

    return jsonify([
        {
            "id": p.id,
            "naziv": p.naziv,
            "opis": p.opis,
            "datum": str(p.datum),
            "lokacija": p.lokacija,
            "kapacitet": p.kapacitet,
            "korisnik_id": p.korisnik_id
        } for p in privatni
    ])

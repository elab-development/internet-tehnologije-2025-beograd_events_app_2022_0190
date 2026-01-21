from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import Korisnik

korisnik_bp = Blueprint("korisnik", __name__, url_prefix="/api/korisnici")


@korisnik_bp.route("", methods=["GET"])
def svi_korisnici():
    korisnici = Korisnik.query.all()
    return jsonify([
        {
            "id": k.id,
            "ime": k.ime,
            "email": k.email
        } for k in korisnici
    ])


@korisnik_bp.route("", methods=["POST"])
def kreiraj_korisnika():
    data = request.json

    novi = Korisnik(
        ime=data["ime"],
        prezime=data["prezime"],
        email=data["email"],
        lozinka=data["lozinka"],
        uloga=data.get("uloga", "KORISNIK")
    )

    db.session.add(novi)
    db.session.commit()

    return jsonify({"poruka": "Korisnik kreiran"}), 201

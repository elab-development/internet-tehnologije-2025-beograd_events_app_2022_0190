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
            "prezime": k.prezime,
            "email": k.email,
            "uloga": k.uloga
        } for k in korisnici
    ])



@korisnik_bp.route("", methods=["POST"])
def kreiraj_korisnika():
    data = request.json

    novi = Korisnik(
        ime=data["ime"],
        prezime=data["prezime"],
        email=data["email"],
        lozinka=data["lozinka"],  # hash dolazi kasnije
        uloga=data.get("uloga", "korisnik")
    )

    db.session.add(novi)
    db.session.commit()

    return jsonify({
        "poruka": "Korisnik kreiran",
        "id": novi.id
    }), 201

@korisnik_bp.route("/<int:id>", methods=["GET"])
def jedan_korisnik(id):
    k = Korisnik.query.get_or_404(id)

    return jsonify({
        "id": k.id,
        "ime": k.ime,
        "prezime": k.prezime,
        "email": k.email,
        "uloga": k.uloga
    })


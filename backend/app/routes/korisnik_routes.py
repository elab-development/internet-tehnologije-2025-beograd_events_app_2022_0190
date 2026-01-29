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
            "email": k.email,
            "lozinka": k.lozinka,
            "uloga":k.uloga,
            "prezime":k.prezime
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
        uloga=data.get("uloga", "REGISTROVANI")
    )

    db.session.add(novi)
    db.session.commit()

    return jsonify({"poruka": "Korisnik kreiran"}), 201


@korisnik_bp.route("/<int:id>", methods=["PUT"])
def azuriraj_korisnika(id):
    korisnik = Korisnik.query.get(id)

    if not korisnik:
        return jsonify({"poruka": "Korisnik ne postoji"}), 404

    data = request.json

    korisnik.ime = data.get("ime", korisnik.ime)
    korisnik.prezime = data.get("prezime", korisnik.prezime)
    korisnik.email = data.get("email", korisnik.email)
    korisnik.lozinka = data.get("lozinka", korisnik.lozinka)
    korisnik.uloga = data.get("uloga", korisnik.uloga)

    db.session.commit()

    return jsonify({"poruka": "Korisnik uspešno ažuriran"})


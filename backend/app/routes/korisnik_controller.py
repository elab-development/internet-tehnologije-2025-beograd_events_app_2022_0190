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


@korisnik_bp.route("/register", methods=["POST"])
def register():
    data = request.json

    ime = data.get("ime")
    prezime = data.get("prezime")
    email = data.get("email")
    lozinka = data.get("lozinka")

    if not ime or len(ime) < 3:
        return jsonify({"poruka": "Ime mora imati minimum 3 karaktera"}), 400

    if not email or "@gmail.com" not in email:
        return jsonify({"poruka": "Email mora sadržati @gmail.com"}), 400

    if not lozinka or len(lozinka) < 5:
        return jsonify({"poruka": "Lozinka mora imati minimum 5 karaktera"}), 400

    postoji = Korisnik.query.filter_by(email=email).first()
    if postoji:
        return jsonify({"poruka": "Email već postoji"}), 400

    novi = Korisnik(
        ime=ime,
        prezime=prezime,
        email=email,
        lozinka=lozinka,
        uloga="REGISTROVANI"
    )

    db.session.add(novi)
    db.session.commit()

    return jsonify({"poruka": "Uspešna registracija"}), 201


@korisnik_bp.route("/login", methods=["POST"])
def login():
    data = request.json

    email = data.get("email")
    lozinka = data.get("lozinka")

    if not email or not lozinka:
        return jsonify({"poruka": "Email i lozinka su obavezni"}), 400

    korisnik = Korisnik.query.filter_by(email=email).first()

    if not korisnik:
        return jsonify({"poruka": "Korisnik sa tim email-om ne postoji"}), 404

    if korisnik.lozinka != lozinka:
        return jsonify({"poruka": "Pogrešna lozinka"}), 400

    if not lozinka or len(lozinka) < 5:
        return jsonify({"poruka": "Lozinka mora imati minimum 5 karaktera"}), 400

    return jsonify({
        "poruka": "Uspešno prijavljivanje",
        "korisnik": {
            "id": korisnik.id,
            "ime": korisnik.ime,
            "prezime": korisnik.prezime,
            "email": korisnik.email,
            "uloga": korisnik.uloga,
            "lozinka" : korisnik.lozinka
        }
    }), 200

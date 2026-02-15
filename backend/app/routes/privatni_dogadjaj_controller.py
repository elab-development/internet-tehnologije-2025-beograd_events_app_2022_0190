from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.privatni_dogadjaj import PrivatniDogadjaj
from datetime import date

privatni_bp = Blueprint(
    "privatni",
    __name__,
    url_prefix="/api/privatni-dogadjaji"
)


@privatni_bp.route("", methods=["POST"])
def kreiraj_privatni():
    """
    Kreira novi privatni događaj
    ---
    tags:
      - PrivatniDogadjaji
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - naziv
            - opis
            - datum
            - lokacija
            - kapacitet
            - korisnik_id
          properties:
            naziv:
              type: string
            opis:
              type: string
            datum:
              type: string
              example: "2026-06-20"
            lokacija:
              type: string
            kapacitet:
              type: integer
            korisnik_id:
              type: integer
            imageURL:
              type: string
    responses:
      201:
        description: Privatni događaj uspešno kreiran
    """
    data = request.json

    novi = PrivatniDogadjaj(
        naziv=data["naziv"],
        opis=data["opis"],
        datum=data["datum"],
        lokacija=data["lokacija"],
        kapacitet=data["kapacitet"],
        korisnik_id=data["korisnik_id"],
        imageURL=data["imageURL"]
    )

    db.session.add(novi)
    db.session.commit()

    return jsonify({
        "poruka": "Privatni događaj uspešno kreiran",
        "id": novi.id
    }), 201


@privatni_bp.route("", methods=["GET"])
def svi_privatni():
    """
    Vraća sve buduće privatne događaje
    ---
    tags:
      - PrivatniDogadjaji
    responses:
      200:
        description: Lista privatnih događaja
    """
    danas = date.today()
    privatni = PrivatniDogadjaj.query.filter(PrivatniDogadjaj.datum > danas).all()

    return jsonify([
        {
            "id": p.id,
            "naziv": p.naziv,
            "opis": p.opis,
            "datum": str(p.datum),
            "lokacija": p.lokacija,
            "kapacitet": p.kapacitet,
            "korisnik_id": p.korisnik_id,
            "imageURL": p.imageURL
        } for p in privatni
    ])


@privatni_bp.route("/<int:id>", methods=["GET"])
def jedan_privatni(id):
    """
    Vraća jedan privatni događaj po ID-u
    ---
    tags:
      - PrivatniDogadjaji
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Jedan privatni događaj
      404:
        description: Nije pronađen
    """
    p = PrivatniDogadjaj.query.get_or_404(id)

    return jsonify({
        "id": p.id,
        "naziv": p.naziv,
        "opis": p.opis,
        "datum": str(p.datum),
        "lokacija": p.lokacija,
        "kapacitet": p.kapacitet,
        "korisnik_id": p.korisnik_id,
        "imageURL": p.imageURL
    })


@privatni_bp.route("/korisnik/<int:korisnik_id>", methods=["GET"])
def privatni_po_korisniku(korisnik_id):
    """
    Vraća sve privatne događaje određenog korisnika
    ---
    tags:
      - PrivatniDogadjaji
    parameters:
      - name: korisnik_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Lista privatnih događaja korisnika
    """
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
            "korisnik_id": p.korisnik_id,
            "imageURL": p.imageURL
        } for p in privatni
    ])


@privatni_bp.route("/<int:id>", methods=["DELETE"])
def obrisi_privatni(id):
    """
    Briše privatni događaj
    ---
    tags:
      - PrivatniDogadjaji
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Privatni događaj obrisan
      404:
        description: Nije pronađen
    """
    p = PrivatniDogadjaj.query.get_or_404(id)
    db.session.delete(p)
    db.session.commit()
    return jsonify({"poruka": "Privatni događaj obrisan"})


@privatni_bp.route("/<int:id>", methods=["PUT"])
def azuriraj_privatni(id):
    """
    Ažurira privatni događaj
    ---
    tags:
      - PrivatniDogadjaji
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Privatni događaj ažuriran
      404:
        description: Nije pronađen
    """
    p = PrivatniDogadjaj.query.get_or_404(id)
    data = request.json

    p.naziv = data.get("naziv", p.naziv)
    p.opis = data.get("opis", p.opis)
    p.datum = data.get("datum", p.datum)
    p.lokacija = data.get("lokacija", p.lokacija)
    p.kapacitet = data.get("kapacitet", p.kapacitet)
    p.imageURL = data.get("imageURL", p.imageURL)

    db.session.commit()
    return jsonify({"poruka": "Privatni događaj ažuriran"})

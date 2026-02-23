from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import KategorijaDogadjaja

kategorija_bp = Blueprint("kategorija", __name__, url_prefix="/api/kategorije")


@kategorija_bp.route("", methods=["GET"])
def sve_kategorije():
    """
    Vraća sve kategorije događaja
    ---
    tags:
      - Kategorije
    responses:
      200:
        description: Lista svih kategorija
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              naziv:
                type: string
    """
    kategorije = KategorijaDogadjaja.query.all()

    return jsonify([
        {
            "id": k.id,
            "naziv": k.naziv
        } for k in kategorije
    ])


@kategorija_bp.route("", methods=["POST"])
def dodaj_kategoriju():
    """
    Dodaje novu kategoriju
    ---
    tags:
      - Kategorije
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - naziv
          properties:
            naziv:
              type: string
    responses:
      201:
        description: Kategorija uspešno dodata
    """
    data = request.json

    k = KategorijaDogadjaja(naziv=data["naziv"])
    db.session.add(k)
    db.session.commit()

    return jsonify({"poruka": "Kategorija dodata"}), 201


@kategorija_bp.route("/<int:id>", methods=["GET"])
def jedna_kategorija(id):
    """
    Vraća jednu kategoriju po ID-u
    ---
    tags:
      - Kategorije
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Jedna kategorija
      404:
        description: Kategorija nije pronađena
    """
    kategorija = KategorijaDogadjaja.query.get_or_404(id)

    return jsonify({
        "id": kategorija.id,
        "naziv": kategorija.naziv
    })

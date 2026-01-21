from app.extensions import db

class Dogadjaj(db.Model):
    __tablename__ = "dogadjaj"

    id = db.Column(db.Integer, primary_key=True)
    naziv = db.Column(db.String(100), nullable=False)
    opis = db.Column(db.Text, nullable=False)
    datum = db.Column(db.Date, nullable=False)
    lokacija = db.Column(db.String(100), nullable=False)
    cena = db.Column(db.Float)

    imageURL = db.Column(db.String(255))
    sourceURL = db.Column(db.String(255))

    kategorija_dogadjaja_id = db.Column(
        db.Integer,
        db.ForeignKey("kategorija_dogadjaja.id"),
        nullable=False
    )

    omiljeni = db.relationship(
        "OmiljeniDogadjaj",
        backref="dogadjaj",
        lazy=True
    )

    def __repr__(self):
        return f"<Dogadjaj {self.naziv}>"

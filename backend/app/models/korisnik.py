from app.extensions import db

class Korisnik(db.Model):
    __tablename__ = "korisnik"

    id = db.Column(db.Integer, primary_key=True)
    ime = db.Column(db.String(50), nullable=False)
    prezime = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    lozinka = db.Column(db.String(255), nullable=False)
    uloga = db.Column(db.String(20), nullable=False)

    privatni_dogadjaji = db.relationship(
        "PrivatniDogadjaj",
        backref="korisnik",
        lazy=True
    )

    omiljeni_dogadjaji = db.relationship(
        "OmiljeniDogadjaj",
        backref="korisnik",
        lazy=True
    )

    def __repr__(self):
        return f"<Korisnik {self.email}>"

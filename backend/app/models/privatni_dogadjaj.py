from app.extensions import db

class PrivatniDogadjaj(db.Model):
    __tablename__ = "privatni_dogadjaj"

    id = db.Column(db.Integer, primary_key=True)
    naziv = db.Column(db.String(100), nullable=False)
    opis = db.Column(db.Text, nullable=False)
    datum = db.Column(db.Date, nullable=False)
    lokacija = db.Column(db.String(100), nullable=False)
    kapacitet = db.Column(db.Integer, nullable=False)
    
    imageURL = db.Column(db.String(255), nullable=False)
    
    korisnik_id = db.Column(
        db.Integer,
        db.ForeignKey("korisnik.id"),
        nullable=False
    )

    def __repr__(self):
        return f"<PrivatniDogadjaj {self.naziv}>"

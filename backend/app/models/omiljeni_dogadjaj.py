from app.extensions import db

class OmiljeniDogadjaj(db.Model):
    __tablename__ = "omiljeni_dogadjaj"

    korisnik_id = db.Column(
        db.Integer,
        db.ForeignKey("korisnik.id"),
        primary_key=True
    )

    dogadjaj_id = db.Column(
        db.Integer,
        db.ForeignKey("dogadjaj.id"),
        primary_key=True
    )

    podsetnik = db.Column(db.Date)

    def __repr__(self):
        return (
            f"<OmiljeniDogadjaj korisnik={self.korisnik_id} "
            f"dogadjaj={self.dogadjaj_id}>"
        )

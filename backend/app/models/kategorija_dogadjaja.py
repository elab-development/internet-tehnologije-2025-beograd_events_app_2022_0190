from app.extensions import db

class KategorijaDogadjaja(db.Model):
    __tablename__ = "kategorija_dogadjaja"

    id = db.Column(db.Integer, primary_key=True)
    naziv = db.Column(db.String(50), unique=True, nullable=False)

    dogadjaji = db.relationship(
        "Dogadjaj",
        backref="kategorija",
        lazy=True
    )

    def __repr__(self):
        return f"<KategorijaDogadjaja {self.naziv}>"

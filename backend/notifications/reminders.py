from datetime import date
from app.extensions import db
from app.models.omiljeni_dogadjaj import OmiljeniDogadjaj
from app.models.korisnik import Korisnik
from app.models.dogadjaj import Dogadjaj
from mail.mail_service import send_reminder_email

def run_daily_reminders():
    print("Provera dnevnih podsetnika...")

    today = date.today()

    podsetnici = OmiljeniDogadjaj.query.filter(
        OmiljeniDogadjaj.podsetnik == today
    ).all()

    if not podsetnici:
        print("Nema podsetnika za danas")
        return

    print(f"Pronađeno {len(podsetnici)} podsetnika")

    for p in podsetnici:
        korisnik = Korisnik.query.get(p.korisnik_id)
        dogadjaj = Dogadjaj.query.get(p.dogadjaj_id)

        if not korisnik or not dogadjaj:
            continue

        email = korisnik.email


        send_reminder_email(email, dogadjaj)




    print("Dnevni podsetnici završeni")

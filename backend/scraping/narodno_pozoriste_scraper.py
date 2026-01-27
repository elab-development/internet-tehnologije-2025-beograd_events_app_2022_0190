import requests
from bs4 import BeautifulSoup
from datetime import datetime

from app.extensions import db
from app.models.dogadjaj import Dogadjaj


URL = "https://www.narodnopozoriste.rs/repertoar/drama"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "sr-RS,sr;q=0.9",
}

MESECI = {
    "јан": 1,
    "феб": 2,
    "мар": 3,
    "апр": 4,
    "мај": 5,
    "јун": 6,
    "јул": 7,
    "авг": 8,
    "сеп": 9,
    "окт": 10,
    "нов": 11,
    "дец": 12,
}


# ---------------------------------------------------
# Pomocna funkcija – parsiranje datuma
# Primer: "23.01.2026"
# ---------------------------------------------------
from datetime import date

def parse_datum_iz_repertoara(entry):
    """
    HTML struktura:
    <div class="repertoarwide-entry-date">26
        <span class="mesec">јан</span>
    </div>
    """
    try:
        #print(entry)
        date_div = entry.select_one("div.repertoarwide-entry-date")
        if not date_div:
            
            return None

        # DAN (npr. 26)
        dan_text = date_div.contents[1]
        #print(dan_text)
        dan = int(str(dan_text).strip())
        #print(dan)
        # MESEC (npr. јан)
        mesec_el = date_div.select_one("span.mesec")
        if not mesec_el:
            return None

        mesec_txt = mesec_el.get_text(strip=True).lower()
        mesec = MESECI.get(mesec_txt)

        if not mesec:
            return None

        return date(2026, mesec, dan)

    except:
        return None



# ---------------------------------------------------
# GLAVNA FUNKCIJA
# ---------------------------------------------------
def run_narodno_scraping():
    print("Scraping Narodno pozorište")

    r = requests.get(URL, headers=HEADERS, timeout=15)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")

    entries = soup.select("div.repertoarwide-entry")
    print(f"Pronađeno {len(entries)} predstava")

    dodato = 0

    for entry in entries:
        # DATUM
        datum = parse_datum_iz_repertoara(entry)

        if not datum:
            #print("do datuma je")
            continue

        # NASLOV + SOURCE URL
        title_link = entry.select_one("div.entry-title a")
        if not title_link:
            #print("do naslova je")
            continue

        naziv = title_link.get_text(strip=True)
        source_url = title_link.get("href")

        if source_url.startswith("/"):
            source_url = "https://www.narodnopozoriste.rs" + source_url

        # OPIS
        opis_el = entry.select_one("div.entry-title em")
        opis = opis_el.get_text(strip=True) if opis_el else ""

        # SLIKA
        img_el = entry.select_one("img.img-fluid.donottouch")
        image_url = img_el.get("src") if img_el else None
        if image_url and image_url.startswith("/"):
            image_url = "https://www.narodnopozoriste.rs" + image_url

        # DUPLIKATI
        postoji = Dogadjaj.query.filter_by(
            naziv=naziv,
            datum=datum
        ).first()

        if postoji:
            continue

        # UPIS U BAZU
        dogadjaj = Dogadjaj(
            naziv=naziv,
            opis=opis,
            datum=datum,
            lokacija="Narodno pozorište",
            cena=0,
            imageURL=image_url,
            sourceURL=source_url,
            kategorija_dogadjaja_id=3
        )

        db.session.add(dogadjaj)
        dodato += 1

    db.session.commit()
    print(f"Narodno pozorište: dodato {dodato} događaja")

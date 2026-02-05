import requests
from bs4 import BeautifulSoup
from datetime import datetime

from app.extensions import db
from app.models.dogadjaj import Dogadjaj

from datetime import datetime, date
from sqlalchemy import and_, or_



BASE_URL = "https://www.beograd.rs"
LIST_URL = "https://www.beograd.rs/lat/zivot-u-beogradu/manifestacije"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "sr-RS,sr;q=0.9",
}


def scrape_opis(detail_url):
    try:
        r = requests.get(detail_url, headers=HEADERS, timeout=15)
        r.raise_for_status()

        soup = BeautifulSoup(r.text, "html.parser")

        opis_div = soup.select_one("div.story__full-content")
        if not opis_div:
            return ""

        return opis_div.get_text("\n", strip=True)

    except Exception:
        return ""




import re
from datetime import datetime

def extract_datum_from_opis(opis):
    
    try:
        if not opis:
            return None

        tekst = opis.lower()

        if "kada se održava" not in tekst:
            return None

        deo = tekst.split("kada se održava", 1)[1]

        dan_match = re.search(r"\b(\d{1,2})\b", deo)
        if not dan_match:
            return None

        dan = int(dan_match.group(1))

        MESECI = {
            "januar": 1, "februar": 2, "mart": 3, "april": 4,
            "maj": 5, "jun": 6, "jul": 7, "avgust": 8,
            "septembar": 9, "oktobar": 10, "novembar": 11, "decembar": 12
        }

        mesec = None
        for ime, broj in MESECI.items():
            if ime in deo:
                mesec = broj
                break

        if not mesec:
            return None

        return datetime(2026, mesec, dan).date()

    except:
        return None


def extract_lokacija_from_opis(opis):
    try:
        if not opis:
            return None

        tekst = opis.strip()

        if "Gde se održava" not in tekst:
            return None

        deo = tekst.split("Gde se održava", 1)[1]

        linija = deo.strip().split("\n")[0].strip()

        return linija if linija else ""

    except:
        return ""



def run_beograd_scraping():
    print("Scraping beograd.rs manifestacije...")

    dodato = 0

    for page in [1,2,3]:
        url = f"{LIST_URL}?page={page}"
        r = requests.get(url, headers=HEADERS, timeout=15)
        r.raise_for_status()

        soup = BeautifulSoup(r.text, "html.parser")

        cards = soup.select("div.simple-news-card")
        print(f"Beograd.rs: Stranica {page}: pronađeno {len(cards)} događaja")

        for card in cards:
            link_el = card.select_one("a.simple-news-card__link")

            if not link_el:
                continue

            source_url = BASE_URL + link_el["href"]

            title_el = card.select_one("h2.simple-news-card__title")
            naziv = title_el.get_text(strip=True) if title_el else None
            if not naziv:
                continue
            
            img_el = card.select_one("img.image")
            image_url = img_el["src"] if img_el and img_el.get("src") else None
            if image_url and image_url.startswith("/"):
                image_url = BASE_URL + image_url

            lokacija = ""
            datum = ""

            opis = scrape_opis(source_url)

            datum = extract_datum_from_opis(opis)
            lokacija = extract_lokacija_from_opis(opis)
            
            with db.session.no_autoflush:
                postoji = Dogadjaj.query.filter(
                    or_(
                        Dogadjaj.naziv == naziv,
                        Dogadjaj.sourceURL == source_url
                    )
                ).first()

            if postoji:
                continue

            dogadjaj = Dogadjaj(
                naziv=naziv,
                opis=opis,
                datum=datum,
                lokacija=lokacija,
                cena=0,
                imageURL=image_url,
                sourceURL=source_url,
                kategorija_dogadjaja_id=2
            )

            db.session.add(dogadjaj)
            dodato += 1

    db.session.commit()
    print(f"Beograd.rs: dodato {dodato} događaja")

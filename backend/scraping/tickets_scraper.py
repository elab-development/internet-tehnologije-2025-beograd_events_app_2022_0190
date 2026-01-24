import requests
from bs4 import BeautifulSoup
from datetime import datetime
from app.extensions import db
from app.models.dogadjaj import Dogadjaj







URL = "https://tickets.rs"

MESECI = {
    "januar": 1,
    "februar": 2,
    "mart": 3,
    "april": 4,
    "maj": 5,
    "jun": 6,
    "jul": 7,
    "avgust": 8,
    "septembar": 9,
    "oktobar": 10,
    "novembar": 11,
    "decembar": 12,
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept-Language": "sr-RS,sr;q=0.9,en-US;q=0.8,en;q=0.7",
}






def scrape_detail_page(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        r.raise_for_status()

        soup = BeautifulSoup(r.text, "html.parser")

        if "event-list-item" not in r.text:
            print("❌ Nije event stranica:", url)
            return None, None, ""
        
        opis = ""
        #opis = scrape_opis_bez_seleniuma(url)   
        
        # DATUM + CENA
        datum = None
        cena = None

        item = soup.select_one(".date-time")
        if item:
            text = item.get_text(" ", strip=True).lower()

            # DATUM
            for mesec, broj in MESECI.items():
                if mesec in text:
                    try:
                        parts = text.replace(".", "").split()
                        i = parts.index(mesec)
                        dan = int(parts[i - 1])
                        godina = int(parts[i + 1])
                        datum = datetime(godina, broj, dan).date()
                        break
                    except:
                        pass

            cena_item = soup.select_one(".price")
            if cena_item:
                text = cena_item.get_text(" ", strip=True).lower()
            # CENA
            if "rsd" in text:
                try:
                    broj = (
                        text.replace(".", "")
                        .replace(",", ".")
                        .split("od")[-1]
                        .split()[0]
                    )
                    cena = float(broj)
                except:
                    pass
        return datum, cena, opis

    except Exception as e:
        print("⚠️ Greška:", e)
        return None, None, ""






def run_scraping():
    print("🕷️ Scraping tickets.rs (FULL)...")

    r = requests.get(URL, headers=HEADERS, timeout=15)

    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")
   
    slides = soup.select(".swiper-slide")
    dodato = 0

    for slide in slides:
        eventi = slide.select('a[href^="/tour/"]')

        for e in eventi:
            naziv_el = e.select_one("h3")
            datum_el = e.select_one(".date-time")
            lokacija_el = e.select_one(".place")
            cena_el = e.select_one(".price")

            if not (naziv_el and datum_el and lokacija_el):
                continue

            naziv = naziv_el.get_text(strip=True)
            #datum = parse_datum(datum_el.get_text())
            lokacija = lokacija_el.get_text(strip=True)

           


            #cena = parse_cena(cena_el.get_text()) if cena_el else None

            image_url = None
            style = e.get("style", "")
            if "url(" in style:
                image_url = style.split("url(")[1].split(")")[0].replace('"', "")

            source_url = URL + e.get("href")

            datum, cena, opis = scrape_detail_page(source_url)

            if not datum:
                continue

            postoji = Dogadjaj.query.filter_by(
                naziv=naziv,
                datum=datum
            ).first()

            if postoji:
                continue
            


            dogadjaj = Dogadjaj(
                naziv=naziv,
                opis="Za vise detalja posetite sajt"+source_url,
                datum=datum,
                lokacija=lokacija,
                cena=cena,
                imageURL=image_url,
                sourceURL=source_url,
                kategorija_dogadjaja_id=1
            )

            db.session.add(dogadjaj)
            dodato += 1
    db.session.commit()
    print(f"✅ Dodato novih događaja: {dodato}")

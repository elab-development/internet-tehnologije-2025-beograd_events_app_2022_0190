# Beograd Events App

## Opis projekta

Beograd Events App je web aplikacija za automatsko prikupljanje, obradu i prikaz događaja u Beogradu.

Aplikacija koristi web scraping tehniku za preuzimanje podataka sa tri različita sajta i skladišti ih u MySQL bazu podataka. Korisnici mogu da pregledaju događaje, registruju se, prijave, dodaju događaje u omiljene i podese podsetnike putem email-a.

Pored toga, aplikacija prikazuje:
- Trenutnu temperaturu (OpenWeather API)
- Mapu Beograda (OpenStreetMap API)

---

## Funkcionalnosti

- Web scraping događaja sa više izvora
- Čuvanje događaja u bazi
- REST API za rad sa događajima
- Registracija i prijava korisnika
- Dodavanje događaja u omiljene
- Email podsetnici za događaje
- Prikaz vremenske prognoze
- Prikaz mape Beograda
- Dockerizovana aplikacija

---

## Arhitektura sistema

Aplikacija je podeljena na tri glavna servisa:

- **Frontend** (React)
- **Backend** (Flask + SQLAlchemy)
- **Baza podataka** (MySQL)

Sistem koristi Docker Compose za orkestraciju servisa.

---

## Tehnologije

### Backend
- Python
- Flask
- SQLAlchemy
- BeautifulSoup (web scraping)
- Requests
- MySQL
- OpenWeather API
- OpenStreetMap API
- SMTP (email podsetnici)

### Frontend
- React
- JavaScript
- CSS

### DevOps
- Docker
- Docker Compose

---

## Pokretanje aplikacije

1. Otvoriti terminal u root folderu projekta.

2. Pokrenuti komandu:

docker compose up --build

3. Aplikacija je dostupna na:

Frontend:
http://localhost:3000

Backend:
http://localhost:5000

## Autori

Branka Baković
Nikola Ilić  
Internet Tehnologije 2026 
Beograd

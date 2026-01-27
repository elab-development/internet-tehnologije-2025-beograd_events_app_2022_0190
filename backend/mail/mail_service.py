import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import current_app


def send_reminder_email(to_email, dogadjaj):
    try:
        msg = MIMEMultipart()
        msg["From"] = current_app.config["MAIL_USERNAME"]
        msg["To"] = to_email
        msg["Subject"] = f"📅 Podsetnik: {dogadjaj.naziv}"

        body = f"""
Zdravo 👋

Ovo je podsetnik za događaj koji ste sačuvali ❤️

📌 Naziv: {dogadjaj.naziv}
📅 Datum: {dogadjaj.datum}
📍 Lokacija: {dogadjaj.lokacija or "Nije navedeno"}
💰 Cena: {dogadjaj.cena if dogadjaj.cena is not None else "Besplatno"}

🔗 Više detalja:
{dogadjaj.sourceURL}

Vidimo se! 🎉
BG Events
        """

        msg.attach(MIMEText(body, "plain", "utf-8"))

        server = smtplib.SMTP(
            current_app.config["MAIL_HOST"],
            current_app.config["MAIL_PORT"]
        )
        server.starttls()
        server.login(
            current_app.config["MAIL_USERNAME"],
            current_app.config["MAIL_PASSWORD"]
        )

        server.send_message(msg)
        server.quit()

        print(f"Email poslat: {to_email}")

    except Exception as e:
        print(f"❌ Greška pri slanju maila ({to_email}):", e)

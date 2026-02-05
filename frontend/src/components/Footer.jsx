import "../styles/footer.css";

function Footer() {
  return (
    <footer className="app-footer">
      <div className="footer-content">

        <div className="footer-brand">
        {}

          <h3>BG Events</h3>
          <p>Sva dešavanja u Beogradu na jednom mestu</p>
        </div>

        <div className="footer-autori">
            <p><u>Branka Bakovic 2022/0295</u></p>
            <p><u>Nikola Ilic 2022/0190</u></p>
        </div>

      </div>

      <div className="footer-bottom">
        © {new Date().getFullYear()} BG Events · Beograd
      </div>
    </footer>
  );
}

export default Footer;

import { Link, useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import { logoutUser } from "../services/authService.js";
import "../styles/navbar.css";
import Button from "./button.jsx";


function Navbar() {
  const navigate = useNavigate();
  const loggedUser = JSON.parse(localStorage.getItem("loggedUser"));
  const uloga = loggedUser?.uloga;

  const [visible, setVisible] = useState(true);

  const handleLogout = () => {
    logoutUser();
    navigate("/");
  };

  useEffect(() => {
    let lastScrollY = window.scrollY;

    const handleScroll = () => {
      if (window.scrollY > 80) {
        setVisible(false);
      } else {
        setVisible(true);
      }
      lastScrollY = window.scrollY;
    };

    const handleMouseMove = (e) => {
      if (e.clientY < 20) {
        setVisible(true);
      }
    };

    window.addEventListener("scroll", handleScroll);
    window.addEventListener("mousemove", handleMouseMove);

    return () => {
      window.removeEventListener("scroll", handleScroll);
      window.removeEventListener("mousemove", handleMouseMove);
    };
  }, []);

  return (
    <nav className={`navbar ${visible ? "show" : "hide"}`}>
      <div className="navbar-left">
        {(uloga === "REGISTROVANI" || uloga === "ADMIN") && (
          <>
            <Link to="/home" className="nav-link">Događaji</Link>
            <span
  className="nav-link"
  onClick={() => navigate("/private-events")}
>
  Privatni događaji
</span>
<span
  className="nav-link"
  onClick={() => navigate("/user")}
>
  Korisnik
</span>

          </>
        )}

{uloga === "ADMIN" && (
  <>
    <span
      className="nav-link"
      onClick={() => navigate("/users")}
    >
      Korisnički nalozi
    </span>

    <Link to="/categories" className="nav-link">
      Kategorija događaja
    </Link>
  </>
)}

      </div>

      <div className="navbar-right">
        {loggedUser && (
          <>
            
            <Button text="Logout" onClick={handleLogout} />

          </>
        )}
      </div>
    </nav>
  );
}

export default Navbar;

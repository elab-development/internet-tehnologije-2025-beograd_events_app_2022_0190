import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { registerUser } from "../services/authService.js";
import "../styles/auth.css";
import avatar from "../assets/avatar.jpg"

function Register() {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    name: "",
    surname: "",
    email: "",
    password: "",
  });

  useEffect(() => {
    window.onpopstate = () => {
      navigate("/");
    };
  }, [navigate]);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const result = await registerUser(form);
    if (!result.success) {
      alert(result.message);
      return;
    }

    alert("Registracija uspešna!");
    navigate("/");
  };

  return (
    <div className="auth-page">
      <div className="auth-card">
      <img src={avatar} alt="Avatar" className="avatar" />


        <h2>Registracija</h2>

        <input name="name" placeholder="Ime" onChange={handleChange} />
        <input name="surname" placeholder="Prezime" onChange={handleChange} />
        <input name="email" placeholder="Email" onChange={handleChange} />
        <input
          type="password"
          name="password"
          placeholder="Lozinka"
          onChange={handleChange}
        />

        <button onClick={handleSubmit}>Registruj se</button>

        

        <div className="auth-link" onClick={() => navigate("/")}>
          Već imaš nalog? Prijavi se
        </div>
      </div>
      <button className="guest-btn" onClick={() => navigate("/Home")}>
          Uđi kao gost
        </button>
    </div>
  );
}

export default Register;

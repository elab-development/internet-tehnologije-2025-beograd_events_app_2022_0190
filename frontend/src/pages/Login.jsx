import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { loginUser } from "../services/authService";
import "../styles/auth.css";

function Login() {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    email: "",
    password: "",
  });

  const handleSubmit = (e) => {
    e.preventDefault();

    const result = loginUser(form.email, form.password);

    if (!result.success) {
      alert(result.message); // ❌ nevalidan korisnik
      return;
    }

    // ✅ validan korisnik
    navigate("/home");
  };

  return (
    <div className="auth-page">
      <div className="auth-card">
        <h2>Login</h2>

        <input
          type="email"
          placeholder="Email"
          value={form.email}
          onChange={(e) =>
            setForm({ ...form, email: e.target.value })
          }
        />

        <input
          type="password"
          placeholder="Lozinka"
          value={form.password}
          onChange={(e) =>
            setForm({ ...form, password: e.target.value })
          }
        />

        <button onClick={handleSubmit}>Prijavi se</button>

        <div
          className="auth-link"
          onClick={() => navigate("/register")}
        >
          Nemate nalog? Registrujte se
        </div>
      </div>

      <button
        className="guest-btn"
        onClick={() => navigate("/home")}
      >
        Uđi kao gost
      </button>
    </div>
  );
}

export default Login;

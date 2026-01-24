import { useState } from "react";
import "../styles/userPanel.css";

function UserPanel({ user, onUpdate }) {
  const [open, setOpen] = useState(false);
  const [form, setForm] = useState({ ...user });
  const [confirm, setConfirm] = useState(false);

  const handleSave = () => {
    const users = JSON.parse(localStorage.getItem("users")) || [];

    const updated = users.map(u =>
      u.email === user.email ? form : u
    );

    localStorage.setItem("users", JSON.stringify(updated));
    alert("Korisnik je uspešno ažuriran!");
    setConfirm(false);
    onUpdate();
  };

  return (
    <div className="user-panel">
      <div
        className="user-panel-header"
        onClick={() => setOpen(!open)}
      >
        <span>{user.name} {user.surname}</span>
        <span className={`arrow ${open ? "open" : ""}`}>⌄</span>
      </div>

      {open && (
  <div className="user-panel-body">

    <label>Ime</label>
    <input
      type="text"
      value={form.name}
      onChange={e => setForm({ ...form, name: e.target.value })}
    />

    <label>Prezime</label>
    <input
      type="text"
      value={form.surname}
      onChange={e => setForm({ ...form, surname: e.target.value })}
    />

    <label>Email</label>
    <input
      type="text"
      value={form.email}
      onChange={e => setForm({ ...form, email: e.target.value })}
    />

    <label>Lozinka</label>
    <input
      type="text"
      value={form.password}
      onChange={e => setForm({ ...form, password: e.target.value })}
    />

    <label>Uloga</label>
    <input
      type="text"
      value={form.uloga}
      onChange={e => setForm({ ...form, uloga: e.target.value })}
    />

    <button onClick={() => setConfirm(true)}>
      Ažuriraj
    </button>

    {confirm && (
      <div className="confirm-box">
        <p>Da li ste sigurni da želite da ažurirate korisnika?</p>
        <button onClick={handleSave}>Da</button>
        <button onClick={() => setConfirm(false)}>Ne</button>
      </div>
    )}

  </div>
)}

    </div>
  );
}

export default UserPanel;

import { useState } from "react";
import "../styles/userPanel.css";

function UserPanel({ user, onUpdate }) {
  const [open, setOpen] = useState(false);
  const [confirm, setConfirm] = useState(false);

  const [form, setForm] = useState({
    ime: user.ime,
    prezime: user.prezime,
    email: user.email,
    lozinka: user.lozinka,
    uloga: user.uloga,
  });

  const handleSave = async () => {
    try {
      const response = await fetch(
        `http://localhost:5000/api/korisnici/${user.id}`,3*
        {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(form),
        }
      );

      if (!response.ok) {
        alert("Greška pri ažuriranju korisnika");
        return;
      }

      alert("Korisnik je uspešno ažuriran!");
      setConfirm(false);
      onUpdate(); 
    } catch (error) {
      alert("Backend nije dostupan");
    }
  };

  return (
    <div className="user-panel">
      <div
        className="user-panel-header"
        onClick={() => setOpen(!open)}
      >
        <span>{user.ime} {user.prezime}</span>
        <span className={`arrow ${open ? "open" : ""}`}>⌄</span>
      </div>

      {open && (
        <div className="user-panel-body">

          <label>Ime</label>
          <input
            type="text"
            value={form.ime}
            onChange={(e) =>
              setForm({ ...form, ime: e.target.value })
            }
          />

          <label>Prezime</label>
          <input
            type="text"
            value={form.prezime}
            onChange={(e) =>
              setForm({ ...form, prezime: e.target.value })
            }
          />

          <label>Email</label>
          <input
            type="text"
            value={form.email}
            onChange={(e) =>
              setForm({ ...form, email: e.target.value })
            }
          />

          <label>Lozinka</label>
          <input
            type="text"
            value={form.lozinka}
            onChange={(e) =>
              setForm({ ...form, lozinka: e.target.value })
            }
          />

          <label>Uloga</label>
          <input
            type="text"
            value={form.uloga}
            onChange={(e) =>
              setForm({ ...form, uloga: e.target.value })
            }
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

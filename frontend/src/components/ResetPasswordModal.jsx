import { useState } from "react";
import "../styles/resetPasswordModal.css";

function ResetPasswordModal({ onClose }) {
  const [oldPass, setOldPass] = useState("");
  const [newPass, setNewPass] = useState("");

  const users = JSON.parse(localStorage.getItem("users")) || [];
  const loggedUser = JSON.parse(localStorage.getItem("loggedUser"));

  const handleReset = () => {
    const index = users.findIndex(u => u.email === loggedUser.email);

    if (users[index].password !== oldPass) {
      alert("Stara lozinka nije ispravna!");
      return;
    }

    users[index].password = newPass;
    localStorage.setItem("users", JSON.stringify(users));
    localStorage.setItem("loggedUser", JSON.stringify(users[index]));

    alert("Lozinka je uspešno promenjena!");
    onClose();
  };

  return (
    <div className="rpm-overlay">
      <div className="rpm-modal">
        <h3>Resetovanje lozinke</h3>

        <input
          type="password"
          placeholder="Stara lozinka"
          value={oldPass}
          onChange={e => setOldPass(e.target.value)}
        />

        <input
          type="password"
          placeholder="Nova lozinka"
          value={newPass}
          onChange={e => setNewPass(e.target.value)}
        />

        <div className="rpm-actions">
          <button onClick={handleReset}>Sačuvaj</button>
          <button className="cancel" onClick={onClose}>
            Otkaži
          </button>
        </div>
      </div>
    </div>
  );
}

export default ResetPasswordModal;

import { useState } from "react";
import "../styles/resetPasswordModal.css";

function ResetPasswordModal({ onClose }) {
  const [oldPass, setOldPass] = useState("");
  const [newPass, setNewPass] = useState("");

  const loggedUser = JSON.parse(localStorage.getItem("loggedUser"));

  const handleReset = async () => {
    if (loggedUser.lozinka !== oldPass) {
      alert("Stara lozinka nije ispravna!");
      return;
    }

    try {
      const response = await fetch(
        `http://localhost:5000/api/korisnici/${loggedUser.id}`,
        {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            lozinka: newPass,
          }),
        }
      );

      if (!response.ok) {
        alert("Greška pri promeni lozinke");
        return;
      }

      const updatedUser = {
        ...loggedUser,
        lozinka: newPass,
      };

      localStorage.setItem("loggedUser", JSON.stringify(updatedUser));

      alert("Lozinka je uspešno promenjena!");
      onClose();
    } catch (error) {
      alert("Backend nije dostupan");
    }
  };

  return (
    <div className="rpm-overlay">
      <div className="rpm-modal">
        <h3>Resetovanje lozinke</h3>

        <input
          type="password"
          placeholder="Stara lozinka"
          value={oldPass}
          onChange={(e) => setOldPass(e.target.value)}
        />

        <input
          type="password"
          placeholder="Nova lozinka"
          value={newPass}
          onChange={(e) => setNewPass(e.target.value)}
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

import { useState } from "react";
import ReactDOM from "react-dom";
import { updatePrivateEvent } from "../services/privateEventService.js";
import "../styles/privateEventModal.css";

function PrivateEventModal({ event, onClose, onSave, loggedUser }) {
  const [form, setForm] = useState({ ...event });

  const handleSave = () => {
    updatePrivateEvent(form, loggedUser);
    onSave();
  };

  return ReactDOM.createPortal(
    <div className="pe-modal-backdrop" onClick={onClose}>
      <div
        className="pe-modal"
        onClick={(e) => e.stopPropagation()}
      >
        <h2>Izmeni privatni događaj</h2>

        <label>Naziv</label>
        <input
          value={form.naziv}
          onChange={e =>
            setForm({ ...form, naziv: e.target.value })
          }
        />

        <label>Opis</label>
        <textarea
          value={form.opis}
          onChange={e =>
            setForm({ ...form, opis: e.target.value })
          }
        />

        <label>Datum</label>
        <input
          type="date"
          value={form.datum}
          onChange={e =>
            setForm({ ...form, datum: e.target.value })
          }
        />

        <label>Lokacija</label>
        <input
          value={form.lokacija}
          onChange={e =>
            setForm({ ...form, lokacija: e.target.value })
          }
        />

        <label>Kapacitet</label>
        <input
          type="number"
          value={form.kapacitet}
          onChange={e =>
            setForm({ ...form, kapacitet: e.target.value })
          }
        />

        <div className="pe-modal-actions">
          <button onClick={handleSave}>Sačuvaj</button>
        </div>
      </div>
    </div>,
    document.getElementById("modal-root")
  );
}

export default PrivateEventModal;

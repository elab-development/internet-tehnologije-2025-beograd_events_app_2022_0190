import { useEffect, useState, useRef } from "react";
import {
  createPrivateEvent,
  getPrivateEventsForUser,
  deletePrivateEvent
} from "../services/privateEventService.js";
import {
  getAllCategories,
  createCategory
} from "../services/categoryService.js";
import PrivateEventModal from "../components/privateEventModal.jsx";
import "../styles/privateEvent.css";

function PrivateEvents() {

  // ✅ loggedUser se učitava JEDNOM
  const [loggedUser] = useState(() =>
    JSON.parse(localStorage.getItem("loggedUser"))
  );

  const [events, setEvents] = useState([]);
  const [categories, setCategories] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [selectedEvent, setSelectedEvent] = useState(null);
  const [newCategory, setNewCategory] = useState("");

  const scrollRef = useRef(null);

  const [form, setForm] = useState({
    naziv: "",
    opis: "",
    datum: "",
    lokacija: "",
    kapacitet: "",
    categoryId: ""
  });

  // ✅ useEffect BEZ petlje
  useEffect(() => {
    if (!loggedUser) return;

    setEvents(getPrivateEventsForUser(loggedUser));
    setCategories(getAllCategories());
  }, []);

  if (!loggedUser) {
    return <h2>Morate biti prijavljeni</h2>;
  }

  const handleCreate = () => {
    const result = createPrivateEvent(form, loggedUser);

    if (!result.success) {
      alert(result.message);
      return;
    }

    setEvents(getPrivateEventsForUser(loggedUser));
    setForm({
      naziv: "",
      opis: "",
      datum: "",
      lokacija: "",
      kapacitet: "",
      categoryId: ""
    });
  };

  const handleDelete = (id) => {
    if (!window.confirm("Da li ste sigurni?")) return;
    deletePrivateEvent(id, loggedUser);
    setEvents(getPrivateEventsForUser(loggedUser));
  };

  const scrollLeft = () => {
    scrollRef.current.scrollBy({ left: -300, behavior: "smooth" });
  };

  const scrollRight = () => {
    scrollRef.current.scrollBy({ left: 300, behavior: "smooth" });
  };

  return (
    <div className="pe-page">

      {/* HERO */}
      <div className="pe-hero">
        <h1>Privatni događaj</h1>
        <p>Kreiraj i upravljaj svojim privatnim događajima</p>
      </div>

      <div className="pe-container">

        {/* FORMA */}
        <div className="pe-form">
          <h2>Kreiranje privatnog događaja</h2>

          <input
            placeholder="Naziv"
            value={form.naziv}
            onChange={e => setForm({ ...form, naziv: e.target.value })}
          />

          <textarea
            placeholder="Opis"
            value={form.opis}
            onChange={e => setForm({ ...form, opis: e.target.value })}
          />

          <input
            type="date"
            value={form.datum}
            onChange={e => setForm({ ...form, datum: e.target.value })}
          />

          <input
            placeholder="Lokacija"
            value={form.lokacija}
            onChange={e => setForm({ ...form, lokacija: e.target.value })}
          />

          <input
            type="number"
            placeholder="Kapacitet"
            value={form.kapacitet}
            onChange={e => setForm({ ...form, kapacitet: e.target.value })}
          />

          <select
            value={form.categoryId}
            onChange={e =>
              setForm({ ...form, categoryId: Number(e.target.value) })
            }
          >
            <option value="">Izaberi kategoriju</option>
            {categories.map(c => (
              <option key={c.id} value={c.id}>{c.naziv}</option>
            ))}
          </select>

          <input
            placeholder="Nova kategorija (ako ne postoji)"
            value={newCategory}
            onChange={e => setNewCategory(e.target.value)}
          />

          <button
            type="button"
            onClick={() => {
              const result = createCategory(newCategory);

              if (!result.success) {
                alert(result.message);
                return;
              }

              const updatedCategories = getAllCategories();
              setCategories(updatedCategories);

              const created = updatedCategories.find(
                c => c.naziv.toLowerCase() === newCategory.trim().toLowerCase()
              );

              if (created) {
                setForm({ ...form, categoryId: created.id });
              }

              setNewCategory("");
            }}
          >
            Dodaj kategoriju
          </button>

          <button onClick={handleCreate}>
            Kreiraj privatni događaj
          </button>
        </div>

        {/* MOJI DOGAĐAJI */}
        <h2 className="pe-my-title">Moji događaji</h2>

        <div className="pe-my-wrapper">

          <div className="pe-events-row" ref={scrollRef}>
            {events.map(event => (
              <div key={`private-${event.id}`} className="pe-card">

                <img src={event.imageURL} alt={event.naziv} />
                <h3>{event.naziv}</h3>

                <div className="pe-card-menu">
                  <button className="menu-btn">⋮</button>

                  <div className="menu-dropdown">
                    <button
                      onClick={() => {
                        setSelectedEvent(event);
                        setShowModal(true);
                      }}
                    >
                      Izmeni
                    </button>

                    <button
                      className="danger"
                      onClick={() => handleDelete(event.id)}
                    >
                      Obriši
                    </button>
                  </div>
                </div>

              </div>
            ))}
          </div>

          {/* ✅ STRELICE ISPOD, NA SREDINI */}
          {events.length > 3 && (
            <div className="pe-arrows-bottom">
              <button className="pe-arrow" onClick={scrollLeft}>◀</button>
              <button className="pe-arrow" onClick={scrollRight}>▶</button>
            </div>
          )}

        </div>
      </div>

      {showModal && (
        <PrivateEventModal
          event={selectedEvent}
          loggedUser={loggedUser}
          onClose={() => setShowModal(false)}
          onSave={() => {
            setEvents(getPrivateEventsForUser(loggedUser));
            setShowModal(false);
          }}
        />
      )}
    </div>
  );
}

export default PrivateEvents;

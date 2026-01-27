import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getAllEvents } from "../services/eventService.js";
import { logoutUser } from "../services/authService.js";
import "../styles/home.css";
import { getCategoryById } from "../services/categoryService.js";
import { getAllPrivateEvents } from "../services/privateEventService.js";



function Home() {
  const loggedUser = JSON.parse(localStorage.getItem("loggedUser"));

  const navigate = useNavigate();
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const privateEvents = getAllPrivateEvents();
  
  const [searchOpen, setSearchOpen] = useState(false);
  const [searchTerm, setSearchTerm] = useState("");
  const [allEvents, setAllEvents] = useState([]);

  

  useEffect(() => {
    setTimeout(() => {
      const publicEvents = getAllEvents();
      const privateEvents = getAllPrivateEvents();
  
      const data = [...privateEvents, ...publicEvents];
      setAllEvents(data);
setEvents(data);

      setLoading(false);
    }, 2000);
  }, []);
  
  const filteredEvents = allEvents.filter(event =>
    event.naziv &&
    event.naziv.toLowerCase().includes(searchTerm.trim().toLowerCase())
  );
  
  
  if (loading) {
    return (
      <div className="loader-center">
        <div className="loader"></div>
      </div>
    );
  }

  return (
    <div className="home-container">
      {/* 🔴 BORDO HERO SEKCIJA */}
      <div className="hero-section">
  <h1>Događaji u Beogradu...</h1>

  <div className="search-container">
    {searchOpen && (
      <div className="search-box">
        <input
          type="text"
          placeholder="Pretraži događaje..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
        <button
  className="search-reset"
  onClick={() => {
    setSearchTerm("");
    setEvents(allEvents);
  }}
>
  ⟳
</button>

      </div>
    )}

    <button
      className="search-icon"
      onClick={() => setSearchOpen(prev => !prev)}
    >
      🔍
    </button>
  </div>
</div>


      <div className="events-grid-wrapper">
        <div className="events-grid">
        {(searchTerm ? filteredEvents : allEvents).map((event) => (
            <div
              className="event-card"
              key={`${event.user ? "private" : "public"}-${event.id}`}

              onClick={() =>
                navigate(
                  event.user
                    ? `/events/private/${event.id}`
                    : `/events/public/${event.id}`
                )
              }
              
            >
              <div className="event-image-wrapper">
                <img
                  src={event.imageURL || "https://via.placeholder.com/300"}
                  alt={event.naziv}
                />

{event.categoryId && (
  <div className="event-overlay">
    <span>
      {getCategoryById(event.categoryId)?.naziv}
    </span>
  </div>
)}
              </div>

              <h3 className="event-title">{event.naziv}</h3>
            </div>
          ))}
        </div>
      </div>

      
    </div>
  );
}

export default Home;

import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getAllEvents } from "../services/eventService.js";
import { logoutUser } from "../services/authService.js";
import "../styles/home.css";
import { getCategoryById } from "../services/categoryService.js";
import { getAllPrivateEvents } from "../services/privateEventService.js";

// ➕ MAPA
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import "leaflet/dist/leaflet.css";

import L from "leaflet";
import "leaflet/dist/leaflet.css";

// Fix za default marker
delete L.Icon.Default.prototype._getIconUrl;

L.Icon.Default.mergeOptions({
  iconRetinaUrl:
    "https://unpkg.com/leaflet@1.7.1/dist/images/marker-icon-2x.png",
  iconUrl:
    "https://unpkg.com/leaflet@1.7.1/dist/images/marker-icon.png",
  shadowUrl:null,
});

function Home() {
  const loggedUser = JSON.parse(localStorage.getItem("loggedUser"));

  const navigate = useNavigate();
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const privateEvents = getAllPrivateEvents();

  const [searchOpen, setSearchOpen] = useState(false);
  const [searchTerm, setSearchTerm] = useState("");
  const [allEvents, setAllEvents] = useState([]);

  // VREME
  const [weather, setWeather] = useState(null);

  useEffect(() => {
    setTimeout(async () => {
      const publicEvents = await getAllEvents();
      const privateEvents = await getAllPrivateEvents();

      const data = [...privateEvents, ...publicEvents];

      setAllEvents(data);
      
      setEvents(data);
      console.log("DOBIJENI DOGADJAJI:", data);
      console.log("PRVI EVENT:", data[0]);
      setLoading(false);
    }, 2000);
  }, []);

  // FETCH TEMPERATURE
  useEffect(() => {
    fetch(`${process.env.REACT_APP_API_URL}/dogadjaji`)
      .then(res => res.json())
      .then(data => {
        if (data.length > 0 && data[0].temperatura) {
          setWeather({
            temperatura: data[0].temperatura,
            vreme: data[0].vreme
          });
        }
      });
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
      <div className="hero-section">

        <div className="hero-content">

          <div className="hero-left">
            <h1>Događaji u Beogradu...</h1>

            {weather && (
              <div className="weather-box">
                🌡 {weather.temperatura}°C | {weather.vreme}
              </div>
            )}
          </div>

          <div className="hero-map">
            <MapContainer
              center={
                allEvents.some(e => e.lat && e.lon)
                  ? [
                    parseFloat(allEvents.find(e => e.lat && e.lon).lat),
                    parseFloat(allEvents.find(e => e.lat && e.lon).lon)
                  ]
                  : [44.8170058, 20.4610046]
              }
              zoom={12}
              scrollWheelZoom={false}
            >
              <TileLayer
                attribution='&copy; OpenStreetMap contributors'
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
              />

              {allEvents
                .filter(event => event.lat && event.lon)
                .map(event => (
                  <Marker
                    key={`map-${event.id}`}
                    position={[
                      parseFloat(event.lat),
                      parseFloat(event.lon)
                    ]}
                  >
                    <Popup>
                      <strong>{event.naziv}</strong>
                      <br />
                      📍 {event.lokacija}
                      <br />
                      📅 {event.datum}
                      {event.temperatura && (
                        <>
                          <br />
                          🌡 {event.temperatura}°C
                        </>
                      )}
                    </Popup>
                  </Marker>
                ))}
            </MapContainer>
          </div>

        </div>

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
                  event.korisnik_id
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

                {event.datum && (
                  <div className="event-overlay">
                    <span>{event.datum}</span>
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
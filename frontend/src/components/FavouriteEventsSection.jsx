import { useNavigate } from "react-router-dom";
import "../styles/favouriteSection.css";
import { getEventById } from "../services/eventService.js";
import { getPrivateEventById } from "../services/privateEventService.js";


function FavouriteEventsSection() {
  const navigate = useNavigate();
  const user = JSON.parse(localStorage.getItem("loggedUser"));
  const data =
    JSON.parse(localStorage.getItem("favouriteEvents")) || {};

  const favourites = data[user.email] || [];

  if (favourites.length === 0) return null;

  return (
    <div className="fav-section">
      <h2>Omiljeni događaji</h2>

      <div className="events-grid">
      {favourites.map(f => {
  let event = null;
  let route = "";

  if (f.eventType === "PRIVATE") {
    event = getPrivateEventById(f.eventId);
    route = `/events/private/${f.eventId}`;
  } else {
    // sve ostalo je PUBLIC
    event = getEventById(f.eventId);
    route = `/events/public/${f.eventId}`;
  }

  if (!event) return null;

  return (
    <div
      key={`${f.eventType ?? "PUBLIC"}-${f.eventId}`}
      className="event-card"
      onClick={() => navigate(route)}
    >
      <div className="event-title">
        {event.naziv}
      </div>
    </div>
  );
})}



      </div>
    </div>
  );
}

export default FavouriteEventsSection;

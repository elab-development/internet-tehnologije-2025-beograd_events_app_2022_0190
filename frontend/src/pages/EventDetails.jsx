import { useEffect, useState } from "react";
import { useParams, useLocation } from "react-router-dom";

import { getEventById } from "../services/eventService.js";
import { getPrivateEventById } from "../services/privateEventService.js";
import { getCategoryById } from "../services/categoryService.js";

import {
  isFavourite,
  addFavouriteEvent,
  removeFavouriteEvent
} from "../services/favouriteService";

import "../styles/home.css";
import "../styles/eventDetails.css";

function EventDetails() {
  const { id } = useParams();
  const location = useLocation();

  const loggedUser = JSON.parse(localStorage.getItem("loggedUser"));
  const canFavourite = loggedUser !== null;

  const [event, setEvent] = useState(null);
  const [category, setCategory] = useState(null);
  const [favourite, setFavourite] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchEvent = async () => {
      setLoading(true);

      let foundEvent = null;

      if (location.pathname.includes("/events/private")) {
        foundEvent = await getPrivateEventById(id);
      } else {
        foundEvent = await getEventById(id);
      }

      setEvent(foundEvent);

      // ⚠️ ako ti više ne koristiš kategorije, može i da ostane null
      if (foundEvent?.categoryId) {
        const cat = await getCategoryById(foundEvent.categoryId);
        setCategory(cat);
      } else {
        setCategory(null);
      }

      if (loggedUser && foundEvent) {
        const fav = await isFavourite(
          loggedUser.id,
          foundEvent.id
        );
        setFavourite(fav);
      } else {
        setFavourite(false);
      }


      setLoading(false);
    };

    fetchEvent();
  }, [id, location.pathname]);


  const eventType = location.pathname.includes("/events/private")
    ? "PRIVATE"
    : "PUBLIC";

  const isPrivateEvent = location.pathname.includes("/events/private");


  const handleFavouriteClick = async () => {
  if (!loggedUser || !event) return;

  try {
    if (favourite) {
      await removeFavouriteEvent(
        loggedUser.id,
        event.id
      );

      alert("Događaj je uklonjen iz omiljenih ❤️");
    } else {
      const success = await addFavouriteEvent(
        loggedUser.id,
        event.id
      );

      if (!success) {
        alert("Događaj je već u omiljenim");
        return;
      }

      alert("Događaj je dodat u omiljene ⭐");
    }

    setFavourite(!favourite);
  } catch (error) {
    alert("Greška pri komunikaciji sa serverom");
  }
};





  if (loading) {
    return (
      <div className="loader-center">
        <div className="loader"></div>
      </div>
    );
  }

  if (!event) {
    return <h2>Događaj nije pronađen</h2>;
  }

  return (
    <div className="ed-page">
      <div className="ed-hero">
        <div className="ed-content">

          <div className="ed-left">
            <h1 className="ed-title">
              {event.naziv}
              {canFavourite && !isPrivateEvent &&(
                <span
                  className={`ed-heart ${favourite ? "active" : ""}`}
                  onClick={handleFavouriteClick}
                >
                  {favourite ? "❤️" : "🤍"}
                </span>
              )}
            </h1>

            <p><strong>Opis:</strong> {event.opis}</p>
            <p><strong>Datum:</strong> {event.datum}</p>
            <p><strong>Lokacija:</strong> {event.lokacija}</p>

            {event.cena !== undefined && (
              <p>
                <strong>Cena:</strong>{" "}
                {event.cena === 0 ? "Besplatno" : `${event.cena} RSD`}
              </p>
            )}

            {category && (
              <p><strong>Kategorija:</strong> {category.naziv}</p>
            )}

            {event.user && (
              <p>
                <strong>Kreirao:</strong>{" "}
                {event.user.name} {event.user.surname}
              </p>
            )}

            {/* LINK ZA KUPVINU KARTE – SAMO ZA JAVNE DOGAĐAJE */}
            {event.sourceURL && (
              <p className="ed-ticket-link">
                Kartu za ovaj događaj možete kupiti{" "}
                <a
                  href={event.sourceURL}
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  ovde
                </a>
              </p>
            )}

          </div>

          <div className="ed-right">
            <img
              src={event.imageURL}
              alt={event.naziv}
              className="ed-image"
            />
          </div>

        </div>
      </div>
    </div>
  );
}

export default EventDetails;

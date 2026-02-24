import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/favouriteSection.css";

function FavouriteEventsSection() {
  const navigate = useNavigate();
  const user = JSON.parse(localStorage.getItem("loggedUser"));

  const [favourites, setFavourites] = useState([]);

  useEffect(() => {
    if (!user) return;

    const fetchFavourites = async () => {
      try {
        const res = await fetch(
          `/api/omiljeni/korisnik/${user.id}`
      );
        const data = await res.json();
        setFavourites(data);
      } catch (err) {
        console.error("Greška pri učitavanju omiljenih", err);
      }
    };

    fetchFavourites();
  }, [user]);

  if (!user || favourites.length === 0) return null;

  return (
    <div className="fav-section">
      <h2>Omiljeni događaji</h2>

      <div className="events-grid">
        {favourites.map(f => (
          <div
            key={`fav-${f.dogadjaj_id}`}
            className="event-card"
            onClick={() =>
              navigate(`/events/public/${f.dogadjaj_id}`)
            }
          >
            <div className="event-title">
              {f.dogadjaj.naziv}
            </div>

           
          </div>
        ))}
      </div>
    </div>
  );
}

export default FavouriteEventsSection;

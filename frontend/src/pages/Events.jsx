import { useEffect, useState } from "react";
import EventCard from "../components/eventCard.jsx";

function Events() {
  const [events, setEvents] = useState([]);

  useEffect(() => {
    // simulacija API poziva
    setTimeout(() => {
      setEvents([
        {
          id: 1,
          naziv: "Rock koncert",
          datum: "2026-03-12",
          lokacija: "Beogradska Arena"
        },
        {
          id: 2,
          naziv: "Pozorišna predstava",
          datum: "2026-03-20",
          lokacija: "Narodno pozorište"
        }
      ]);
    }, 1000);
  }, []);

  return (
    <>
      <h1>Events</h1>

      {events.length === 0 && <p>Učitavanje događaja...</p>}

      {events.map(event => (
        <EventCard key={event.id} event={event} />
      ))}
    </>
  );
}

export default Events;

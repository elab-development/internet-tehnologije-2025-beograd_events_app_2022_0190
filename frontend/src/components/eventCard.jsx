import Button from "./button.jsx";

function EventCard({ event }) {
  return (
    <div style={{ border: "1px solid #ccc", padding: "10px", margin: "10px" }}>
      <h3>{event.naziv}</h3>
      <p><strong>Datum:</strong> {event.datum}</p>
      <p><strong>Lokacija:</strong> {event.lokacija}</p>

      <Button
        text="Detalji"
        onClick={() => alert(`Detalji za: ${event.naziv}`)}
      />
    </div>
  );
}

export default EventCard;

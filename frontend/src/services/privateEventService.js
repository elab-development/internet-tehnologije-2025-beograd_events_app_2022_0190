const API_URL = "http://localhost:5000/api/privatni-dogadjaji";

/* SVI PRIVATNI */
export const getAllPrivateEvents = async () => {
  const res = await fetch(API_URL);
  return res.json();
};

/* JEDAN PRIVATNI */
export const getPrivateEventById = async (id) => {
  const res = await fetch(`${API_URL}/${id}`);
  return res.json();
};

/* KREIRANJE */
export const createPrivateEvent = async (data, user) => {
  if (!user) {
    return { success: false, message: "Morate biti prijavljeni" };
  }

  const res = await fetch(API_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      naziv: data.naziv,
      opis: data.opis,
      datum: data.datum,
      lokacija: data.lokacija,
      kapacitet: data.kapacitet,
      korisnik_id: user.id,
      imageURL:
        "https://alvasshowroom.com/wp-content/uploads/2018/08/Private-event-image.jpg"
    })
  });

  if (!res.ok) {
    return { success: false, message: "Greška pri kreiranju" };
  }

  return { success: true };
};

/* BRISANJE */
export const deletePrivateEvent = async (id) => {
  await fetch(`${API_URL}/${id}`, {
    method: "DELETE"
  });
};

/* AŽURIRANJE */
export const updatePrivateEvent = async (event) => {
  await fetch(`${API_URL}/${event.id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(event)
  });
};

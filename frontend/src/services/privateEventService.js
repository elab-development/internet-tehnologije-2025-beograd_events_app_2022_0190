const API_URL = `https://internet-tehnologije-2025-beogradeventsapp202-production.up.railway.app/api/privatni-dogadjaji`;
export const getAllPrivateEvents = async () => {
  const res = await fetch(API_URL);
  return await res.json();
};

export const getPrivateEventById = async (id) => {
  const res = await fetch(`${API_URL}/${id}`);
  return await res.json();
};

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
    }),
  });

  return { success: res.ok };
};

export const deletePrivateEvent = async (id) => {
  await fetch(`${API_URL}/${id}`, { method: "DELETE" });
};

export const updatePrivateEvent = async (event) => {
  await fetch(`${API_URL}/${event.id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(event),
  });
};

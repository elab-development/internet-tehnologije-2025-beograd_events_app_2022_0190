const API_URL = "http://localhost:5000/api/omiljeni";

/**
 * ✅ Provera da li je događaj u omiljenim (iz baze)
 */
export const isFavourite = async (korisnikId, dogadjajId) => {
  const response = await fetch(
    `${API_URL}/${korisnikId}/${dogadjajId}`
  );

  return response.ok;
};

/**
 * ⭐ Dodavanje u omiljene (baza)
 */
export const addFavouriteEvent = async (korisnikId, dogadjajId) => {
  const response = await fetch(API_URL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      korisnik_id: korisnikId,
      dogadjaj_id: dogadjajId,
    }),
  });

  return response.ok;
};

/**
 * ❌ Uklanjanje iz omiljenih (baza)
 */
export const removeFavouriteEvent = async (korisnikId, dogadjajId) => {
  const response = await fetch(
    `${API_URL}/${korisnikId}/${dogadjajId}`,
    {
      method: "DELETE",
    }
  );

  return response.ok;
};

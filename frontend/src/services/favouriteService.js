const API_URL = `https://internet-tehnologije-2025-beogradeventsapp202-production.up.railway.app/api/omiljeni`;
export const isFavourite = async (korisnikId, dogadjajId) => {
  const response = await fetch(`${API_URL}/${korisnikId}/${dogadjajId}`);
  return response.ok;
};

export const addFavouriteEvent = async (korisnikId, dogadjajId) => {
  const response = await fetch(API_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      korisnik_id: korisnikId,
      dogadjaj_id: dogadjajId,
    }),
  });

  return response.ok;
};

export const removeFavouriteEvent = async (korisnikId, dogadjajId) => {
  const response = await fetch(
    `${API_URL}/${korisnikId}/${dogadjajId}`,
    { method: "DELETE" }
  );

  return response.ok;
};

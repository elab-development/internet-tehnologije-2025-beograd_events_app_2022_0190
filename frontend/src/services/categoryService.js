const API_URL = `https://internet-tehnologije-2025-beogradeventsapp202-production.up.railway.app/api/kategorije`;
export const getAllCategories = async () => {
  const response = await fetch(API_URL);
  return await response.json();
};

export const getCategoryById = async (id) => {
  const response = await fetch(`${API_URL}/${id}`);
  return await response.json();
};

export const createCategory = async (naziv) => {
  const response = await fetch(API_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ naziv }),
  });

  return response.ok;
};

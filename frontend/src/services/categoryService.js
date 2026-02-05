const API_URL = "http://localhost:5000/api/kategorije";


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
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ naziv }),
  });

  if (!response.ok) {
    return { success: false, message: "Greška pri dodavanju kategorije" };
  }

  return { success: true };
};

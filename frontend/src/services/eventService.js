const API_URL = `${process.env.REACT_APP_API_URL}/api/dogadjaji`;

export const getAllEvents = async () => {
  try {
    const response = await fetch(API_URL);
    return await response.json();
  } catch (error) {
    console.error("Greška:", error);
    return [];
  }
};

export const getEventById = async (id) => {
  try {
    const response = await fetch(`${API_URL}/${id}`);
    return await response.json();
  } catch (error) {
    console.error("Greška:", error);
    return null;
  }
};

export const createEvent = async (event) => {
  const response = await fetch(API_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(event),
  });

  return response.ok;
};

const KEY = "privateEvents";

const getAll = () => {
  return JSON.parse(localStorage.getItem(KEY)) || [];
};

export const getPrivateEventsForUser = (user) => {
    if (!user) return [];
  
    const events = JSON.parse(localStorage.getItem("privateEvents")) || [];
  
    // ❌ admin nema posebna prava
    return events.filter(
      e => e.user && e.user.email === user.email
    );
  };
  
  

export const createPrivateEvent = (data, user) => {
  if (!user) {
    return { success: false, message: "Morate biti prijavljeni" };
  }

  const events = getAll();

  const newEvent = {
    id: events.length ? Math.max(...events.map(e => e.id)) + 1 : 1,
    ...data,
    imageURL:
      "https://alvasshowroom.com/wp-content/uploads/2018/08/Private-event-image.jpg",
    user: {
      name: user.name,
      surname: user.surname,
      email: user.email
    },
    eventType: "PRIVATE" // 👈 KLJUČNA LINIJA
  };
  

  events.push(newEvent);
  localStorage.setItem(KEY, JSON.stringify(events));

  return { success: true };
};

export const deletePrivateEvent = (id, user) => {
    if (!user) return;
  
    const events = JSON.parse(localStorage.getItem("privateEvents")) || [];
    const event = events.find(e => e.id === id);
  
    // ❌ samo kreator
    if (!event || event.user.email !== user.email) return;
  
    const filtered = events.filter(e => e.id !== id);
    localStorage.setItem("privateEvents", JSON.stringify(filtered));
  };
  

  export const updatePrivateEvent = (updatedEvent, user) => {
    const events = JSON.parse(localStorage.getItem("privateEvents")) || [];
    const index = events.findIndex(e => e.id === updatedEvent.id);
  
    if (index === -1) return;
  
    // ❌ samo kreator
    if (events[index].user.email !== user.email) return;
  
    events[index] = updatedEvent;
    localStorage.setItem("privateEvents", JSON.stringify(events));
  };
  
export const getAllPrivateEvents = () => {
    return JSON.parse(localStorage.getItem("privateEvents")) || [];
  };
  export const getPrivateEventById = (id) => {
    const events = JSON.parse(localStorage.getItem("privateEvents")) || [];
    return events.find(e => e.id === Number(id));
  };
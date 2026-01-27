const KEY = "favouriteEvents";

const getAll = () => {
  return JSON.parse(localStorage.getItem(KEY)) || {};
};

// ✅ PROVERA OMILJENOG
export const isFavourite = (userEmail, eventId, eventType) => {
  const data = getAll();
  const type = eventType ?? "PUBLIC";

  return data[userEmail]?.some(
    f => f.eventId === eventId && f.eventType === type
  );
};

// ⭐ DODAVANJE OMILJENOG
export const addFavouriteEvent = (userEmail, event) => {
  const data = getAll();

  if (!data[userEmail]) {
    data[userEmail] = [];
  }

  const eventType = event.eventType ?? "PUBLIC";

  // ⛔ spreči duplikate
  if (
    data[userEmail].some(
      f => f.eventId === event.id && f.eventType === eventType
    )
  ) {
    return;
  }

  // 🗓 datum događaja (robustno)
  const rawDate =
    event.datum ||
    event.date ||
    event.data;

  let reminderDate = null;

  if (rawDate) {
    const [year, month, day] = rawDate.split("-").map(Number);
    const eventDate = new Date(year, month - 1, day);

    reminderDate = new Date(eventDate);
    reminderDate.setDate(eventDate.getDate() - 1);
  }

  data[userEmail].push({
    eventId: event.id,
    eventType,
    podsetnik: reminderDate
      ? reminderDate.toISOString().split("T")[0]
      : null
  });

  localStorage.setItem(KEY, JSON.stringify(data));
};

// ❌ UKLANJANJE OMILJENOG
export const removeFavouriteEvent = (userEmail, eventId, eventType) => {
  const data = getAll();
  const type = eventType ?? "PUBLIC";

  if (!data[userEmail]) return;

  data[userEmail] = data[userEmail].filter(
    f => !(f.eventId === eventId && f.eventType === type)
  );

  localStorage.setItem(KEY, JSON.stringify(data));
};

const EVENTS_KEY = "events";


const initialEvents = [
  {
    id: 1,
    naziv: "Koncert Bijelog Dugmeta",
    opis: "Legendarni koncert u Štark Areni.",
    datum: "2026-03-15",
    lokacija: "Štark Arena, Beograd",
    cena: 4500,
    categoryId: 1,
    imageURL: "https://images.pexels.com/photos/2486168/pexels-photo-2486168.jpeg",
    sourceURL: "https://tickets.rs"
  },
  {
    id: 2,
    naziv: "Pozorišna predstava Hamlet",
    opis: "Klasik Vilijama Šekspira u modernoj interpretaciji.",
    datum: "2026-02-10",
    lokacija: "Narodno pozorište",
    cena: 1800,
    categoryId: 2,
    imageURL: "https://images.pexels.com/photos/2486168/pexels-photo-2486168.jpeg",
    sourceURL: "https://narodnopozoriste.rs"
  },
  {
    id: 3,
    naziv: "Beogradski maraton",
    opis: "Tradicionalna sportska manifestacija.",
    datum: "2026-04-20",
    lokacija: "Centar Beograda",
    cena: 0,
    categoryId: 3,
    imageURL: "https://images.pexels.com/photos/2486168/pexels-photo-2486168.jpeg",
    sourceURL: "https://bgmarathon.org"
  },
  {
    id: 4,
    naziv: "Festival vina",
    opis: "Degustacija domaćih i stranih vina.",
    datum: "2026-05-05",
    lokacija: "Kalemegdan",
    cena: 2500,
    categoryId: 4,
    imageURL: "https://images.pexels.com/photos/2486168/pexels-photo-2486168.jpeg",
    sourceURL: "https://winefest.rs"
  },

  {
    id: 5,
    naziv: "Festival vina",
    opis: "Degustacija domaćih i stranih vina.",
    datum: "2026-05-05",
    lokacija: "Kalemegdan",
    cena: 2500,
    categoryId: 4,
    imageURL: "https://images.pexels.com/photos/2486168/pexels-photo-2486168.jpeg",
    sourceURL: "https://winefest.rs"
  },

  {
    id: 6,
    naziv: "Festival vina",
    opis: "Degustacija domaćih i stranih vina.",
    datum: "2026-05-05",
    lokacija: "Kalemegdan",
    cena: 2500,
    categoryId: 4,
    imageURL: "https://images.pexels.com/photos/2486168/pexels-photo-2486168.jpeg",
    sourceURL: "https://winefest.rs"
  }
];



const initEvents = () => {
  localStorage.setItem(EVENTS_KEY, JSON.stringify(initialEvents));
};

initEvents();



const API_URL = "http://localhost:5000/api/dogadjaji";

export const getAllEvents = async () => {
  const response = await fetch("http://localhost:5000/api/dogadjaji");
  return response.json();
};



export const getEventById = async(id) => {
  const response = await fetch("http://localhost:5000/api/dogadjaji/"+id);
  return response.json();
};



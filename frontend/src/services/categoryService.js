const CATEGORY_KEY = "categories";

/**
 * Inicijalne kategorije (mock)
 */
const initialCategories = [
  { id: 1, naziv: "Koncert" },
  { id: 2, naziv: "Pozorište" },
  { id: 3, naziv: "Sport" },
  { id: 4, naziv: "Festival" }
];

/**
 * Init kategorija (poziva se jednom)
 */
const initCategories = () => {
  const categories = JSON.parse(localStorage.getItem(CATEGORY_KEY));
  if (!categories) {
    localStorage.setItem(
      CATEGORY_KEY,
      JSON.stringify(initialCategories)
    );
  }
};

initCategories();

/**
 * Vraća sve kategorije
 */
export const getAllCategories = () => {
  return JSON.parse(localStorage.getItem(CATEGORY_KEY)) || [];
};

export const getCategoryById = (id) => {
    const categories = getAllCategories();
    return categories.find(c => c.id === Number(id));
  };
  
  
  

/**
 * Kreira novu kategoriju
 */
export const createCategory = (naziv) => {
  if (!naziv || naziv.trim().length < 3) {
    return { success: false, message: "Naziv mora imati bar 3 karaktera" };
  }

  const categories = getAllCategories();

  const newCategory = {
    id: categories.length
      ? Math.max(...categories.map(c => c.id)) + 1
      : 1,
    naziv: naziv.trim()
  };

  categories.push(newCategory);
  localStorage.setItem(CATEGORY_KEY, JSON.stringify(categories));

  return { success: true };
};

/**
 * Ažuriranje kategorije
 */
export const updateCategory = (id, newName) => {
  if (!newName || newName.trim().length < 3) {
    return { success: false, message: "Naziv mora imati bar 3 karaktera" };
  }

  const categories = getAllCategories();
  const category = categories.find(c => c.id === id);

  if (!category) {
    return { success: false, message: "Kategorija ne postoji" };
  }

  category.naziv = newName.trim();
  localStorage.setItem(CATEGORY_KEY, JSON.stringify(categories));

  return { success: true };
};

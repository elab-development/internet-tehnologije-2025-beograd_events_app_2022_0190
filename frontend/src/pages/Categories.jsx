import { useEffect, useState } from "react";
import {
  getAllCategories,
  createCategory
} from "../services/categoryService.js";
import "../styles/categories.css";

function Categories() {
  const [categories, setCategories] = useState([]);
  const [search, setSearch] = useState("");
  const [showForm, setShowForm] = useState(false);
  const [newCategory, setNewCategory] = useState("");

  const loggedUser = JSON.parse(localStorage.getItem("loggedUser"));

  useEffect(() => {
    const fetchCategories = async () => {
      const data = await getAllCategories();
      setCategories(data);
    };

    fetchCategories();
  }, []);

  if (!loggedUser || loggedUser.uloga !== "ADMIN") {
    return <h2>Nemate pravo pristupa ovoj stranici</h2>;
  }

  const filteredCategories = categories.filter(c =>
    c.naziv.toLowerCase().includes(search.toLowerCase())
  );

  const handleCreate = async () => {
    const result = await createCategory(newCategory);

    if (!result.success) {
      alert(result.message);
      return;
    }

    const refreshed = await getAllCategories();
    setCategories(refreshed);

    setNewCategory("");
    setShowForm(false);
  };

  return (
    <div className="categories-page">

      <h1 className="categories-title">Kategorije događaja</h1>

      <div className="categories-toolbar">
        <input
          type="text"
          placeholder="Pretraga po nazivu..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />

        <button onClick={() => setShowForm(!showForm)}>
          ➕ Dodaj kategoriju
        </button>
      </div>

      {showForm && (
        <div className="category-form">
          <input
            type="text"
            placeholder="Naziv kategorije"
            value={newCategory}
            onChange={(e) => setNewCategory(e.target.value)}
          />
          <button onClick={handleCreate}>Sačuvaj</button>
        </div>
      )}

      <div className="categories-list">
        {filteredCategories.map((category, index) => (
          <div
            key={category.id}
            className="category-card"
            style={{ animationDelay: `${index * 0.08}s` }}
          >
            {category.naziv}
          </div>
        ))}
      </div>

    </div>
  );
}

export default Categories;

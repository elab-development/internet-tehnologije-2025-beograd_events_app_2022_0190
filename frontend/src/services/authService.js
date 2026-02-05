const ADMIN_EMAIL = "admin@test.com";
const ADMIN_PASSWORD = "admin123";

const initUsers = () => {
  let users = JSON.parse(localStorage.getItem("users")) || [];
  
  const adminExists = users.some(
    u => u.email === ADMIN_EMAIL && u.uloga === "ADMIN"
  );

  if (!adminExists) {
    users.push({
      name: "Admin",
      surname: "Admin",
      email: ADMIN_EMAIL,
      password: ADMIN_PASSWORD,
      uloga: "ADMIN"
    });

    localStorage.setItem("users", JSON.stringify(users));
  }
};



const API_URL = "http://localhost:5000/api/korisnici";


export const registerUser = async (user) => {
  try {
    const response = await fetch(`${API_URL}/register`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        ime: user.name,
        prezime: user.surname,
        email: user.email,
        lozinka: user.password,
      }),
    });

    const data = await response.json(); 

    if (!response.ok) {
      return { 
        success: false, 
        message: data.poruka || "Greška pri registraciji" 
      };
    }

    return { 
      success: true, 
      message: data.poruka 
    };

  } catch (error) {
    return { 
      success: false, 
      message: "Backend nije dostupan" 
    };
  }
};


export const loginUser = async (email, password) => {
  try {
    const response = await fetch(`${API_URL}/login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        email: email,
        lozinka: password,
      }),
    });

    const data = await response.json();

    if (!response.ok) {
      return {
        success: false,
        message: data.poruka, 
      };
    }

    localStorage.setItem("loggedUser", JSON.stringify(data.korisnik));

    return {
      success: true,
      message: data.poruka,
    };

  } catch (error) {
    return {
      success: false,
      message: "Backend nije dostupan",
    };
  }
};



export const logoutUser = () => {
  localStorage.removeItem("loggedUser");
};

// 🔑 DEMO ADMIN PODACI
const ADMIN_EMAIL = "admin@test.com";
const ADMIN_PASSWORD = "admin123";

// ✅ inicijalizacija "baze"
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

// POZIVAMO ODMAH
//initUsers();

// export const registerUser = (user) => {
//   const users = JSON.parse(localStorage.getItem("users")) || [];

//   const userExists = users.find(u => u.email === user.email);
//   if (userExists) {
//     return { success: false, message: "Email već postoji!" };
//   }

//   users.push({
//     ...user,
//     uloga: "REGISTROVANI"
//   });

//   localStorage.setItem("users", JSON.stringify(users));

//   return { success: true };
// };

// export const loginUser = (email, password) => {
//   const users = JSON.parse(localStorage.getItem("users")) || [];

//   const user = users.find(
//     u => u.email === email && u.password === password
//   );

//   if (!user) {
//     return { success: false, message: "Pogrešan email ili lozinka" };
//   }

//   localStorage.setItem("loggedUser", JSON.stringify(user));
//   return { success: true };
// };

// export const logoutUser = () => {
//   localStorage.removeItem("loggedUser");
// };

const API_URL = "http://localhost:5000/api/korisnici";

/**
 * REGISTRACIJA – upis u bazu
 */
export const registerUser = async (user) => {
  try {
    const response = await fetch(API_URL, {
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

    if (!response.ok) {
      return { success: false, message: "Greška pri registraciji" };
    }

    return { success: true };
  } catch (error) {
    return { success: false, message: "Backend nije dostupan" };
  }
};

/**
 * LOGIN – proveravamo korisnika iz baze
 */
export const loginUser = async (email, password) => {
  try {
    const response = await fetch(API_URL);
    const users = await response.json();

    const user = users.find(
      (u) => u.email === email
    );

    if (!user) {
      return { success: false, message: "Pogrešan email ili lozinka" };
    }

    // ⚠️ trenutno NEMAŠ backend login,
    // zato ovo ostaje privremeno:
    localStorage.setItem("loggedUser", JSON.stringify(user));

    return { success: true };
  } catch (error) {
    return { success: false, message: "Backend nije dostupan" };
  }
};

export const logoutUser = () => {
  localStorage.removeItem("loggedUser");
};

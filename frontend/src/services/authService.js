const API_URL = `${process.env.REACT_APP_API_URL}/api/dogadjaji`;

export const registerUser = async (user) => {
  try {
    const response = await fetch(`${API_URL}/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        ime: user.name,
        prezime: user.surname,
        email: user.email,
        lozinka: user.password,
      }),
    });

    const data = await response.json();

    if (!response.ok) {
      return { success: false, message: data.poruka };
    }

    return { success: true, message: data.poruka };

  } catch {
    return { success: false, message: "Backend nije dostupan" };
  }
};

export const loginUser = async (email, password) => {
  try {
    const response = await fetch(`${API_URL}/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        email,
        lozinka: password,
      }),
    });

    const data = await response.json();

    if (!response.ok) {
      return { success: false, message: data.poruka };
    }

    localStorage.setItem("token", data.access_token);
    localStorage.setItem("loggedUser", JSON.stringify(data.korisnik));

    return { success: true };

  } catch {
    return { success: false, message: "Backend nije dostupan" };
  }
};

export const logoutUser = () => {
  localStorage.removeItem("token");
  localStorage.removeItem("loggedUser");
};

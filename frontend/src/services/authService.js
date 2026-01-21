export const registerUser = (user) => {
    const users = JSON.parse(localStorage.getItem("users")) || [];
  
    const userExists = users.find(u => u.email === user.email);
    if (userExists) {
      return { success: false, message: "Email već postoji!" };
    }
  
    users.push(user);
    localStorage.setItem("users", JSON.stringify(users));
  
    return { success: true };
  };
  
  export const loginUser = (email, password) => {
    const users = JSON.parse(localStorage.getItem("users")) || [];
  
    const user = users.find(
      u => u.email === email && u.password === password
    );
  
    if (!user) {
      return { success: false, message: "Pogrešan email ili lozinka" };
    }
  
    localStorage.setItem("loggedUser", JSON.stringify(user));
    return { success: true };
  };
  
  export const logoutUser = () => {
    localStorage.removeItem("loggedUser");
  };
  
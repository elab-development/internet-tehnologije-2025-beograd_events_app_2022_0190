import { useState } from "react";
import "../styles/usersPage.css";
import UserPanel from "../components/UserPanel";

function UsersPage() {
  const [users, setUsers] = useState(
    JSON.parse(localStorage.getItem("users")) || []
  );

  const refreshUsers = () => {
    setUsers(JSON.parse(localStorage.getItem("users")) || []);
  };

  return (
    <div className="users-page">
      <h1 className="users-title">Korisnički nalozi</h1>

      {users.map((user, index) => (
        <UserPanel
          key={index}
          user={user}
          onUpdate={refreshUsers}
        />
      ))}
    </div>
  );
}

export default UsersPage;

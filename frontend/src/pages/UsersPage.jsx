import { useEffect, useState } from "react";
import "../styles/usersPage.css";
import UserPanel from "../components/UserPanel";

function UsersPage() {
  const [users, setUsers] = useState([]);

  const fetchUsers = async () => {
    const response = await fetch(`${process.env.REACT_APP_API_URL}/korisnici`);
    const data = await response.json();
    setUsers(data);
  };

  useEffect(() => {
    fetchUsers();
  }, []);

  const refreshUsers = () => {
    fetchUsers(); 
  };

  return (
    <div className="users-page">
      <h1 className="users-title">Korisnički nalozi</h1>

      {users.map((user) => (
        <UserPanel
          key={user.id}
          user={user}
          onUpdate={refreshUsers}
        />
      ))}
    </div>
  );
}

export default UsersPage;

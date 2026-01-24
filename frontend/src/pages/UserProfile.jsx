import { useState } from "react";
import "../styles/userProfile.css";
import avatar from "../assets/avatar.jpg";
import ResetPasswordModal from "../components/ResetPasswordModal";
import FavouriteEventsSection from "../components/FavouriteEventsSection";

function UserProfile() {
  const user = JSON.parse(localStorage.getItem("loggedUser"));
  const [showReset, setShowReset] = useState(false);

  if (!user) return <h2>Niste prijavljeni</h2>;

  return (
    <div className="up-page">
      <div className="up-card">
        <img src={avatar} className="up-avatar" alt="avatar" />

        <div className="up-field">
          <label>Ime</label>
          <input value={user.name} disabled />
        </div>

        <div className="up-field">
          <label>Prezime</label>
          <input value={user.surname} disabled />
        </div>

        <div className="up-field">
          <label>Email</label>
          <input value={user.email} disabled />
        </div>

        <div className="up-field">
          <label>Uloga</label>
          <input value={user.uloga} disabled />
        </div>

        <span
          className="up-reset-link"
          onClick={() => setShowReset(true)}
        >
          Resetuj lozinku
        </span>
      </div>

      <FavouriteEventsSection />

      {showReset && (
        <ResetPasswordModal onClose={() => setShowReset(false)} />
      )}
    </div>
  );
}

export default UserProfile;

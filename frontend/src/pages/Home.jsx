import { useNavigate } from "react-router-dom";
import { logoutUser } from "../services/authService";

function Home() {
  const navigate = useNavigate();

  return (
    <div>
      <h1>Početna stranica</h1>

      <button
        onClick={() => {
          logoutUser();
          navigate("/");
        }}
      >
        Odjavi se
      </button>
    </div>
  );
}

export default Home;

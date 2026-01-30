import { BrowserRouter, Routes, Route, useLocation } from "react-router-dom";
import Navbar from "./components/navbar.jsx";
import Home from "./pages/Home.jsx";
import Login from "./pages/Login.jsx";
import Register from "./pages/Register.jsx";
import EventDetails from "./pages/EventDetails.jsx";
import Categories from "./pages/Categories.jsx";
import PrivateEvents from "./pages/privateEvent.jsx";
import UserProfile from "./pages/UserProfile";
import UsersPage from "./pages/UsersPage";
import Footer from "./components/Footer.jsx";


function AppContent() {
  const location = useLocation();

  const hideNavbar =
    location.pathname === "/" ||
    location.pathname === "/register";

  return (
    <>
      {!hideNavbar && <Navbar />}

      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/home" element={<Home />} />
        <Route path="/events/:id" element={<EventDetails />} />
        <Route path="/categories" element={<Categories />} />
        <Route path="/private-events" element={<PrivateEvents />} />
        <Route path="/events/public/:id" element={<EventDetails />} />
<Route path="/events/private/:id" element={<EventDetails />} />
<Route path="/user" element={<UserProfile />} />
<Route path="/users" element={<UsersPage />} />


      </Routes>
       {!hideLayout && <Footer />}
    </>
  );
}

function App() {
  return (
    <BrowserRouter>
      <AppContent />
    </BrowserRouter>
  );
}

export default App;

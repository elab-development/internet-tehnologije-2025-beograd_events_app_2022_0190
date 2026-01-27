import "../styles/button.css";


function Button({ text, onClick, type = "button" }) {
  return (
    <button
      type={type}
      onClick={onClick}
      className="app-button"
    >
      {text}
    </button>
  );
}

export default Button;

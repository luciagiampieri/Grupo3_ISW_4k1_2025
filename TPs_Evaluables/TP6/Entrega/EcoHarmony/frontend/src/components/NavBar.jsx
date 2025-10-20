import "./NavBar.css";
import logo from "../assets/logo.png"; // reemplazá por tu archivo

export default function NavBar() {
  return (
    <>
      <header className="navbar">
        <div className="nav-inner">
          <h2>EcoHarmony</h2>
          <img src={logo} alt="Logo" className="nav-logo" />
        </div>
      </header>
      {/* Espaciador para que el contenido no quede debajo de la navbar fija */}
      <div className="navbar-spacer" />
    </>
  );
}

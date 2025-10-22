import "./NavBar.css";
import logo from "../assets/logo.png";

import { Link } from 'react-router-dom';

export default function NavBar() {
  return (
    <>
      <nav className="navbar">
        <div className="nav-inner">
          <div className="nav-brand">
            <img src={logo} alt="EcoHarmony Logo" className="nav-logo" />
            <h2 className="nav-title">EcoHarmony</h2>
          </div>

          <div className="nav-links">
            <Link to="/">Inicio</Link>
            <Link to="/form">Comprar</Link>
          </div>
        </div>
      </nav>

      <div className="navbar-spacer" />
    </>
  );
}

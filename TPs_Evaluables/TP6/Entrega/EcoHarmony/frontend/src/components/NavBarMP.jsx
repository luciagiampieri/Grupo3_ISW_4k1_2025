import "./NavBarMP.css";
import mpLogo from "../assets/mercadopago_bg_removed_outer.png";

export default function NavBarMP() {
  return (
    <nav className="navbar-mp">
      <div className="navbar-mp-content">
        <img
          src={mpLogo}
          alt="Mercado Pago"
          className="navbar-mp-logo"
        />
      </div>
    </nav>
  );
}

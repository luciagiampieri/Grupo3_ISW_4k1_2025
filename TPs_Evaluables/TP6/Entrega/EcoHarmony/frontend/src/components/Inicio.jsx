import './Inicio.css';
import logo from '../assets/parque.png';
import { Link } from 'react-router-dom';

export default function Inicio() {
      return (
      <main className="inicio-container">
            <section className="inicio-hero">
            <div className="inicio-texto">
            <h1>Bienvenido a <span>EcoHarmony Park</span> 🌱</h1>
            <p>
                  Descubrí la magia de la naturaleza en su máximo esplendor. <br />
                  Explorá nuestras exhibiciones, conocé a los animales y disfrutá de
                  actividades únicas pensadas para toda la familia.
            </p>

            <Link to="/form" className="home-button">
                  Comprar Entradas
            </Link>
            </div>
            </section>
      </main>
      );
}

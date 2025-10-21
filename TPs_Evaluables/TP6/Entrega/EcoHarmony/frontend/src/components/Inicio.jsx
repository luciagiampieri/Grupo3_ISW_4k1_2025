import './Inicio.css';
import logo from '../assets/parque.png';

export default function Inicio() {
      return (
            <main className="inicio-container">
                  <section className="inicio-hero">
                        <img src={logo} alt="EcoHarmony logo" className="inicio-logo" />
                        <h1>Bienvenido a EcoHarmony Park</h1>
                        <p>
                              Descubrí la magia de la naturaleza en su máximo esplendor.
                              <br /> Explorá nuestras exhibiciones, conocé los animales y disfrutá
                              de actividades únicas pensadas para toda la familia.
                        </p>

                  <a href="/" className="home-button">
                        Comprar Entradas
                  </a>
      </section>
      </main>
);
}

import { BrowserRouter as Router, Routes, Route, useLocation } from 'react-router-dom'
import './App.css'
import SimpleForm from './components/SimpleForm.jsx'
import PurchaseDetail from './components/PurchaseDetail.jsx'
import NavBar from './components/NavBar.jsx'
import NavBarMP from './components/NavBarMP.jsx'
import FakeMercadoPago from './components/FakeMercadoPago.jsx'
import Inicio from './components/Inicio.jsx'

function AppContent() {
  const location = useLocation();
  const isMercadoPago = location.pathname === '/fakemercadopago';

  return (
    <>
      {isMercadoPago ? <NavBarMP /> : <NavBar />}
      <Routes>
        <Route path="/" element={<Inicio />} />
        <Route path="/form" element={<SimpleForm />} />
        <Route path="/detalle-compra" element={<PurchaseDetail />} />
        <Route path="/fakemercadopago" element={<FakeMercadoPago />} />
      </Routes>
    </>
  );
}

function App() {
  return (
    <Router>
      <AppContent />
    </Router>
  )
}

export default App

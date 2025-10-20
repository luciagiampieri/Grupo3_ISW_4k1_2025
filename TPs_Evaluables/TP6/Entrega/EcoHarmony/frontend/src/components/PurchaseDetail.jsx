import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "./PurchaseDetail.css";

export default function PurchaseDetail() {
  const navigate = useNavigate();
  const [detalles, setDetalles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [purchaseData, setPurchaseData] = useState(null);

  useEffect(() => {
    // Cargar los datos desde sessionStorage
    const storedData = sessionStorage.getItem('purchaseData');
    if (!storedData) {
      setError("No hay datos de compra disponibles");
      setLoading(false);
      return;
    }

    try {
      const data = JSON.parse(storedData);
      setPurchaseData(data);
      setDetalles(data.detalles || []);
      setLoading(false);
    } catch (err) {
      setError("Error al cargar los detalles de la compra");
      setLoading(false);
    }
  }, []);

  const formatearPrecio = (precio) => {
    return new Intl.NumberFormat("es-AR", {
      style: "currency",
      currency: "ARS",
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(precio);
  };

  if (loading) {
    return (
      <div className="detail-wrapper">
        <div className="card">
          <p>Cargando detalles...</p>
        </div>
      </div>
    );
  }

  if (error || !purchaseData) {
    return (
      <div className="detail-wrapper">
        <div className="card">
          <p className="err">{error || "No hay datos de compra"}</p>
          <button className="btn" onClick={() => navigate('/')}>
            Volver
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="detail-wrapper">
      <div className="card detail-card">
        <h1>✓ Compra Confirmada</h1>
        
        <div className="detail-section">
          <h2>Información General</h2>
          <div className="info-grid">
            <div className="info-item">
              <span className="label">Email:</span>
              <span className="value">{purchaseData.usuario_email}</span>
            </div>
            <div className="info-item">
              <span className="label">Fecha de visita:</span>
              <span className="value">{new Date(purchaseData.fecha_visita + "T00:00:00").toLocaleDateString("es-AR")}</span>
            </div>
            <div className="info-item">
              <span className="label">Forma de pago:</span>
              <span className="value">{purchaseData.forma_pago_nombre === "tarjeta" ? "Tarjeta" : "Efectivo"}</span>
            </div>
          </div>
        </div>

        <div className="detail-section">
          <h2>Entradas Compradas</h2>
          <div className="tickets-list">
            {detalles.map((detalle, index) => {
              const edad = detalle.edad_visitante;
              const tipo = detalle.tipo_entrada_nombre;
              const precio = detalle.precio || 0; // Usar el precio que viene del cálculo original

              return (
                <div key={index} className="ticket-item">
                  <div className="ticket-number">Entrada #{index + 1}</div>
                  <div className="ticket-details">
                    <div className="ticket-info">
                      <span className="ticket-label">Edad:</span>
                      <span className="ticket-value">{edad} años</span>
                    </div>
                    <div className="ticket-info">
                      <span className="ticket-label">Tipo:</span>
                      <span className="ticket-value ticket-type">{tipo === "vip" ? "VIP" : "Regular"}</span>
                    </div>
                    <div className="ticket-info">
                      <span className="ticket-label">Precio:</span>
                      <span className="ticket-value ticket-price">{formatearPrecio(precio)}</span>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        <div className="total-section">
          <div className="total-row">
            <span className="total-label">Total:</span>
            <span className="total-value">{formatearPrecio(purchaseData.total || 0)}</span>
          </div>
        </div>

        <div className="detail-actions">
          <button className="btn btn-primary" onClick={() => {
            sessionStorage.removeItem('purchaseData');
            navigate('/');
          }}>
            Nueva Compra
          </button>
        </div>

        <div className="detail-note">
          <p>
            <strong>Importante:</strong> Presentá este comprobante el día de tu visita.
            Recibirás un email de confirmación en {purchaseData.usuario_email}.
          </p>
        </div>
      </div>
    </div>
  );
}

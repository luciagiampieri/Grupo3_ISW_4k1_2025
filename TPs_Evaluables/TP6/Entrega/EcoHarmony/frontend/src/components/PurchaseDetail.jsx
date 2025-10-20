import { useState, useEffect } from "react";
import "./PurchaseDetail.css";

export default function PurchaseDetail({ purchaseData, onBack }) {
  const [detalles, setDetalles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Cargar los detalles de la compra desde el backend
    const fetchDetalles = async () => {
      try {
        // Aquí puedes hacer una llamada a la API para obtener los detalles completos
        // Por ahora, usamos los datos que ya tenemos
        setDetalles(purchaseData.detalles || []);
        setLoading(false);
      } catch (err) {
        setError("Error al cargar los detalles de la compra");
        setLoading(false);
      }
    };

    fetchDetalles();
  }, [purchaseData]);

  const calcularPrecioTotal = () => {
    let total = 0;
    detalles.forEach((detalle) => {
      const edad = detalle.edad_visitante;
      const tipo = detalle.tipo_entrada_nombre;
      
      // Lógica de precios (ajusta según tu backend)
      let precio = 0;
      if (tipo === "regular") {
        if (edad < 12) precio = 5000;
        else if (edad >= 65) precio = 8000;
        else precio = 10000;
      } else if (tipo === "vip") {
        if (edad < 12) precio = 8000;
        else if (edad >= 65) precio = 12000;
        else precio = 15000;
      }
      total += precio;
    });
    return total;
  };

  const formatearPrecio = (precio) => {
    return new Intl.NumberFormat("es-AR", {
      style: "currency",
      currency: "ARS",
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

  if (error) {
    return (
      <div className="detail-wrapper">
        <div className="card">
          <p className="err">{error}</p>
          <button className="btn" onClick={onBack}>
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
              
              let precio = 0;
              if (tipo === "regular") {
                if (edad < 12) precio = 5000;
                else if (edad >= 65) precio = 8000;
                else precio = 10000;
              } else if (tipo === "vip") {
                if (edad < 12) precio = 8000;
                else if (edad >= 65) precio = 12000;
                else precio = 15000;
              }

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
            <span className="total-value">{formatearPrecio(calcularPrecioTotal())}</span>
          </div>
        </div>

        <div className="detail-actions">
          <button className="btn btn-primary" onClick={onBack}>
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

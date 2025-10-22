import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import "./FakeMercadoPago.css";

export default function FakeMercadoPago() {
  const navigate = useNavigate();
  const [purchaseData, setPurchaseData] = useState(null);

  useEffect(() => {
    // Cargar los datos desde sessionStorage
    const storedData = sessionStorage.getItem('purchaseData');
    if (!storedData) {
      // Si no hay datos, redirigir al formulario
      navigate('/form');
      return;
    }
    setPurchaseData(JSON.parse(storedData));
  }, [navigate]);

  const handleConfirm = () => {
    // No eliminar los datos, redirigir al detalle de compra
    navigate('/detalle-compra');
  };

  const handleCancel = () => {
    sessionStorage.removeItem('purchaseData');
    navigate('/form');
  };

  if (!purchaseData) {
    return null; // Evita renderizar mientras redirige
  }

  const formatearPrecio = (precio) => {
    return new Intl.NumberFormat("es-AR", {
      style: "currency",
      currency: "ARS",
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(precio);
  };

  return (
    <div className="mp-wrapper">
      <div className="mp-container">
        <div className="mp-card">
          <div className="mp-header">
            <h1 className="mp-title">Confirmá tu compra</h1>
            <p className="mp-desc">
              Estás a punto de completar tu pago con <strong>tarjeta de crédito/débito</strong> de forma segura a través de Mercado Pago.
            </p>
          </div>

          <div className="mp-info-section">
            <h3>Resumen de tu compra</h3>
            <div className="mp-info-item">
              <span className="mp-info-label">Email:</span>
              <span className="mp-info-value">{purchaseData.usuario_email}</span>
            </div>
            <div className="mp-info-item">
              <span className="mp-info-label">Fecha de visita:</span>
              <span className="mp-info-value">
                {new Date(purchaseData.fecha_visita + "T00:00:00").toLocaleDateString("es-AR")}
              </span>
            </div>
            <div className="mp-info-item">
              <span className="mp-info-label">Cantidad de entradas:</span>
              <span className="mp-info-value">{purchaseData.detalles.length}</span>
            </div>
            <div className="mp-info-item">
              <span className="mp-info-label">Método de pago:</span>
              <span className="mp-info-value">Tarjeta (Mercado Pago)</span>
            </div>
            <div className="mp-info-item mp-total-item">
              <span className="mp-info-label">Total a pagar:</span>
              <span className="mp-info-value mp-total-value">{formatearPrecio(purchaseData.total || 0)}</span>
            </div>
          </div>

          <div className="mp-actions">
            <button className="mp-btn mp-btn-confirm" onClick={handleConfirm}>
              ✓ Confirmar pago
            </button>
            <button className="mp-btn mp-btn-cancel" onClick={handleCancel}>
              ✕ Cancelar
            </button>
          </div>

          <div className="mp-security-note">
            <p>
              🔒 <strong>Pago seguro:</strong> Tu información está protegida con encriptación de nivel bancario.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

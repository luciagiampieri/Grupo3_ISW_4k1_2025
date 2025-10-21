import { useEffect, useState, useMemo } from "react";
import { useNavigate } from "react-router-dom";
import "./SimpleForm.css";

// Cierra los LUNES (1) | 0=Dom, 1=Lun, ... 6=Sáb
const CLOSED_WEEKDAY = 1;

// --- Precios base (deben coincidir con la DB) ---
const TICKET_PRICES = {
  regular: 5000,
  vip: 10000,
};

// --- Lógica de descuento (replicada de detalleEntrada.py) ---
function calcularMontoDetalle(edadStr, pase) {
  // Estandariza a minúsculas (ej. "VIP" -> "vip")
  const precioBase = TICKET_PRICES[pase.toLowerCase()];
  if (!precioBase) return 0;

  const edad = Number(edadStr);
  // No calcula si la edad está vacía o es inválida
  if (isNaN(edad) || edadStr === "" || edad < 0 || edad > 121) {
    return null; // 'null' para mostrar "-" en lugar de $0
  }

  // Lógica de descuento: < 10 años o > 60 años pagan 50%
  if (edad < 10 || edad > 60) {
    return precioBase * 0.5;
  }
  return precioBase;
}

// --- Helper para formatear a pesos ARS ---
const formatCurrency = (value) => {
  if (value === null || value === undefined) return "—"; // Guion para edades inválidas
  return value.toLocaleString("es-AR", {
    style: "currency",
    currency: "ARS",
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  });
};

function isClosedHoliday(dateStr) {
  // Feriados fijos: 1 de enero y 25 de diciembre
  const d = new Date(dateStr + "T00:00:00");
  if (Number.isNaN(d.getTime())) return false;
  const m = d.getMonth() + 1; // 1..12
  const day = d.getDate();
  return (m === 1 && day === 1) || (m === 12 && day === 25);
}

function isOpenDay(dateStr) {
  const d = new Date(dateStr + "T00:00:00");
  if (Number.isNaN(d.getTime())) return false;
  const dow = d.getDay();
  return dow !== CLOSED_WEEKDAY && !isClosedHoliday(dateStr);
}

function isTodayOrFuture(dateStr) {
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  const d = new Date(dateStr + "T00:00:00");
  return d >= today;
}

export default function SimpleForm() {
  const navigate = useNavigate();
  const [cantidad, setCantidad] = useState(1);
  const [fecha, setFecha] = useState("");
  const [email, setEmail] = useState("");
  const [pago, setPago] = useState("efectivo"); // "efectivo" | "tarjeta"
  const [personas, setPersonas] = useState([{ edad: "", pase: "regular" }]);
  const [errors, setErrors] = useState({});
  const [okMsg, setOkMsg] = useState("");
  const [purchaseCompleted, setPurchaseCompleted] = useState(false);
  const [purchaseData, setPurchaseData] = useState(null);

  // --- MODIFICADO: Cálculo de precios y DESGLOSE con dinero ---
  const calculoPrecios = useMemo(() => {
    let total = 0;
    
    // Objeto para contar los tipos de entrada
    const summary = {
      regular_full: 0,
      regular_half: 0,
      vip_full: 0,
      vip_half: 0,
    };
    
    // 'detalles' será un array con el precio de cada persona
    const detalles = personas.map((p) => {
      const monto = calcularMontoDetalle(p.edad, p.pase);
      
      if (monto !== null) {
        total += monto; // Suma al total solo si es un monto válido
        
        // Lógica para el desglose
        const edad = Number(p.edad);
        const pase = p.pase.toLowerCase(); // "regular" o "vip"
        const hasDiscount = (edad < 10 || edad > 60);

        if (pase === 'regular') {
          if (hasDiscount) summary.regular_half++;
          else summary.regular_full++;
        } else if (pase === 'vip') {
          if (hasDiscount) summary.vip_half++;
          else summary.vip_full++;
        }
      }
      return monto;
    });

    // Convertir el objeto 'summary' en un array de strings legibles
    const breakdownLines = [];

    // --- Lógica para agregar los subtotales en ( ) ---
    if (summary.regular_full > 0) {
      const lineTotal = summary.regular_full * TICKET_PRICES.regular;
      breakdownLines.push(
        `${summary.regular_full} x Entrada Regular (${formatCurrency(lineTotal)})`
      );
    }
    if (summary.regular_half > 0) {
      const lineTotal = summary.regular_half * (TICKET_PRICES.regular * 0.5);
      breakdownLines.push(
        `${summary.regular_half} x Regular (50% OFF) (${formatCurrency(lineTotal)})`
      );
    }
    if (summary.vip_full > 0) {
      const lineTotal = summary.vip_full * TICKET_PRICES.vip;
      breakdownLines.push(
        `${summary.vip_full} x Entrada VIP (${formatCurrency(lineTotal)})`
      );
    }
    if (summary.vip_half > 0) {
      const lineTotal = summary.vip_half * (TICKET_PRICES.vip * 0.5);
      breakdownLines.push(
        `${summary.vip_half} x VIP (50% OFF) (${formatCurrency(lineTotal)})`
      );
    }

    return { total, detalles, breakdown: breakdownLines };
  }, [personas]); // Fin del useMemo


  // useEffect para 'cantidad'
  useEffect(() => {
    const num = Number(cantidad);

    if (cantidad !== "" && (!Number.isInteger(num) || num < 1 || num > 10)) {
      setErrors((prev) => ({
        ...prev,
        cantidad: "La cantidad debe ser entre 1 y 10.",
      }));
    } else {
      setErrors((prev) => {
        const newErrors = { ...prev };
        delete newErrors.cantidad;
        return newErrors;
      });
    }

    let safeNum = num;
    if (!Number.isInteger(safeNum) || safeNum < 1) safeNum = 1;
    if (safeNum > 10) safeNum = 10;

    setPersonas((prev) => {
      if (prev.length === safeNum) return prev;
      const copy = prev.slice(0, safeNum);
      while (copy.length < safeNum) copy.push({ edad: "", pase: "regular" });
      return copy;
    });
  }, [cantidad]);

  // handlePersonaChange
  const handlePersonaChange = (idx, field, value) => {
    setPersonas((prev) => {
      const copy = prev.map((p) => ({ ...p }));
      copy[idx][field] = value;
      return copy;
    });

    if (field === "edad") {
      const edadNum = Number(value);
      const errorKey = "edad_" + idx;

      if (value === "") {
        setErrors((prev) => ({
          ...prev,
          [errorKey]: "Ingresá la edad.",
        }));
      } else if (edadNum < 0) {
        setErrors((prev) => ({
          ...prev,
          [errorKey]: "La edad no puede ser negativa.",
        }));
      } else if (edadNum > 121) {
        setErrors((prev) => ({
          ...prev,
          [errorKey]: "La edad no puede ser mayor a 121.",
        }));
      } else {
        setErrors((prev) => {
          const newErrors = { ...prev };
          delete newErrors[errorKey];
          return newErrors;
        });
      }
    }
  };

  // validate
  const validate = () => {
    const e = {};
    if (!fecha) e.fecha = "Elegí una fecha.";
    else {
      if (!isTodayOrFuture(fecha)) e.fecha = "La fecha debe ser hoy o futura.";
      if (!isOpenDay(fecha))
        e.fechaAbierto =
          "El parque abre todos los días excepto los lunes. Además está cerrado el 1/1 y el 25/12.";
    }

    if (!email.trim()) e.email = "Ingresá un email.";
    const c = Number(cantidad);
    if (!Number.isInteger(c) || c < 1) e.cantidad = "Mínimo 1 entrada.";
    if (c > 10) e.cantidad = "Máximo 10 entradas.";

    personas.forEach((p, i) => {
      if (p.edad === "" || Number(p.edad) < 0)
        e["edad_" + i] = "Edad inválida.";
      if (!["regular", "vip"].includes(p.pase))
        e["pase_" + i] = "Seleccioná un pase.";
    });

    setErrors(e);
    return Object.keys(e).length === 0;
  };

  // handleSubmit (con fix .toLowerCase())
  const handleSubmit = async (ev) => {
    ev.preventDefault();
    setOkMsg("");
    setErrors({});

    if (!validate()) {
      console.log("Error de validación del frontend.");
      return;
    }

    const datosCompra = {
      usuario_email: email,
      fecha_visita: fecha,
      forma_pago_nombre: pago,
      total: calculoPrecios.total, // Agregar el total calculado
      detalles: personas.map((p, index) => ({
        edad_visitante: Number(p.edad),
        tipo_entrada_nombre: p.pase.toLowerCase(), // Fix
        precio: calculoPrecios.detalles[index], // Agregar el precio individual
      })),
    };

    try {
      const response = await fetch("http://127.0.0.1:5000/api/comprar", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(datosCompra),
      });

      const resultado = await response.json();

      if (!response.ok) {
        setErrors({ api: resultado.error || "Error al procesar la compra." });
      } else {
        // ¡Éxito! El backend devolvió un 200 OK
        // Ej: {"status": "approved", ...}

        // Guarda los datos de la compra
        setPurchaseData(datosCompra);
        setPurchaseCompleted(true);

        // Muestra el mensaje de confirmación real
        setOkMsg(`¡Compra confirmada! Estado: ${resultado.status}.`);

        // Redirige a la pantalla simulada de Mercado Pago si corresponde
        if (datosCompra.forma_pago_nombre === 'tarjeta') {
          // Guardar datos en sessionStorage para acceder desde la otra ruta
          sessionStorage.setItem('purchaseData', JSON.stringify(datosCompra));
          setTimeout(() => {
            navigate('/fakemercadopago');
          }, 500);
        }
      }

    } catch (error) {
      console.error("Error de conexión:", error);
      setErrors({
        api: "No se pudo conectar con el servidor. ¿Está 'api.py' ejecutándose?",
      });
    }
  };

  return (
    <div className="form-wrapper">
      <h1>Compra de Entradas</h1>

      <form className="card" onSubmit={handleSubmit} noValidate>
        {/* Fecha */}
        <label className="field">
          <span>Fecha de visita</span>
          <input
            type="date"
            value={fecha}
            onChange={(e) => setFecha(e.target.value)}
          />
          {errors.fecha && <small className="err">{errors.fecha}</small>}
          {errors.fechaAbierto && (
            <small className="err">{errors.fechaAbierto}</small>
          )}
        </label>

        {/* Cantidad */}
        <label className="field">
          <span>Cantidad de entradas (máx. 10)</span>
          <input
            type="number"
            min={1}
            max={10}
            value={cantidad}
            onChange={(e) => setCantidad(e.target.value)}
          />
          {errors.cantidad && <small className="err">{errors.cantidad}</small>}
        </label>

        {/* Email */}
        <label className="field">
          <span>Email de confirmación</span>
          <input
            type="email"
            placeholder="tucorreo@ejemplo.com"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
          {errors.email && <small className="err">{errors.email}</small>}
        </label>

        {/* Personas */}
        <div className="people">
          <h2>Visitantes</h2>
          {personas.map((p, i) => (
            <div className="person" key={i}>
              <div className="inline">
                <label className="subfield">
                  <span>Edad #{i + 1}</span>
                  <input
                    type="number"
                    min={0}
                    max={121}
                    value={p.edad}
                    onChange={(e) =>
                      handlePersonaChange(i, "edad", e.target.value)
                    }
                  />
                  {errors["edad_" + i] && (
                    <small className="err">{errors["edad_" + i]}</small>
                  )}
                </label>

                <label className="subfield">
                  <span>Tipo de pase</span>
                  <select
                    value={p.pase}
                    onChange={(e) =>
                      handlePersonaChange(i, "pase", e.target.value)
                    }
                  >
                    <option value="regular">Regular</option>
                    <option value="vip">VIP</option>
                  </select>
                  {errors["pase_" + i] && (
                    <small className="err">{errors["pase_" + i]}</small>
                  )}
                </label>
              </div>
              {/* Muestra el precio por persona */}
              <div className="person-price">
                {formatCurrency(calculoPrecios.detalles[i])}
              </div>
            </div>
          ))}
        </div>

        {/* Pago */}
        <fieldset className="field radios">
          <legend>Forma de pago</legend>
          <label className="radio">
            <input
              type="radio"
              name="pago"
              value="efectivo"
              checked={pago === "efectivo"}
              onChange={(e) => setPago(e.target.value)}
            />
            <span>Efectivo</span>
          </label>
          <label className="radio">
            <input
              type="radio"
              name="pago"
              value="tarjeta"
              checked={pago === "tarjeta"}
              onChange={(e) => setPago(e.target.value)}
            />
            <span>Tarjeta </span>
          </label>
        </fieldset>

        {/* Muestra el Monto Total y el Desglose */}
        <div className="total-price-wrapper">
          {/* Sección Superior: Monto Total */}
          <div className="total-price-header">
            <span>Monto Total:</span>
            <span className="total-price-amount">
              {formatCurrency(calculoPrecios.total)}
            </span>
          </div>

          {/* Sección Inferior: Desglose (si hay items) */}
          {calculoPrecios.breakdown.length > 0 && (
            <div className="total-breakdown">
              {calculoPrecios.breakdown.map((line, i) => (
                <span key={i} className="breakdown-line">{line}</span>
              ))}
            </div>
          )}
        </div>

        {errors.api && (
          <small className="err" style={{ textAlign: "center", display: "block" }}>
            {errors.api}
          </small>
        )}

        <button className="btn" type="submit">
          Confirmar compra
        </button>

        {okMsg && <p className="ok">{okMsg}</p>}
        
        {/* Botón para ver detalle si la compra fue con efectivo y está completada */}
        {purchaseCompleted && pago === "efectivo" && (
          <button 
            className="btn btn-detail" 
            type="button"
            onClick={() => {
              sessionStorage.setItem('purchaseData', JSON.stringify(purchaseData));
              navigate('/detalle-compra');
            }}
          >
            Ver Detalle de Compra
          </button>
        )}
      </form>

      <p className="helper">
        EcoHarmony - Parque Natural<br />
        Abierto todos los días excepto los lunes.
        <br />
        Feriados cerrados: 1 de enero y 25 de diciembre.
      </p>
    </div>
  );
}
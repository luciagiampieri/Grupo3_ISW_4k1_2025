import { useEffect, useState } from "react";
import "./SimpleForm.css";

// Cierra los LUNES (1) | 0=Dom, 1=Lun, ... 6=Sáb
const CLOSED_WEEKDAY = 1;

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
  const [cantidad, setCantidad] = useState(1);
  const [fecha, setFecha] = useState("");
  const [email, setEmail] = useState("");
  const [pago, setPago] = useState("efectivo"); // "efectivo" | "tarjeta"
  const [personas, setPersonas] = useState([{ edad: "", pase: "regular" }]);
  const [errors, setErrors] = useState({});
  const [okMsg, setOkMsg] = useState("");

  // Mantener el arreglo de personas en sync con 'cantidad' (1..10)
  useEffect(() => {
    let n = Number(cantidad);
    if (!Number.isInteger(n) || n < 1) n = 1;
    if (n > 10) n = 10;
    if (n !== cantidad) setCantidad(n);

    setPersonas((prev) => {
      const copy = prev.slice(0, n);
      while (copy.length < n) copy.push({ edad: "", pase: "regular" });
      return copy;
    });
  }, [cantidad]);

  const handlePersonaChange = (idx, field, value) => {
    setPersonas((prev) => {
      const copy = prev.map((p) => ({ ...p }));
      copy[idx][field] = value;
      return copy;
    });
  };

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

  const handleSubmit = (ev) => {
    ev.preventDefault();
    setOkMsg("");
    if (!validate()) return;

    // Simulación de confirmación "vía mail"
    setOkMsg(`¡Listo! Enviamos la confirmación a ${email}.`);

    // Redirección si el pago es con tarjeta
    if (pago === "tarjeta") {
      window.location.assign("https://www.mercadopago.com.ar/");
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
            onChange={(e) => setCantidad(Number(e.target.value))}
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

        <button className="btn" type="submit">
          Confirmar compra
        </button>

        {okMsg && <p className="ok">{okMsg}</p>}
      </form>

      <p className="helper">
        EcoHarmony - Parque Natural. Abierto todos los días excepto los lunes.
        <br />
        Feriados cerrados: 1 de enero y 25 de diciembre.
      </p>
    </div>
  );
}

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
  const num = Number(cantidad);

  // 1. Lógica de validación instantánea
  if (cantidad !== "" && (!Number.isInteger(num) || num < 1 || num > 10)) {
    // Si el campo no está vacío Y el número es inválido, muestra el error.
    setErrors((prev) => ({
      ...prev,
      cantidad: "La cantidad debe ser entre 1 y 10.",
    }));
  } else {
    // Si el número es válido o el campo está vacío, elimina el error.
    setErrors((prev) => {
      const newErrors = { ...prev };
      delete newErrors.cantidad;
      return newErrors;
    });
  }

  // 2. Lógica para mostrar los campos de los visitantes (igual que antes)
  // Se usa una versión "segura" del número (entre 1 y 10) para no romper la UI.
  let safeNum = num;
  if (!Number.isInteger(safeNum) || safeNum < 1) safeNum = 1;
  if (safeNum > 10) safeNum = 10;

  setPersonas((prev) => {
    if (prev.length === safeNum) return prev; // Evita re-renderizados innecesarios
    const copy = prev.slice(0, safeNum);
    while (copy.length < safeNum) copy.push({ edad: "", pase: "regular" });
    return copy;
  });
}, [cantidad]); // Se ejecuta cada vez que 'cantidad' cambia

  const handlePersonaChange = (idx, field, value) => {
  // 1. Actualiza el estado de 'personas'
  setPersonas((prev) => {
    const copy = prev.map((p) => ({ ...p }));
    copy[idx][field] = value;
    return copy;
  });

  // 2. Validación instantánea solo para el campo 'edad'
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
      // Si es válido, borra el error específico
      setErrors((prev) => {
        const newErrors = { ...prev };
        delete newErrors[errorKey];
        return newErrors;
      });
    }
  }
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

  // Reemplaza tu handleSubmit por esta versión
  const handleSubmit = async (ev) => {
    ev.preventDefault();
    setOkMsg("");
    setErrors({}); // Limpia errores previos

    // 1. Ejecuta la validación del frontend primero
    if (!validate()) {
      console.log("Error de validación del frontend.");
      return;
    }

    // 2. Prepara el JSON para el backend
    //    (Traduciendo los nombres de estado del front a los esperados por la API)
    const datosCompra = {
      usuario_email: email,
      fecha_visita: fecha,
      forma_pago_nombre: pago, // "efectivo" o "tarjeta"
      detalles: personas.map((p) => ({
        edad_visitante: Number(p.edad), // Aseguramos que sea número
        tipo_entrada_nombre: p.pase, // "regular" o "vip"
      })),
    };

    try {
      // 3. Llama a la API de Flask (¡la que creamos!)
      const response = await fetch("http://127.0.0.1:5000/api/comprar", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(datosCompra),
      });

      // 4. Obtiene la respuesta del backend
      const resultado = await response.json();

      // 5. Maneja la respuesta
      if (!response.ok) {
        // Si el backend devolvió un error (400, 403, 500)
        // Ej: {"error": "El usuario no está registrado."}
        // Lo mostramos como un error general en el formulario
        setErrors({ api: resultado.error || "Error al procesar la compra." });
      } else {
        // ¡Éxito! El backend devolvió un 200 OK
        // Ej: {"status": "approved", ...}

        // Muestra el mensaje de confirmación real
        setOkMsg(`¡Compra confirmada! Estado: ${resultado.status}.`);

        // Si el backend nos dio una URL de Mercado Pago, redirigimos
        if (resultado.redirect_url) {
          // Usamos un pequeño delay para que el usuario alcance a leer el msg
          setTimeout(() => {
            window.location.assign(resultado.redirect_url);
          }, 1500);
        }
      }
    } catch (error) {
      // Error de red (ej. el servidor de Flask no está corriendo)
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
            onChange={(e) => setCantidad((e.target.value))}
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

        {/* ... dentro del <form> ... */}

        {/* Agrega esto antes del botón */}
        {errors.api && (
          <small className="err" style={{ textAlign: "center", display: "block" }}>
            {errors.api}
          </small>
        )}

        <button className="btn" type="submit">
          Confirmar compra
        </button>

        {/* ... */}

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
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import traceback # Para ver errores detallados en la terminal

# --- Importamos tus Modelos de Negocio ---
# (Asumimos que están en una carpeta 'modelos' o en el mismo nivel)
try:
    # --- Importamos tus Modelos de Negocio ---
# (Asumimos que están todos en la misma carpeta)
    from modelos.usuario import Usuario
    from modelos.tipoEntrada import TipoEntrada
    from modelos.formaPago import FormaPago
    from modelos.detalleEntrada import DetalleEntrada
    from modelos.entrada import Entrada
    import base_de_datos
except ImportError:
    # Si no están en 'modelos', prueba importarlos directamente
    from modelos.usuario import Usuario
    from modelos.tipoEntrada import TipoEntrada
    from modelos.formaPago import FormaPago
    from modelos.detalleEntrada import DetalleEntrada
    from modelos.entrada import Entrada

# --- Creación de la Aplicación Flask ---
app = Flask(__name__)

CORS(app)


@app.route('/api/comprar', methods=['POST'])
def comprar_entrada():
    
    """
    Endpoint para procesar una nueva compra de entradas.
    Espera un JSON con:
    {
        "usuario_email": "fachi@gmail.com",
        "fecha_visita": "2025-10-25",
        "forma_pago_nombre": "tarjeta débito",
        "detalles": [
            { "edad_visitante": 25, "tipo_entrada_nombre": "regular" },
            { "edad_visitante": 70, "tipo_entrada_nombre": "VIP" }
        ]
    }
    """
    try:
        # 1. Obtener los datos JSON de la solicitud
        data = request.get_json()
        if not data:
            return jsonify({"error": "No se recibieron datos (JSON vacío)."}), 400

        # --- 2. Validar y "Rehidratar" los objetos de dominio ---
        
        # 2a. Validar Usuario (Criterio de Aceptación)
        usuario_email = data.get('usuario_email')
        if not usuario_email:
            return jsonify({"error": "Falta 'usuario_email'."}), 400
        
        usuario = Usuario(mail=usuario_email)
        # Re-usamos la lógica de validación que ya probaste
        if not usuario.validar_usuario_registrado(usuario_email): #
            return jsonify({"error": "El usuario no está registrado."}), 403 # 403 Forbidden

        # 2b. Validar y parsear Fecha
        fecha_visita_str = data.get('fecha_visita')
        if not fecha_visita_str:
            return jsonify({"error": "Falta 'fecha_visita'."}), 400
        # Convertimos el string "YYYY-MM-DD" a un objeto date
        fecha_visita_obj = datetime.strptime(fecha_visita_str, '%Y-%m-%d').date()

        # 2c. Crear Forma de Pago
        forma_pago_nombre = data.get('forma_pago_nombre', 'tarjeta')
        forma_pago = FormaPago(nombre=data["forma_pago_nombre"], descripcion=f"Pago con {data['forma_pago_nombre']}")


        # 2d. Crear Detalles de Entradas
        detalles_json = data.get('detalles')
        if not detalles_json or not isinstance(detalles_json, list) or len(detalles_json) == 0:
            return jsonify({"error": "Falta la lista 'detalles' o está vacía."}), 400

        detalles_entrada_obj = []
        for detalle_data in detalles_json:
            tipo_nombre = detalle_data.get('tipo_entrada_nombre')
            tipo_row = base_de_datos.get_tipo_entrada_por_nombre(tipo_nombre)

            if not tipo_row:
                return jsonify({"error": f"El tipo de entrada '{tipo_nombre}' no es válido."}), 400

            # Normalizar lo que devuelve la función de la DB a una instancia de TipoEntrada
            if isinstance(tipo_row, TipoEntrada):
                tipo_entrada_obj = tipo_row
            elif isinstance(tipo_row, dict):
                tipo_entrada_obj = TipoEntrada(
                    nombre=tipo_row.get('nombre', tipo_nombre),
                    descripcion=tipo_row.get('descripcion'),
                    precio=float(tipo_row.get('precio', 0))
                )
            elif isinstance(tipo_row, (int, float)):
                # Si la función solo devuelve el precio
                tipo_entrada_obj = TipoEntrada(nombre=tipo_nombre, descripcion=None, precio=float(tipo_row))
            else:
                # intento genérico (por si retorna sqlite3.Row)
                try:
                    nombre = tipo_row['nombre'] if 'nombre' in tipo_row else tipo_nombre
                    precio = float(tipo_row['precio'])
                    descripcion = tipo_row.get('descripcion', None) if hasattr(tipo_row, 'get') else None
                    tipo_entrada_obj = TipoEntrada(nombre=nombre, descripcion=descripcion, precio=precio)
                except Exception:
                    return jsonify({"error": f"El tipo de entrada '{tipo_nombre}' no es válido."}), 400
                
            detalle = DetalleEntrada(
                edad_visitante=detalle_data.get('edad_visitante'),
                tipo_entrada=tipo_entrada_obj #
            )
            detalles_entrada_obj.append(detalle)
        cantidad = len(detalles_entrada_obj)

        # --- 3. Crear la instancia principal de Entrada ---
        entrada = Entrada(
            usuario=usuario,
            cantidad=cantidad,
            fecha_visita=fecha_visita_obj,
            forma_pago=forma_pago,
            detalles_entrada=detalles_entrada_obj
        ) #

        # --- 4. Ejecutar la Lógica de Negocio (RE-USANDO tus validaciones) ---
        # Si algo falla aquí, lanzará un ValueError que capturará el 'except'
        
        entrada.validarCantidadEntradas() #
        entrada.validarFechaVisita()      #

        # 5. Procesar el pago
        resultado_pago = entrada.procesar_pago() #

        # --- 6. Devolver Respuesta Exitosa ---
        # El frontend recibirá este JSON y podrá actuar (ej. redirigir a MP)
        return jsonify(resultado_pago), 200

    except ValueError as e:
        # ¡Magia! Capturamos cualquier error de validación de tus modelos
        # (ej. "La fecha de visita no puede ser un lunes...")
        return jsonify({"error": str(e)}), 400 # 400 Bad Request
    
    except Exception as e:
        # Captura para cualquier otro error inesperado (ej. error de sintaxis)
        print("--- ERROR INTERNO ---")
        traceback.print_exc() # Muestra el error completo en la terminal del servidor
        print("---------------------")
        return jsonify({"error": "Ocurrió un error interno en el servidor."}), 500


@app.route('/api/confirmar_pago', methods=['POST'])
def confirmar_pago():
    """
    Confirma el pago (tarjeta o efectivo) y guarda la compra en la base de datos.
    Solo se ejecuta cuando el pago fue confirmado en el frontend.
    """
    try:
        data = request.get_json()

        print("🟡 Datos recibidos en /api/confirmar_pago:")
        print(data)
        print("📍 Ruta DB:", base_de_datos.DB_PATH)

        if not data:
            return jsonify({"error": "No se recibieron datos"}), 400

        usuario = Usuario(mail=data["usuario_email"])
        forma_pago = FormaPago(nombre=data["forma_pago_nombre"], descripcion=f"Pago con {data['forma_pago_nombre']}")

        CATALOGO_PRECIOS = {
            "regular": 5000,
            "vip": 10000,
        }
        detalles = []
        for d in data["detalles"]:
            nombre_tipo = d["tipo_entrada_nombre"].strip().lower()
            precio_base = CATALOGO_PRECIOS.get(nombre_tipo)
            if precio_base is None:
                return jsonify({"error": f"Tipo de entrada desconocido: {nombre_tipo}"}), 400

            tipo = TipoEntrada(
                nombre=nombre_tipo,
                descripcion=f"Entrada {nombre_tipo}",
                precio=precio_base  # base, sin descuento aplicado
            )
            detalles.append(
                DetalleEntrada(
                    edad_visitante=d["edad_visitante"],
                    tipo_entrada=tipo
                )
            )

        entrada = Entrada(
            usuario=usuario,
            cantidad=len(detalles),
            fecha_visita=datetime.strptime(data["fecha_visita"], "%Y-%m-%d").date(),
            forma_pago=forma_pago,
            detalles_entrada=detalles
        )

        # Procesar pago (simulación)
        pago = entrada.procesar_pago()

        print("🟢 Resultado de procesar_pago:", pago) 

        if pago["status"] == "approved":

            print("⚙️ Entrando al bloque de guardado (pago aprobado)")
            print(f"➡️ Usuario: {usuario.mail} | Fecha: {entrada.fecha_visita} | Cantidad: {entrada.cantidad}")

            entrada_id = base_de_datos.insertar_entrada(
                usuario_email=usuario.mail,
                cantidad=entrada.cantidad,
                fecha_visita=str(entrada.fecha_visita),
                forma_pago_nombre=forma_pago.nombre,
                forma_pago_descripcion=getattr(forma_pago, "descripcion", None),
                fecha_compra=str(entrada.fecha_compra),
                estado_pago="approved"
            )

            for detalle in detalles:
                tipo = detalle.tipo_entrada
                base_de_datos.insertar_detalle(
                    entrada_id=entrada_id,
                    edad_visitante=detalle.edad_visitante,
                    tipo_entrada_nombre=tipo.nombre,
                    tipo_entrada_descripcion=getattr(tipo, "descripcion", None),  
                    tipo_entrada_precio=tipo.precio
            )


            print(f"💾 Compra confirmada y guardada en la base de datos (ID: {entrada_id})")

        return jsonify({"status": pago["status"]}), 200

    except Exception as e:
        import traceback; traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@app.route('/api/enviar_mail', methods=['POST'])
def enviar_mail_confirmacion(): # Se renombró para evitar conflicto con el método
    """Envía el correo real de confirmación de compra usando la plantilla HTML de la clase Entrada."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No se recibieron datos"}), 400

        # 1. Recrear los objetos de negocio
        email = data.get("usuario_email")
        forma_pago_nombre = data.get("forma_pago_nombre")
        fecha_visita_str = data.get("fecha_visita")
        detalles_data = data.get("detalles", [])

        if not email or not forma_pago_nombre or not fecha_visita_str or not detalles_data:
            return jsonify({"error": "Faltan datos esenciales (email, forma_pago, fecha_visita, detalles)."}), 400

        usuario = Usuario(mail=email)
        forma_pago = FormaPago(nombre=forma_pago_nombre, descripcion=f"Pago con {forma_pago_nombre}")
        
        # Necesitamos recrear los objetos DetalleEntrada para que calcular_monto() funcione
        detalles_entrada_obj = []
        for d in detalles_data:
            tipo_nombre = d["tipo_entrada_nombre"]
            tipo_row = base_de_datos.get_tipo_entrada_por_nombre(tipo_nombre)

            if not tipo_row:
                return jsonify({"error": f"El tipo de entrada '{tipo_nombre}' no es válido."}), 400

            if isinstance(tipo_row, TipoEntrada):
                tipo_entrada_obj = tipo_row
            elif isinstance(tipo_row, dict):
                tipo_entrada_obj = TipoEntrada(
                    nombre=tipo_row.get('nombre', tipo_nombre),
                    descripcion=tipo_row.get('descripcion'),
                    precio=float(tipo_row.get('precio', 0))
                )
            elif isinstance(tipo_row, (int, float)):
                tipo_entrada_obj = TipoEntrada(nombre=tipo_nombre, descripcion=None, precio=float(tipo_row))
            else:
                try:
                    nombre = tipo_row['nombre'] if 'nombre' in tipo_row else tipo_nombre
                    precio = float(tipo_row['precio'])
                    descripcion = tipo_row.get('descripcion', None) if hasattr(tipo_row, 'get') else None
                    tipo_entrada_obj = TipoEntrada(nombre=nombre, descripcion=descripcion, precio=precio)
                except Exception:
                    return jsonify({"error": f"El tipo de entrada '{tipo_nombre}' no es válido."}), 400

            detalles_entrada_obj.append(
                DetalleEntrada(
                    edad_visitante=d["edad_visitante"],
                    tipo_entrada=tipo_entrada_obj  # precio base
                )
            )

        fecha_visita_obj = datetime.strptime(fecha_visita_str, "%Y-%m-%d").date()
        
        # 2. Crear la instancia de Entrada
        entrada = Entrada(
            usuario=usuario,
            cantidad=len(detalles_entrada_obj),
            fecha_visita=fecha_visita_obj,
            forma_pago=forma_pago,
            detalles_entrada=detalles_entrada_obj
        )

        # 3. Usar el método interno para generar el HTML completo
        cuerpo_html = entrada._generar_html_compra()
        
        # 4. Generar cuerpo de texto simple (fallback)
        total = entrada.monto_total() # Se calcula el total correctamente
        cuerpo_texto = (
            f"Hola {email},\n\n"
            f"Tu compra fue confirmada exitosamente.\n"
            f"Método de pago: {forma_pago_nombre.capitalize()}\n"
            f"Monto total: ${total}\n"
            f"Fecha de visita: {fecha_visita_str}\n\n"
            "¡Gracias por tu compra y que disfrutes tu visita!"
        )
        
        # 5. Enviar el correo usando el método de la clase Entrada
        asunto = "✅ Confirmación de compra en EcoHarmony Park"
        entrada.enviar_mail(
            destinatario=email, 
            asunto=asunto, 
            cuerpo_texto=cuerpo_texto, 
            cuerpo_html=cuerpo_html # Se pasa el HTML generado por _generar_html_compra()
        )

        return jsonify({"message": "Correo enviado correctamente con plantilla HTML."}), 200

    except Exception as e:
        import traceback; traceback.print_exc()
        return jsonify({"error": f"Error al enviar el correo: {str(e)}"}), 500

# --- Punto de entrada para ejecutar el servidor ---
if __name__ == '__main__':
    # init_db() # Si necesitas asegurar que la DB se inicie (aunque base_de_datos.py ya lo hace)
    print("Servidor API de EcoHarmony iniciado en http://127.0.0.1:5000")
    app.run(debug=True, port=5000) # debug=True para que se reinicie solo con cambios
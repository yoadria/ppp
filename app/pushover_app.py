import requests
import logging
import json

logging.basicConfig(
    level=logging.DEBUG,  # Muestra los logs de nivel DEBUG y superior
    format='%(asctime)s - %(levelname)s - %(message)s'  # Formato para mostrar los logs
)

_logging = logging.getLogger(__name__)

# --- ¡IMPORTANTE! Verifica estas claves ---
# Asegúrate de que API_TOKEN sea la clave de tu APLICACIÓN en Pushover
# y USER_KEY sea tu clave de USUARIO personal de Pushover.
# En tu ejemplo anterior parecían estar al revés. Revisa tu dashboard de Pushover.
API_TOKEN = 'aihav4mdzxeey528gkmmaknt75nf81'  # Token de tu Aplicación Pushover
USER_KEY = 'usi8tt5hzn9utn8wv6sq8higcn4pgb'   # Tu User Key de Pushover

# --- Valores para Emergencia ---
# Define cada cuánto se reintenta (mínimo 30 segundos)
SEGUNDOS_REINTENTO = 60  # Ejemplo: Reintentar cada 60 segundos
# Define durante cuánto tiempo se reintentará (máximo 10800 segundos = 3 horas)
# Recuerda el límite de 50 reintentos. Con 60s de reintento, 3600s (1 hora) son 60 reintentos.
# Se limitará a 50 reintentos * 60s = 3000 segundos (50 minutos).
# Si pones retry=30 y expire=10800, se limitará a 50 reintentos * 30s = 1500 segundos (25 minutos).
SEGUNDOS_EXPIRACION = 3600 # Ejemplo: Dejar de reintentar después de 1 hora (efectivamente 50 mins con retry=60)

# Opcional: URL de Callback (debe ser pública y accesible desde internet)
# CALLBACK_URL = "https://tu.servidor.com/api/pushover_callback" # Descomenta y ajusta si la necesitas

def enviar_notificacion_llamada(habitacion, cama):
    """
    Envia una notificación a Pushover indicando una llamada
    desde una habitación y cama específicas.
    """
    # Construye el mensaje deseado usando los parámetros recibidos
    # mensaje = f"Llamada de la cama {habitacion}{cama}" # Opción 1: Más directo
    mensaje = f"Llamada recibida desde la habitación {habitacion}, cama {cama}." # Opción 2: Más descriptivo

    # Crear un tag único para esta llamada específica (útil para cancelar por tag)
    # Ejemplo: "llamada_hab101_camaA"
    tag_llamada = f"llamada_hab{habitacion}_cama{cama}"
    # Datos para la API de Pushover
    data = {
        "token": API_TOKEN,
        "user": USER_KEY,
        "message": mensaje,
        "title": "Llamada entrante",
        "html": 0,          # O 1 si usas HTML simple (<b>, <i>, <u>, <a>, <font>)
        "priority": 2,      # ¡Prioridad de Emergencia!
        "retry": SEGUNDOS_REINTENTO,  # ¡Obligatorio para priority=2!
        "expire": SEGUNDOS_EXPIRACION, # ¡Obligatorio para priority=2!
        "sound": "persistent", # Sonido 'persistent' o 'echo' son buenos para emergencia
                               # 'persistent' suena hasta que se confirma
        "tags": tag_llamada     # Añadir la etiqueta para posible cancelación posterior
        # Descomenta la siguiente línea si usas callback:
        # "callback": CALLBACK_URL,
    }
    receipt_id = None # Para guardar el ID del recibo si la llamada es exitosa

    _logging.debug(f"Enviando datos a Pushover: {data}")
    # Intenta enviar la notificación
    try:
        response = requests.post(
            "https://api.pushover.net/1/messages.json",
            data=data,
            timeout=15
        )
        # Verifica si la respuesta de Pushover fue exitosa (código 2xx)
        response.raise_for_status()
        respuesta_json = response.json()
        _logging.debug(f"Respuesta de Pushover: {respuesta_json}")

        # Verifica el estado en la respuesta y obtiene el receipt
        if respuesta_json.get("status") == 1 and "receipt" in respuesta_json:
            receipt_id = respuesta_json["receipt"]
            _logging.info(f"✅ Notificación de EMERGENCIA enviada para Hab: {habitacion}, Cama: {cama}. Receipt ID: {receipt_id}, Tag: {tag_llamada}")
            # --- ¡IMPORTANTE! ---
            # Debes guardar este 'receipt_id' asociado a la llamada original
            # si necesitas verificar su estado o cancelarla más tarde.
            # Por ejemplo, guardarlo en tu base de datos junto al registro de la llamada.
            return receipt_id # Devolver el receipt para que el código que llama lo gestione
        else:
            # Caso raro: HTTP 200 pero la respuesta indica un problema
            error_msg = respuesta_json.get("errors", ["Respuesta inesperada sin errores detallados"])
            _logging.error(f"⚠️ Error lógico de API Pushover para Hab: {habitacion}, Cama: {cama}: {error_msg}")
            return None
        
    except requests.exceptions.RequestException as e:
        _logging.error(f"❌ Error al enviar notificación para Hab: {habitacion}, Cama: {cama}: {e}")
        # Imprimir más detalles si hay una respuesta de error de la API
        if hasattr(e, 'response') and e.response is not None:
            try:
                # Intenta decodificar el cuerpo de la respuesta como JSON
                error_json = e.response.json()
                error_detalle = f"Código: {e.response.status_code}, Errores: {error_json.get('errors', ['N/A'])}"
            except json.JSONDecodeError:
                # Si la respuesta no es JSON válido
                error_detalle = f"Código: {e.response.status_code}, Respuesta (no JSON): {e.response.text}"
            _logging.error(f"   Detalle del error de API Pushover: {error_detalle}")
        return None # Indicar fallo


def callback_pushover(receipts):


    try:
        response = requests.get(
            'https://api.pushover.net/1/receipts/%s.json?token=%s' % (receipts, API_TOKEN),
            timeout=15
        )

        response.raise_for_status()
        respuesta_json = response.json()
        acknowledged_by_device = respuesta_json['acknowledged_by_device']
        _logging.debug(f"Respuesta de Pushover: {respuesta_json}")
        return acknowledged_by_device
    except requests.exceptions.RequestException as e:
        _logging.error(f"❌ Error al consultar el estado del recibo: {e}")
        return None
    except json.JSONDecodeError:
        _logging.error("❌ Error al decodificar la respuesta JSON")
        return None
    except Exception as e:
        _logging.error(f"❌ Error inesperado: {e}")
        return None

import requests
import logging
import json

logging.basicConfig(
    level=logging.DEBUG, 
    format='%(asctime)s - %(levelname)s - %(message)s' 
)

_logging = logging.getLogger(__name__)

API_TOKEN = 'aihav4mdzxeey528gkmmaknt75nf81'  # Token de tu Aplicación Pushover
USER_KEY = 'usi8tt5hzn9utn8wv6sq8higcn4pgb'   # Tu User Key de Pushover


SEGUNDOS_REINTENTO = 30  # Ejemplo: Reintentar cada 60 segundos

SEGUNDOS_EXPIRACION = 180 # Ejemplo: Dejar de reintentar después de 3 minutos (180 segundos)

def enviar_notificacion_llamada(habitacion, cama):
    """
    Envia una notificación a Pushover indicando una llamada
    desde una habitación y cama específicas.
    """
    url_atender = f"http://192.168.0.103:5000/llamada/atendida?habitacion={habitacion}&cama={cama}"
    mensaje = (
        f"<p>Llamada recibida desde la habitación <font color='red'><b>{habitacion}</b></font> y cama <font color='red'><b>{cama}</b></font>.</p>"
        f"<a href='{url_atender}'>Atender soliciud de asistencia</a>"
    )

    tag_llamada = f"llamada_hab{habitacion}_cama{cama}"
    # Datos para la API de Pushover
    data = {
        "token": API_TOKEN,
        "user": USER_KEY,
        "message": mensaje,
        "title": "Llamada entrante",
        "html": 1,         
        "priority": 2,     
        "retry": SEGUNDOS_REINTENTO,  
        "expire": SEGUNDOS_EXPIRACION,
        "sound": "persistent",
                              
        "tags": tag_llamada    

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


        if respuesta_json.get("status") == 1:
            _logging.info(f"✅ Notificación de EMERGENCIA enviada para Hab: {habitacion}, Cama: {cama}. Tag: {tag_llamada}")
        else:
            error_msg = respuesta_json.get("errors", ["Respuesta inesperada sin errores detallados"])
            _logging.error(f"⚠️ Error lógico de API Pushover para Hab: {habitacion}, Cama: {cama}: {error_msg}")
    except requests.exceptions.RequestException as e:
        _logging.error(f"❌ Error al enviar notificación para Hab: {habitacion}, Cama: {cama}: {e}")
        if hasattr(e, 'response') and e.response is not None:
            try:
                error_json = e.response.json()
                error_detalle = f"Código: {e.response.status_code}, Errores: {error_json.get('errors', ['N/A'])}"
            except json.JSONDecodeError:
                error_detalle = f"Código: {e.response.status_code}, Respuesta (no JSON): {e.response.text}"
            _logging.error(f"   Detalle del error de API Pushover: {error_detalle}")
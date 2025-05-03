

import requests

# --- ¡IMPORTANTE! Verifica estas claves ---
# Asegúrate de que API_TOKEN sea la clave de tu APLICACIÓN en Pushover
# y USER_KEY sea tu clave de USUARIO personal de Pushover.
# En tu ejemplo anterior parecían estar al revés. Revisa tu dashboard de Pushover.
API_TOKEN = 'aihav4mdzxeey528gkmmaknt75nf81'  # Token de tu Aplicación Pushover
USER_KEY = 'usi8tt5hzn9utn8wv6sq8higcn4pgb'   # Tu User Key de Pushover

def enviar_notificacion_llamada(habitacion, cama):
    """
    Envia una notificación a Pushover indicando una llamada
    desde una habitación y cama específicas.
    """
    # Construye el mensaje deseado usando los parámetros recibidos
    # mensaje = f"Llamada de la cama {habitacion}{cama}" # Opción 1: Más directo
    mensaje = f"Llamada recibida desde la habitación {habitacion}, cama {cama}." # Opción 2: Más descriptivo

    # Datos para la API de Pushover
    data = {
        "token": API_TOKEN,
        "user": USER_KEY,
        "message": mensaje,
        "title": "🚨 Nueva Llamada", # Puedes personalizar el título
        "html": 0,  # Cambia a 1 si quieres usar etiquetas HTML <b>, <u>, <i> etc. en el mensaje
        "priority": 0,  # 1 = Alta prioridad (requiere confirmación en el cliente), 0 = Normal, -1 = Baja, -2 = Silencioso
        "sound": "persistent"  # Sonido de la notificación (ver sonidos disponibles en Pushover)
                               # 'persistent' es bueno para llamadas urgentes
    }

    # Intenta enviar la notificación
    try:
        # Es buena idea añadir un timeout a la petición
        response = requests.post("https://api.pushover.net/1/messages.json", data=data, timeout=10)
        # Verifica si la respuesta de Pushover fue exitosa (código 2xx)
        response.raise_for_status()
        print(f"✅ Notificación enviada correctamente para Hab: {habitacion}, Cama: {cama}.")
        # Podrías devolver True si la ruta necesita saber si funcionó
        # return True
    except requests.exceptions.RequestException as e:
        print(f"❌ Error al enviar notificación para Hab: {habitacion}, Cama: {cama}: {e}")
        # Imprimir más detalles si hay una respuesta de error de la API
        if hasattr(e, 'response') and e.response is not None:
             print(f"   Error de API Pushover: {e.response.status_code} - {e.response.text}")
        # Podrías devolver False en caso de error
        # return False

# --- No pongas código de ejecución directa aquí abajo si solo quieres la función ---
# conn = http.client.HTTPSConnection("api.pushover.net", 443)
# ... (El resto del código anterior con http.client se elimina) ...
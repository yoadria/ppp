# Hospital Call System

Este proyecto es un sistema de gestión de llamadas y asistencias para habitaciones de hospital, desarrollado en Python con Flask, MariaDB y notificaciones Pushover. Permite que pacientes realicen llamadas desde su cama y que los asistentes gestionen y atiendan dichas llamadas.

## Características principales

- Gestión de habitaciones y camas.
- Registro y autenticación de asistentes.
- Llamadas de asistencia desde camas.
- Asignación y atención de llamadas por asistentes.
- Registro de presencia cuando el asistente atiende la llamada.
- Histórico de llamadas y asistencias.
- Notificaciones push a través de Pushover.
- Interfaz web moderna con TailwindCSS.
- Arquitectura basada en contenedores Docker.

## Estructura del proyecto

```
.
├── app/
│   ├── __init__.py
│   ├── pushover_app.py
│   ├── routes.py
│   ├── static/
│   │   ├── pic_bulboff.gif
│   │   ├── pic_bulbon.gif
│   │   └── style.css
│   └── templates/
│       ├── index.html
│       ├── panelhab.html
│       ├── historico.html
│       ├── form_asistente.html
│       ├── form_habitacion_cama.html
│       ├── asistencias.html
│       └── enrolar.html
├── database/
│   ├── __init__.py
│   ├── conexion.py
│   ├── insertar_datos.py
│   ├── solicitar_datos.py
│   └── actualizar_datos.py
├── initdb/
│   └── init.sql
├── nginx/
│   └── nginx.conf
├── main.py
├── requirements.txt
├── Dockerfile
├── compose.yaml
└── README.md
```

## Arquitectura de contenedores

- **flask_app**: Servidor Flask (Gunicorn) con la aplicación web.
- **mariadb**: Base de datos MariaDB.
- **nginx**: Servidor web inverso para servir la app y archivos estáticos.
- **adminer**: Interfaz web para administrar la base de datos.
- **wdb**: Debugger remoto para Python.

## Instalación y ejecución

### Requisitos

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

### Pasos

1. Clona el repositorio:
   ```sh
   git clone <url-del-repo>
   cd ppp
   ```

2. Levanta los servicios con Docker Compose:
   ```sh
   docker compose up --build
   ```

3. Accede a la aplicación web:
   - [http://localhost](http://localhost) (interfaz principal)
   - [http://localhost:8080](http://localhost:8080) (Adminer para la base de datos)

## Uso básico

- **Panel de control**: Permite ver el histórico de llamadas, gestionar asistentes y habitaciones.
- **Panel de habitación**: Simula la interfaz de llamada desde una cama.
- **Asistencias**: Vista para asistentes, donde pueden enrolarse y ver llamadas activas.
- **Notificaciones**: Cuando un paciente realiza una llamada, se envía una notificación push a los asistentes.

## Variables de entorno

Las variables de entorno para la base de datos y Flask están definidas en `compose.yaml` y se pasan automáticamente a los contenedores.

## Inicialización de la base de datos

El script `initdb/init.sql` crea las tablas necesarias y datos iniciales al levantar el contenedor de MariaDB por primera vez.

## Notas adicionales

- El sistema utiliza Pushover para notificaciones push. Configura tus propias claves en `app/pushover_app.py` si lo necesitas.
- El frontend utiliza TailwindCSS vía CDN.
- El sistema está pensado para ser ejecutado en entorno Docker.

---

**Autor:** Adria Hortoneda Martinez  
**Licencia:** MIT

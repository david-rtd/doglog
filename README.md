# 🛡️ DogLog - Linux Log Watchdog & Incident Response
<img width="702" height="262" alt="Captura de pantalla 2026-06-10 185220" src="https://github.com/user-attachments/assets/342253b0-5a17-4a20-8197-e69722f15065" />

**DogLog** es un sistema automatizado de detección de intrusos (IDS) y respuesta ante incidentes en tiempo real diseñado para entornos Linux (Fedora/Kali). El script actúa como un componente *Blue Team*, monitorizando de forma continua los logs de acceso del servidor para detectar patrones de ataques web comunes (Inyecciones SQL, Path Traversal, XSS) y notificando de inmediato al administrador a través de alertas securizadas en Telegram.

---

## 🚀 Características principales

* **Monitorización en Tiempo Real (`Tail -F` Nativo):** Análisis de flujos de logs línea a línea sin saturar la CPU.
* **Detección de Patrones Maliciosos:** Filtros optimizados para identificar payloads sospechosos (`UNION SELECT`, `../`, `<script>`, etc.).
* **Alertas Instantáneas:** Integración con la API de Telegram para recibir alertas críticas en el móvil en menos de 2 segundos.
* **Seguridad por Diseño (PoLP):** Gestión de credenciales críticas (Tokens e IDs) aislada del código fuente mediante variables de entorno (`.env`).
* **Cierre Elegante:** Control de interrupciones del sistema (`SIGINT`) para un apagado limpio en consola.

---

## 🛠️ Arquitectura y Flujo de Datos

El sistema sigue un modelo de monitorización pasiva y respuesta activa:

1. El atacante genera una petición web maliciosa.
2. El servidor web (o el entorno simulado) registra el evento en `server_access.log`.
3. **DogLog** detecta la nueva línea, analiza el *payload* y activa el disparador si coincide con la firma de ataque.
4. Se emite una petición HTTP POST securizada hacia la API de Telegram, enviando los detalles del incidente al dispositivo del administrador.

---

## 📦 Requisitos e Instalación

### 1. Clonar el repositorio
git clone [https://github.com/TU_USUARIO/doglog.git](https://github.com/david-rtd/doglog.git)

cd doglog

___

### 2. Instalar dependencias
El script utiliza la librería requests para la comunicación con la API. Instálala ejecutando:

pip install requests python-dotenv

___

### 3. Configuración del Entorno (.env)

## IMPORTANTE: https://t.me/botfather
Este es el enlace oficial de BotFather, cualquier otro enlace puede ser una estafa
___

Por motivos de seguridad, nunca subas tus credenciales al repositorio. Crea un archivo .env en la raíz del proyecto:

nano .env
Añade tus credenciales con el siguiente formato (sin espacios):

Fragmento de código
TELEGRAM_TOKEN=tu_token_de_botfather_aqui
TELEGRAM_CHAT_ID=tu_id_numérico_aquí
(Nota: Asegúrate de que tu .gitignore incluye el archivo .env antes de hacer el push).

___

### Conseguir el id numerico
Abre el bot que creaste en el BotFather real y asegúrate de haberle dado al botón Iniciar / Start (si ya lo hiciste antes, dale otra vez por si acaso).

Abre una pestaña en tu navegador web.

Copia la siguiente dirección en la barra de URL, pero cambiando la palabra TU_TOKEN_AQUÍ por el token largo que te dio BotFather (el que empieza por números y tiene dos puntos):

https://api.telegram.org/botTELEGRAM_TOKEN/getUpdates
Dale a Enter

Te saldra este contenido:

"message": {
    "from": {
        "id": 123456789,
        "is_bot": false,
        "first_name": "Usuario",
        "username": "tu_usuario"
    }
}

Donde "id", copialo y agregalo en TELEGRAM_CHAT_ID

___

### 💻 Uso y Demostración
Ejecuta el script principal en tu terminal de Linux:

python doglog.py
En una segunda terminal, simula un ataque inyectando una firma maliciosa en el log de pruebas:

echo "192.168.1.50 - - [10/06/2026] 'GET /admin.php?id=1 UNION SELECT' 404" >> server_access.log

Resultado: El guardián procesará la línea y recibirás una alerta push en tu aplicación de Telegram de forma inmediata con los detalles del host atacante y el payload detectado.

Para detener el script de forma limpia, pulsa Ctrl + C.
<img width="692" height="222" alt="Captura de pantalla 2026-06-10 185613" src="https://github.com/user-attachments/assets/87663ddd-d818-42ec-952d-b2a35ce58d01" />

___

### 🛠️ Tecnologías Utilizadas
Lenguaje: Python 3.x

Librerías Core: os, time, requests, dotenv

Entorno de Pruebas: Linux (Fedora / Kali Linux)

Plataforma de Alertas: Telegram Bot API

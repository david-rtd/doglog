import os
import time
import requests
from dotenv import load_dotenv

# Cargamos las credenciales seguras desde el archivo .env
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Archivo de log que vamos a monitorizar (puedes apuntar a /var/log/auth.log en entornos reales)
LOG_FILE_PATH = "server_access.log"

# Patrones sospechosos que queremos cazar (OWASP / Escaneos comunes)
SUSPICIOUS_PATTERNS = [
    "select * from", "union select",  # Inyecciones SQL
    "../", "etc/passwd",              # Path Traversal (Escalada de directorios)
    "<script>", "alert(",             # Ataques XSS
    "404", "wp-admin", "admin.php"     # Escaneos de rutas buscando paneles de administración
]

def send_telegram_alert(log_line):
    """Envía un mensaje formateado a Telegram cuando salta la alarma"""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    
    message = (
        " *ALERTA DE SEGURIDAD DETECTADA* \n"
        "-------------------------------------\n"
        f" *Patrón sospechoso encontrado en los logs:*\n"
        f"`{log_line.strip()}`\n\n"
        " _Se recomienda revisar las IPs de origen en el servidor._"
    )
    
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Error al enviar alerta a Telegram: {e}")

def monitor_log():
    BANNER = r"""
        .__
      __|  |__   ____   ____     __       ____   ____
     / _  |  |  /  _ \ / ___\  _/  \__  /  _ \ / ___\
    |  |_|  |__(  <_> ) /_/  > \   __/_(  <_> ) /_/  >
     \____ |____\____/\___  /   \__/    \____/\___  /
          \/         /_____/                 /_____/
      [ G U A R D I Á N   D E   R E G I S T R O S ]
             -- by david-rtd | Blue Team Tool --
    """
    print(BANNER)
    print("\n🛡️ Guardián activo... Vigilando el archivo de logs.")
    print("-----------------------------------------------------")
    
    # Si el archivo no existe para la prueba, lo creamos vacío
    if not os.path.exists(LOG_FILE_PATH):
        with open(LOG_FILE_PATH, "w") as f:
            f.write("--- Inicio del registro de logs ---\n")

    # Abrimos el archivo y nos vamos al final del todo
    with open(LOG_FILE_PATH, "r") as file:
        file.seek(0, os.SEEK_END)
        
        while True:
            line = file.readline()
            if not line:
                time.sleep(1)  # Espera un segundo si no hay líneas nuevas
                continue
            
            # Analizamos si la nueva línea contiene algo peligroso
            lower_line = line.lower()
            for pattern in SUSPICIOUS_PATTERNS:
                if pattern in lower_line:
                    print(f" ¡Patrón sospechoso detectado!: {pattern}")
                    send_telegram_alert(line)
                    break # Evitamos enviar múltiples alertas por la misma línea

if __name__ == "__main__":
    try:
        monitor_log()
    except KeyboardInterrupt:
        print("\n\n🛡️ Guardián desactivado correctamente. ¡Hasta la próxima, guau guau 🐶!")

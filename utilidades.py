import datetime

# Archivo único de log para todo el sistema
ARCHIVO_LOG = "hospital_registro.log"

# Niveles / categorías de eventos
NIVEL_INFO     = "INFO"
NIVEL_CREAR    = "CREAR"
NIVEL_ELIMINAR = "ELIMINAR"
NIVEL_BUSCAR   = "BUSCAR"
NIVEL_CITA     = "CITA"
NIVEL_ERROR    = "ERROR"


def escribir_log(nivel: str, mensaje: str):
    """
    Función auxiliar para registrar eventos desde cualquier parte del sistema,
    no solo desde clases que hereden de LogMixin (ej: Hospital, GestorDatos).

    Formato: [YYYY-MM-DD HH:MM:SS] [NIVEL] mensaje
    """
    with open(ARCHIVO_LOG, "a", encoding="utf-8") as f:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] [{nivel}] {mensaje}\n")


class LogMixin:
    """
    Mixin de logging automático.
    Cualquier clase que herede de esto registrará sus acciones automáticamente.
    """
    def registrar_log(self, mensaje, nivel=NIVEL_CREAR):
        """Registra un evento. Categoría por defecto: CREAR."""
        escribir_log(nivel, mensaje)

import datetime

class LogMixin:
    """
    Mixin de logging automático.
    Cualquier clase que herede de esto registrará sus acciones automáticamente.
    """
    def registrar_log(self, mensaje):
        # REQUISITO: Gestión de archivos (with open) para logs
        with open("hospital_registro.log", "a", encoding="utf-8") as f:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{timestamp}] {mensaje}\n")

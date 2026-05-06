from entidades import Paciente, Medico


# ─────────────────────────────────────────
# REQUISITO: Excepciones personalizadas
# ─────────────────────────────────────────

class MedicoNoDisponibleError(Exception):
    """Se lanza cuando el médico ya tiene una cita en ese horario."""
    def __init__(self, medico, fecha_hora):
        super().__init__(
            f"El {medico} no está disponible el {fecha_hora}."
        )
        self.medico = medico
        self.fecha_hora = fecha_hora


class CitaDuplicadaError(Exception):
    """Se lanza cuando el paciente ya tiene una cita en ese horario."""
    def __init__(self, paciente, fecha_hora):
        super().__init__(
            f"{paciente} ya tiene una cita registrada el {fecha_hora}."
        )
        self.paciente = paciente
        self.fecha_hora = fecha_hora


# ─────────────────────────────────────────
# REQUISITO: Composición
# Cita "tiene un" Medico y "tiene un" Paciente
# ─────────────────────────────────────────

class Cita:
    def __init__(self, medico: Medico, paciente: Paciente, fecha_hora: str, motivo: str):
        """
        Parámetros:
            medico     : objeto Medico (de entidades.py)
            paciente   : objeto Paciente (de entidades.py)
            fecha_hora : string con formato 'DD/MM/YYYY HH:MM'
            motivo     : descripción breve de la consulta
        """
        self._validar_disponibilidad(medico, fecha_hora)
        self._validar_paciente(paciente, fecha_hora)

        self.medico = medico          # Composición: contiene un objeto Medico
        self.paciente = paciente      # Composición: contiene un objeto Paciente
        self.fecha_hora = fecha_hora
        self.motivo = motivo
        self.tratamiento = None       # Se asigna tras la consulta

        # Registrar cita en la agenda del médico (lista definida en entidades.py)
        medico.agenda.append(self)

    # ── Validaciones internas ──────────────────

    def _validar_disponibilidad(self, medico: Medico, fecha_hora: str):
        """Comprueba que el médico no tenga ya una cita en ese horario."""
        for cita in medico.agenda:
            if cita.fecha_hora == fecha_hora:
                raise MedicoNoDisponibleError(medico, fecha_hora)

    def _validar_paciente(self, paciente: Paciente, fecha_hora: str):
        """Comprueba que el paciente no tenga ya una cita en ese horario."""
        # Recorre la agenda de todos los médicos buscando al paciente
        # Nota: esto lo hace el módulo logica, sin tocar entidades.py
        pass  # La validación cruzada completa la implementa el Integrante 4
              # desde Hospital, que tiene acceso a todos los médicos.

    # ── REQUISITO: Métodos Mágicos ─────────────

    def __str__(self):
        return (
            f"Cita [{self.fecha_hora}] | "
            f"{self.medico} | "
            f"{self.paciente} | "
            f"Motivo: {self.motivo}"
        )

    def __repr__(self):
        return f"Cita(medico={self.medico.nombre!r}, paciente={self.paciente.nombre!r}, fecha={self.fecha_hora!r})"

    def __eq__(self, otra):
        """Dos citas son iguales si tienen el mismo médico, paciente y horario."""
        if not isinstance(otra, Cita):
            return NotImplemented
        return (
            self.medico.identificacion == otra.medico.identificacion
            and self.paciente._dni == otra.paciente._dni
            and self.fecha_hora == otra.fecha_hora
        )

    def __lt__(self, otra):
        """Permite ordenar citas cronológicamente con sorted()."""
        if not isinstance(otra, Cita):
            return NotImplemented
        return self.fecha_hora < otra.fecha_hora


# ─────────────────────────────────────────
# REQUISITO: Composición + lógica de costos
# Tratamiento "tiene una" Cita
# ─────────────────────────────────────────

class Tratamiento:
    # Tarifas base por tipo de tratamiento
    TARIFAS = {
        "consulta":    50.0,
        "cirugia":    400.0,
        "vacuna":      30.0,
        "analisis":    80.0,
        "revision":    40.0,
    }
    DESCUENTO_SEGURO = 0.40  # 40% de descuento para pacientes con seguro

    def __init__(self, cita: Cita, tipo: str, descripcion: str):
        """
        Parámetros:
            cita        : objeto Cita asociado a este tratamiento
            tipo        : clave de TARIFAS ('consulta', 'cirugia', etc.)
            descripcion : detalles clínicos del tratamiento
        """
        if tipo not in self.TARIFAS:
            raise ValueError(
                f"Tipo '{tipo}' no reconocido. "
                f"Opciones válidas: {list(self.TARIFAS.keys())}"
            )

        self.cita = cita              # Composición: contiene un objeto Cita
        self.tipo = tipo
        self.descripcion = descripcion
        self.cita.tratamiento = self  # Enlaza el tratamiento a la cita

    # ── Lógica de costos ──────────────────────

    def calcular_costo(self) -> float:
        """
        Calcula el costo final aplicando descuento si el paciente tiene seguro.
        Usa el atributo 'seguro' de Paciente definido en entidades.py.
        """
        tarifa_base = self.TARIFAS[self.tipo]
        if self.cita.paciente.seguro:
            return tarifa_base * (1 - self.DESCUENTO_SEGURO)
        return tarifa_base

    # ── REQUISITO: Métodos Mágicos ─────────────

    def __str__(self):
        costo = self.calcular_costo()
        seguro_txt = "con seguro" if self.cita.paciente.seguro else "sin seguro"
        return (
            f"Tratamiento: {self.tipo.capitalize()} | "
            f"{self.descripcion} | "
            f"Costo: {costo:.2f}€ ({seguro_txt})"
        )

    def __repr__(self):
        return f"Tratamiento(tipo={self.tipo!r}, costo={self.calcular_costo():.2f})"


# ─────────────────────────────────────────
# Bloque de prueba rápida (solo se ejecuta
# si corres este archivo directamente)
# ─────────────────────────────────────────

if __name__ == "__main__":
    # Crear objetos desde entidades.py
    medico   = Medico("Ana Torres", 45, "11111111A", 3500, "Cardiología", "COL-001")
    paciente = Paciente("Luis Gómez", 30, "22222222B", 75, 1.78, seguro=True)

    # Crear una cita (Composición en acción)
    cita = Cita(medico, paciente, "15/06/2025 10:00", "Revisión anual")
    print(cita)

    # Crear tratamiento y calcular costo
    tratamiento = Tratamiento(cita, "consulta", "Electrocardiograma + análisis")
    print(tratamiento)
    print(f"  → Costo calculado: {tratamiento.calcular_costo():.2f}€")

    # Probar excepción MedicoNoDisponibleError
    print("\nIntentando duplicar horario...")
    try:
        cita2 = Cita(medico, paciente, "15/06/2025 10:00", "Otra consulta")
    except MedicoNoDisponibleError as e:
        print(f"  Error capturado: {e}")

    # Probar ordenación con __lt__
    cita3 = Cita(medico, paciente, "20/06/2025 09:00", "Seguimiento")
    agenda_ordenada = sorted(medico.agenda)
    print("\nAgenda ordenada:")
    for c in agenda_ordenada:
        print(f"  {c}")

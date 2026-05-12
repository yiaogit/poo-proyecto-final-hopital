# hospital.py

from entidades import Persona, Paciente, Medico, DatoInvalidoError
from utilidades import escribir_log, NIVEL_CREAR, NIVEL_ELIMINAR, NIVEL_BUSCAR


class DniDuplicadoError(DatoInvalidoError):
    """Se lanza cuando se intenta registrar a alguien con un DNI ya existente."""
    pass


class PersonaNoEncontradaError(Exception):
    """Se lanza cuando se busca o intenta eliminar a alguien que no existe."""
    pass


class Hospital:
    def __init__(self, nombre):
        self.nombre = nombre
        # REQUISITO: Lista heterogénea. Aquí convivirán Médicos y Pacientes.
        self._directorio = []

    # ─────────────────────────────────────────
    # Operaciones CRUD
    # ─────────────────────────────────────────

    def agregar_persona(self, persona: Persona):
        """
        Agrega un paciente o médico al directorio.
        Lanza DniDuplicadoError si ya existe alguien con el mismo DNI.
        """
        # Verificación de unicidad de DNI (usa __eq__ de Persona)
        if self.buscar_por_dni(persona.dni, registrar=False) is not None:
            escribir_log(
                "ERROR",
                f"Intento de alta duplicada: ya existe alguien con DNI {persona.dni}."
            )
            raise DniDuplicadoError(
                f"Ya existe una persona registrada con DNI {persona.dni}."
            )
        self._directorio.append(persona)
        tipo = type(persona).__name__
        escribir_log(
            NIVEL_CREAR,
            f"Alta en directorio del hospital: {tipo} {persona.nombre} (DNI: {persona.dni})."
        )

    def eliminar_por_dni(self, dni: str) -> Persona:
        """
        Elimina del directorio a la persona con el DNI indicado.
        Devuelve la persona eliminada.
        Lanza PersonaNoEncontradaError si no existe.
        """
        persona = self.buscar_por_dni(dni, registrar=False)
        if persona is None:
            escribir_log(
                NIVEL_ELIMINAR,
                f"Intento de baja fallido: DNI {dni} no existe en el directorio."
            )
            raise PersonaNoEncontradaError(
                f"No existe ninguna persona con DNI {dni}."
            )
        self._directorio.remove(persona)
        tipo = type(persona).__name__
        escribir_log(
            NIVEL_ELIMINAR,
            f"Baja del directorio: {tipo} {persona.nombre} (DNI: {dni})."
        )
        return persona

    def buscar_por_dni(self, dni: str, registrar: bool = True) -> Persona:
        """
        Busca y devuelve a la persona con el DNI indicado, o None si no existe.
        `registrar=False` se usa internamente para no inundar el log
        con búsquedas auxiliares (ej. comprobación de duplicados en agregar).
        """
        dni_str = str(dni).strip()
        for persona in self._directorio:
            if persona.dni == dni_str:
                if registrar:
                    escribir_log(
                        NIVEL_BUSCAR,
                        f"Búsqueda exitosa: DNI {dni_str} corresponde a {persona.nombre}."
                    )
                return persona
        if registrar:
            escribir_log(NIVEL_BUSCAR, f"Búsqueda sin resultados para DNI {dni_str}.")
        return None

    # ─────────────────────────────────────────
    # Métodos mágicos
    # ─────────────────────────────────────────

    def __len__(self):
        """Permite usar len(hospital) para saber cuánta gente hay registrada."""
        return len(self._directorio)

    def __getitem__(self, index):
        """Permite iterar sobre el hospital (for p in hospital) o usar hospital[i]."""
        return self._directorio[index]

    def __contains__(self, dni: str) -> bool:
        """Permite usar 'dni in hospital' como atajo para comprobar existencia."""
        return self.buscar_por_dni(dni, registrar=False) is not None

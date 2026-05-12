# hospital.py

from entidades import Persona, Paciente, Medico

class Hospital:
    def __init__(self, nombre):
        self.nombre = nombre
        # REQUISITO: Lista heterogénea. Aquí convivirán Médicos y Pacientes.
        self._directorio = []

    def agregar_persona(self, persona: Persona):
        """Agrega un paciente o médico al directorio del hospital."""
        self._directorio.append(persona)

    # REQUISITO Integrante 4: Método mágico __len__
    def __len__(self):
        """Permite usar len(hospital) para saber cuánta gente hay registrada."""
        return len(self._directorio)

    # REQUISITO Integrante 4: Método mágico __getitem__
    def __getitem__(self, index):
        """Permite iterar sobre el hospital (for p in hospital) o usar hospital[i]."""
        return self._directorio[index]

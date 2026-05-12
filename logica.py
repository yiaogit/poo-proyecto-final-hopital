from entidades import Paciente, Medico
from datetime import datetime
from utilidades import escribir_log, NIVEL_CITA
 
 
class MedicoNoDisponibleError(Exception):
    def __init__(self, medico, fecha_hora):
        super().__init__(
            f"El {medico} no está disponible el {fecha_hora}."
        )
        self.medico = medico
        self.fecha_hora = fecha_hora
 
 
class CitaDuplicadaError(Exception):
    def __init__(self, paciente, fecha_hora):
        super().__init__(
            f"{paciente} ya tiene una cita registrada el {fecha_hora}."
        )
        self.paciente = paciente
        self.fecha_hora = fecha_hora
 


#________________________________________________________________________
 
class Cita:
    def __init__(self, medico: Medico, paciente: Paciente, fecha_hora: str, motivo: str,
                 validar_pasado: bool = True):
        


       
        if not isinstance(medico, Medico):
            raise TypeError("El parámetro 'medico' debe ser un objeto de la clase Medico.")
        if not isinstance(paciente, Paciente):
            raise TypeError("El parámetro 'paciente' debe ser un objeto de la clase Paciente.")
 


        self._validar_formato_fecha(fecha_hora, validar_pasado=validar_pasado)
 


        if not motivo or not motivo.strip():
            raise ValueError("El motivo de la cita no puede estar vacío ni contener solo espacios.")
        if len(motivo) > 100:
            raise ValueError("El motivo es demasiado largo (máximo 100 caracteres).")
 

        self._validar_disponibilidad(medico, fecha_hora)
        self._validar_paciente(paciente, fecha_hora)
 



        self.medico = medico
        self.paciente = paciente
        self.fecha_hora = fecha_hora                                  

        self._fecha_obj = datetime.strptime(fecha_hora, "%d/%m/%Y %H:%M")
        self.motivo = motivo.strip() 
        self.tratamiento = None
 


        medico.agenda.append(self)
        paciente.agenda.append(self)



        if validar_pasado:
            escribir_log(
                NIVEL_CITA,
                f"Cita programada: {paciente.nombre} con {medico.nombre} "
                f"el {fecha_hora} — motivo: {self.motivo}"
            )
 
#________________________________________________________________________



    def _validar_formato_fecha(self, fecha_hora: str, validar_pasado: bool = True):


        try:
            fecha_obj = datetime.strptime(fecha_hora, "%d/%m/%Y %H:%M")
            

            if validar_pasado and fecha_obj < datetime.now():
                 raise ValueError("No se pueden programar citas en el pasado.")
                 
        except ValueError as e:


            if "pasado" in str(e):
                raise e
            raise ValueError("Formato de fecha inválido. Debe ser 'DD/MM/YYYY HH:MM' (ej. 15/06/2026 10:00).")
 
    def _validar_disponibilidad(self, medico: Medico, fecha_hora: str):


        nueva = datetime.strptime(fecha_hora, "%d/%m/%Y %H:%M")
        for cita in medico.agenda:
            if cita._fecha_obj == nueva:
                raise MedicoNoDisponibleError(medico, fecha_hora)
 
    def _validar_paciente(self, paciente: Paciente, fecha_hora: str):


        nueva = datetime.strptime(fecha_hora, "%d/%m/%Y %H:%M")
        for cita in paciente.agenda:
            if cita._fecha_obj == nueva:
                raise CitaDuplicadaError(paciente, fecha_hora)
 

 
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

        if not isinstance(otra, Cita):
            return NotImplemented
        

        return (
            self.medico.identificacion == otra.medico.identificacion
            and self.paciente._dni == otra.paciente._dni
            and self.fecha_hora == otra.fecha_hora
        )
 
    def __lt__(self, otra):


        if not isinstance(otra, Cita):
            return NotImplemented
        return self._fecha_obj < otra._fecha_obj
 
 
#_______________________________________________________________________-
 
class Tratamiento:
    TARIFAS = {
        "consulta":    50.0,
        "cirugia":    400.0,
        "vacuna":      30.0,
        "analisis":    80.0,
        "revision":    40.0,
    }
    DESCUENTO_SEGURO = 0.40 
 
    def __init__(self, cita: Cita, tipo: str, descripcion: str):
        
        if tipo not in self.TARIFAS:
            raise ValueError(
                f"Tipo '{tipo}' no reconocido. "
                f"Opciones válidas: {list(self.TARIFAS.keys())}"
            )
 
        self.cita = cita              
        self.tipo = tipo

        self.descripcion = descripcion


        self.cita.tratamiento = self

        escribir_log(
            NIVEL_CITA,
            f"Tratamiento '{tipo}' asociado a la cita de {cita.paciente.nombre} "
            f"({cita.fecha_hora}) — coste: {self.calcular_costo():.2f}€"
        )
 
#______________________________________________________ 
    def calcular_costo(self) -> float:
        

        tarifa_base = self.TARIFAS[self.tipo]
        if self.cita.paciente.seguro:
            return tarifa_base * (1 - self.DESCUENTO_SEGURO)
        return tarifa_base
 
 
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
 
 

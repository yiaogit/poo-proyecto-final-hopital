def __init__(self, nombre, edad, dni):
        self.nombre = nombre
        self.edad = edad
        self._dni = dni

    @property
    def edad(self):
        return self._edad

    @edad.setter
    def edad(self, valor):
        if valor < 0 or valor > 120:
            raise ValueError(f'La edad {valor} no es valida')
        self._edad = valor

    def mostrar_datos(self):
        pass

class Paciente(Persona):
    def __init__(self, nombre, edad, dni, peso, altura, seguro=False):
        super().__init__(nombre, edad, dni)
        self.peso = peso
        self.altura = altura
        self.seguro = seguro
        #self.registrar_log(f"Nuevo paciente creado: {self.nombre} (DNI: {self._dni})")


    def __str__(self):
        return f"Paciente: {self.nombre} [DNI: {self._dni}]"

    def mostrar_datos(self):
      if self.seguro == True:
        estado_seguro = "Con seguro"
      else:
        estado_seguro = "Sin seguro"
      return f"{self.__str__()} - {estado_seguro} - IMC: {round(self.peso / (self.altura**2), 2)}"

class Medico(Persona):
    def __init__(self, nombre, edad, dni, salario, especialidad, identificacion):
        super().__init__(nombre, edad, dni)
        self._salario = salario
        self.especialidad = especialidad
        self.identificacion = identificacion
        self.agenda = []  # Lista que llenará la Persona 2 con objetos Cita

    def __str__(self):
        return f"Dr./Dra. {self.nombre} ({self.especialidad})"

    def mostrar_datos(self):
        return f"{self.__str__()} - ID Colegiado: {self.identificacion}"
  

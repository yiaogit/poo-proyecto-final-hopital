from utilidades import LogMixin

class DatoInvalidoError(Exception):
    pass

class Persona:
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

    @property
    def dni(self):
        return self._dni

    def __eq__(self, other):
        if not isinstance(other, Persona):
            return NotImplemented
        return self._dni == other._dni
        
    def __lt__(self, other):
        if not isinstance(other, Persona):
            return NotImplemented
        return self.nombre < other.nombre

    def mostrar_datos(self):
        return 'Datos de la persona'
        

class Paciente(Persona, LogMixin):
    def __init__(self, nombre, edad, dni, peso, altura, seguro=False):
        super().__init__(nombre, edad, dni)
        self.peso = peso
        self.altura = altura
        self.seguro = seguro
        self.agenda = []
        self.registrar_log(f"Nuevo paciente creado: {self.nombre} (DNI: {self._dni})")

    @property
    def peso(self):
        return self._peso

    @peso.setter
    def peso(self, valor):
        if valor <= 0:
            raise DatoInvalidoError(f'La peso {valor} debe ser un numero positivo')
        self._peso = valor

    @property
    def altura(self):
        return self._altura

    @altura.setter
    def altura(self, valor):
        if valor <= 0:
            raise DatoInvalidoError(f'La altura {valor} debe ser un numero positivo')
        self._altura = valor

    @property
    def imc(self):
        return round(self._peso / (self._altura**2), 2)

    def __str__(self):
        return f"Paciente: {self.nombre} [DNI: {self._dni}]"

    def mostrar_datos(self):
        if self.seguro == True:
            estado_seguro = "Con seguro"
        else:
            estado_seguro = "Sin seguro"
        return (
            f"{self}\n"
            f"  Edad  : {self._edad} años\n"
            f"  Seguro: {estado_seguro}\n"
            f"  IMC   : {self.imc} (peso={self._peso}kg, altura={self._altura}m)"
        )
        
    @classmethod
    def desde_csv(cls, linea_csv):
        datos = linea_csv.strip().split(",")
        
        return cls(
            nombre=datos[0],
            edad=int(datos[1]),
            dni=datos[2],
            peso=float(datos[3]),
            altura=float(datos[4]),
            seguro=(datos[5] == "True")
        )
        
        
class Medico(Persona):
    def __init__(self, nombre, edad, dni, salario, especialidad, identificacion):
        super().__init__(nombre, edad, dni)
        self.salario = salario
        self.especialidad = especialidad
        self.identificacion = identificacion
        self.agenda = [] 
    
    @property
    def salario(self):
        return self._salario

    @salario.setter
    def salario(self, valor):
        if valor < 0:
            raise DatoInvalidoError(f'El salario {valor} no es puede ser negativo')
        self._salario = valor
   
    
    def __str__(self):
        return f"Dr./Dra. {self.nombre} ({self.especialidad})"

    def mostrar_datos(self):
        return (
            f"{self}\n"
            f"  Edad         : {self._edad} años\n"
            f"  ID Colegiado : {self.identificacion}\n"
        )

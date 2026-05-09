from utilidades import LogMixin

#Excepcion personalizada
class DatoInvalidoError(Exception):
    pass


#Clase base Persona
class Persona:
    def __init__(self, nombre, edad, dni):
        self.nombre = nombre
        self.edad = edad    #usa el setter para validar que sea 0-120
        self._dni = dni     #atributo proteido (solo tiene getter)
    
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

    #Metodos magicos
    #dos personas son iguales si tienen el mismo dni
    def __eq__(self, other):
        if not isinstance(other, Persona):
            return NotImplemented
        return self._dni == other._dni

    #ordena alfabeticamente por nombre
    def __lt__(self, other):
        if not isinstance(other, Persona):
            return NotImplemented
        return self.nombre < other.nombre

    #sobreescrito por Paciente y Medico (polimorfismo) 
    def mostrar_datos(self):
        return 'Datos de la persona'


#Clase Paciente
class Paciente(Persona, LogMixin):
    def __init__(self, nombre, edad, dni, peso, altura, seguro=False):
        super().__init__(nombre, edad, dni)
        self.peso = peso        #usa el setter para validar que sea positivo
        self.altura = altura    #usa el setter para validar que sea positivo
        self.seguro = seguro    #True si tiene seguro mediso, False si no
        self.agenda = []        #lista de citas que rellena el modulo logica.py

        #registra automaticamente el paciente (Mixin)
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

    #atributo calculado
    @property
    def imc(self):
        return round(self._peso / (self._altura**2), 2)

    #como se muestra el objeto al imprimir
    def __str__(self):
        return f"Paciente: {self.nombre} [DNI: {self._dni}]"

    #sobreescribe el de Persona (polimorfismo)
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

    #Patron Factory
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


#Clase Medico
class Medico(Persona):
    def __init__(self, nombre, edad, dni, salario, especialidad, identificacion):
        super().__init__(nombre, edad, dni)
        self.salario = salario               #usa el setter para validar que no sea negativo
        self.especialidad = especialidad   
        self.identificacion = identificacion
        self.agenda = []                     #lista de citas que rellena el modulo logica.py
    
    @property
    def salario(self):
        return self._salario

    @salario.setter
    def salario(self, valor):
        if valor < 0:
            raise DatoInvalidoError(f'El salario {valor} no es puede ser negativo')
        self._salario = valor
   
    #como se muestra el objeto al imprimir
    def __str__(self):
        return f"Dr./Dra. {self.nombre} ({self.especialidad})"

    #sobreescribe el de Persona (polimorfismo)
    def mostrar_datos(self):
        return (
            f"{self}\n"
            f"  Edad         : {self._edad} años\n"
            f"  ID Colegiado : {self.identificacion}\n"
        )

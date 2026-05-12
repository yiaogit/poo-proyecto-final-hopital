from utilidades import LogMixin

#Excepcion personalizada
class DatoInvalidoError(Exception):
    pass


#Clase base Persona
class Persona:
    def __init__(self, nombre, edad, dni):
        self.nombre = nombre
        self.edad = edad    #usa el setter para validar que sea 0-120
        self._dni = dni     #atributo protegido (solo tiene getter)
    
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
    
    def __hash__(self):
        return hash(self._dni)

    #sobreescrito por Paciente y Medico (polimorfismo) 
    def mostrar_datos(self):
        return 'Datos de la persona'


# Clase Paciente: Representa a un usuario del sistema hospitalario
# Hereda de Persona (Atributos base) y LogMixin (Capacidad de auditoría)
class Paciente(Persona, LogMixin):
    def __init__(self, nombre, edad, dni, peso, altura, seguro=False, es_nuevo=True):
        # Inicialización de la clase base Persona
        super().__init__(nombre, edad, dni)
        
        # Uso de setters para garantizar la integridad de los datos desde el inicio
        self.peso = peso        
        self.altura = altura    
        self.seguro = seguro    
        self.agenda = []        # Lista heterogénea de citas asociadas

        # Lógica de logging: Solo registra si es un ingreso nuevo, no una carga de DB
        if es_nuevo:
            self.registrar_log(f"Nuevo paciente creado: {self.nombre} (DNI: {self._dni})")

    # --- Encapsulamiento con Validación ---

    @property
    def peso(self):
        return self._peso

    @peso.setter
    def peso(self, valor):
        if valor <= 0:
            raise DatoInvalidoError(f'El peso ({valor}kg) debe ser un número positivo')
        self._peso = valor

    @property
    def altura(self):
        return self._altura

    @altura.setter
    def altura(self, valor):
        if valor <= 0:
            raise DatoInvalidoError(f'La altura ({valor}m) debe ser un número positivo')
        self._altura = valor

    # --- Atributos Calculados (Lógica de Negocio) ---

    @property
    def imc(self):
        """Calcula el Índice de Masa Corporal de forma dinámica."""
        return round(self._peso / (self._altura**2), 2)

    def clasificar_imc(self):
        """Proporciona una interpretación clínica del IMC (Toque de Data Science)."""
        valor = self.imc
        if valor < 18.5: return "Bajo peso"
        if 18.5 <= valor < 25: return "Peso normal"
        if 25 <= valor < 30: return "Sobrepeso"
        return "Obesidad"
    
    # --- Representación y Polimorfismo ---

    def __str__(self):
        return f"Paciente: {self.nombre} [DNI: {self._dni}]"

    def mostrar_datos(self):
        """Presentación elegante de la ficha médica del paciente."""
        estado_seguro = "✅ Con seguro médico" if self.seguro else "❌ Sin seguro médico"
        
        return (
            f"{'='*40}\n"
            f"{self}\n"
            f"{'-'*40}\n"
            f" 📋 DATOS GENERALES\n"
            f"    • Edad: {self._edad} años\n"
            f"    • Póliza: {estado_seguro}\n"
            f" ⚖️ MÉTRICAS FÍSICAS\n"
            f"    • Peso/Altura: {self._peso}kg / {self._altura}m\n"
            f"    • IMC Actual: {self.imc} -> [{self.clasificar_imc()}]\n"
            f"{'='*40}"
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
            seguro=(datos[5] == "True"),
            es_nuevo=False
        )


# Clase Medico actualizada con validaciones de seguridad
class Medico(Persona, LogMixin): 
    # 2. Se añade el parámetro por defecto 'es_nuevo=True' para controlar el registro
    def __init__(self, nombre, edad, dni, salario, especialidad, identificacion, es_nuevo=True):
        # Llama al constructor de la clase padre (Persona)
        super().__init__(nombre, edad, dni)
        
        # Al asignar a través de 'self.', se activan automáticamente las validaciones de los @setters
        self.salario = salario               
        self.especialidad = especialidad     
        self.identificacion = identificacion 
        self.agenda = []                     

        # 3. Registro automático en el log (Utiliza el método heredado de LogMixin)
        if es_nuevo:
            self.registrar_log(f"Nuevo médico registrado: Dr./Dra. {self.nombre} (Especialidad: {self._especialidad}, ID: {self._identificacion})")
    
    # --- Propiedades y Encapsulamiento ---

    @property
    def salario(self):
        return self._salario

    @salario.setter
    def salario(self, valor):
        if valor < 0:
            raise DatoInvalidoError(f'El salario {valor} no puede ser negativo.')
        self._salario = valor
   
    @property
    def especialidad(self):
        return self._especialidad

    @especialidad.setter
    def especialidad(self, valor):
        # Valida que la cadena no esté vacía ni contenga solo espacios
        if not valor or not valor.strip():
            raise DatoInvalidoError("La especialidad médica no puede estar vacía.")
        self._especialidad = valor.strip()

    @property
    def identificacion(self):
        return self._identificacion

    @identificacion.setter
    def identificacion(self, valor):
        if not valor or not valor.strip():
            raise DatoInvalidoError("El ID de colegiado no puede estar vacío.")
        self._identificacion = valor.strip()

    # --- Métodos Mágicos y Polimorfismo ---

    # Representación en cadena del objeto
    def __str__(self):
        return f"Dr./Dra. {self.nombre} ({self.especialidad})"

    # Sobreescribe el método de la clase base Persona (Polimorfismo)
    def mostrar_datos(self):
        """Presentación elegante de la ficha profesional del médico."""
        # 逻辑处理：如果日程为空，显示提示信息
        resumen_agenda = f"{len(self.agenda)} citas programadas" if self.agenda else "Sin citas pendientes"
        
        return (
            f"{'='*40}\n"
            f"{self}\n"  # 调用 __str__ 显示姓名和科室
            f"{'-'*40}\n"
            f" 👨‍⚕️ INFORMACIÓN PROFESIONAL\n"
            f"    • Edad         : {self._edad} años\n"
            f"    • ID Colegiado : {self.identificacion}\n"
            f"    • Salario Mens.: {self.salario:.2f} €\n" # :.2f 保证显示两位小数
            f" 📅 AGENDA Y TURNOS\n"
            f"    • Estado       : {resumen_agenda}\n"
            f"{'='*40}"
        )

    # --- Patrones de Diseño ---

    # Patrón Factory para instanciar objetos a partir de un archivo CSV
    @classmethod
    def desde_csv(cls, linea_csv):
        datos = linea_csv.strip().split(",")
        return cls(
            nombre=datos[0],
            edad=int(datos[1]),
            dni=datos[2],
            salario=float(datos[3]),
            especialidad=datos[4],
            identificacion=datos[5],
            # 4. CLAVE: Evita generar logs duplicados al cargar datos históricos
            es_nuevo=False  
        )

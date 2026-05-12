from utilidades import LogMixin

#Excepcion personalizada
class DatoInvalidoError(Exception):
    pass


#Clase base Persona
class Persona:
    def __init__(self, nombre, edad, dni):
        self.nombre = nombre
        self.edad = edad    #Usa el setter para validar que sea 0-120
        #Validación de DNI: no puede estar vacío
        if not dni or not str(dni).strip():
            raise DatoInvalidoError("El DNI no puede estar vacío.")
        self._dni = str(dni).strip()
    
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
    #Dos personas son iguales si tienen el mismo dni
    def __eq__(self, other):
        if not isinstance(other, Persona):
            return NotImplemented
        return self._dni == other._dni

    #Ordena alfabeticamente por nombre
    def __lt__(self, other):
        if not isinstance(other, Persona):
            return NotImplemented
        return self.nombre < other.nombre

    #Permite usar el objeto en sets y evita duplicados basados en el DNI
    def __hash__(self):
        return hash(self._dni)

    #sobreescrito por Paciente y Medico (polimorfismo) 
    def mostrar_datos(self):
        return 'Datos de la persona'


#Clase Paciente, hereda de Persona (Atributos base) y LogMixin (Capacidad de auditoría)
class Paciente(Persona, LogMixin):
    def __init__(self, nombre, edad, dni, peso, altura, seguro=False, es_nuevo=True):
        super().__init__(nombre, edad, dni)
        #Uso de setters para validar los datos
        self.peso = peso        
        self.altura = altura    
        self.seguro = seguro    
        self.agenda = []        #Lista heterogénea de citas asociadas

        #Lógica de logging: Solo registra si es un ingreso nuevo
        if es_nuevo:
            self.registrar_log(f"Nuevo paciente creado: {self.nombre} (DNI: {self._dni})")

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

    #Atributo calculado (Índice de Masa Corporal)
    @property
    def imc(self):
        return round(self._peso / (self._altura**2), 2)

    def clasificar_imc(self):
        valor = self.imc
        if valor < 18.5: return "Bajo peso"
        if 18.5 <= valor < 25: return "Peso normal"
        if 25 <= valor < 30: return "Sobrepeso"
        return "Obesidad"
    
    def __str__(self):
        return f"Paciente: {self.nombre} [DNI: {self._dni}]"

    def resumen(self):
        """Línea breve para listados paginados."""
        seguro_icon = "🛡️" if self.seguro else "  "
        return (
            f"{seguro_icon} {self.nombre:<28} DNI: {self._dni:<11} "
            f"Edad: {self._edad:>3}  IMC: {self.imc:>5} [{self.clasificar_imc()}]"
        )

    #sobreescribe el metodo de Persona (polimorfismo)
    def mostrar_datos(self):
        estado_seguro = "✅ Con seguro médico" if self.seguro else "❌ Sin seguro médico"

        #Sección de agenda: si hay citas, las listamos cronológicamente
        if self.agenda:
            citas_ordenadas = sorted(self.agenda)
            lineas_citas = []
            for c in citas_ordenadas:
                trat = f" → {c.tratamiento.tipo}" if c.tratamiento else ""
                lineas_citas.append(
                    f"    • {c.fecha_hora} con {c.medico.nombre}{trat}"
                )
            seccion_agenda = "\n".join(lineas_citas)
        else:
            seccion_agenda = "    • Sin citas programadas"

        return (
            f"{'='*50}\n"
            f"{self}\n"
            f"{'-'*50}\n"
            f" 📋 DATOS GENERALES\n"
            f"    • Edad: {self._edad} años\n"
            f"    • Póliza: {estado_seguro}\n"
            f" ⚖️ MÉTRICAS FÍSICAS\n"
            f"    • Peso/Altura: {self._peso}kg / {self._altura}m\n"
            f"    • IMC Actual: {self.imc} -> [{self.clasificar_imc()}]\n"
            f" 📅 AGENDA ({len(self.agenda)} cita(s))\n"
            f"{seccion_agenda}\n"
            f"{'='*50}"
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


#Clase Medico, hereda de Persona y LogMixin
class Medico(Persona, LogMixin): 
    def __init__(self, nombre, edad, dni, salario, especialidad, identificacion, es_nuevo=True):
        super().__init__(nombre, edad, dni)
        #Uso de setters para validar los datos
        self.salario = salario               
        self.especialidad = especialidad     
        self.identificacion = identificacion 
        self.agenda = []        #Lista heterogénea de citas asociadas

        #Registro automático en el log si es ingreso nuevo
        if es_nuevo:
            self.registrar_log(f"Nuevo médico registrado: Dr./Dra. {self.nombre} (Especialidad: {self._especialidad}, ID: {self._identificacion})")
    
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

    #Representación en cadena del objeto
    def __str__(self):
        return f"Dr./Dra. {self.nombre} ({self.especialidad}) [ID: {self.identificacion} · DNI: {self._dni}]"

    def resumen(self):
        return (
            f"🩺 {self.nombre:<28} ID: {self.identificacion:<10} "
            f"DNI: {self._dni:<11} {self.especialidad:<18} "
            f"({len(self.agenda)} cita(s))"
        )

    #Sobreescribe el método de la clase base Persona (polimorfismo)
    def mostrar_datos(self):
        if self.agenda:
            citas_ordenadas = sorted(self.agenda)
            lineas_citas = []
            for c in citas_ordenadas:
                trat = f" → {c.tratamiento.tipo}" if c.tratamiento else ""
                lineas_citas.append(
                    f"    • {c.fecha_hora} — paciente {c.paciente.nombre}{trat}"
                )
            seccion_agenda = "\n".join(lineas_citas)
        else:
            seccion_agenda = "    • Sin citas pendientes"

        return (
            f"{'='*50}\n"
            f"{self}\n"
            f"{'-'*50}\n"
            f" 👨‍⚕️ INFORMACIÓN PROFESIONAL\n"
            f"    • Edad         : {self._edad} años\n"
            f"    • DNI          : {self._dni}\n"
            f"    • ID Colegiado : {self.identificacion}\n"
            f"    • Especialidad : {self.especialidad}\n"
            f"    • Salario Mens.: {self.salario:.2f} €\n"
            f" 📅 AGENDA ({len(self.agenda)} cita(s))\n"
            f"{seccion_agenda}\n"
            f"{'='*50}"
        )

    #Patrón Factory para instanciar objetos a partir de un archivo CSV
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
            es_nuevo=False  
        )

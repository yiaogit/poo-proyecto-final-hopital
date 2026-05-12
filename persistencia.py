import os

class GestorDatos:
    """
    Clase responsable de guardar y cargar los datos del hospital.
    No necesita ser instanciada, usa métodos estáticos.
    """
    ARCHIVO_PACIENTES = "pacientes_db.csv"
    ARCHIVO_MEDICOS = "medicos_db.csv"  # 🆕 Nuevo archivo exclusivo para médicos

    # ─────────────────────────────────────────
    # MÉTODOS PARA PACIENTES
    # ─────────────────────────────────────────

    @staticmethod
    def guardar_pacientes(lista_pacientes):
        """
        REQUISITO: Gestión de archivos (with open).
        Guarda la lista de objetos Paciente en un archivo CSV.
        """
        with open(GestorDatos.ARCHIVO_PACIENTES, "w", encoding="utf-8") as f:
            for p in lista_pacientes:
                # Se asume la estructura definida con Integrante 1
                linea = f"{p.nombre},{p.edad},{p._dni},{p.peso},{p.altura},{p.seguro}\n"
                f.write(linea)
        print(f"✅ Se guardaron {len(lista_pacientes)} pacientes en la base de datos.")

    @staticmethod
    def cargar_pacientes(clase_paciente):
        """
        Lee el archivo CSV y reconstruye los objetos Paciente.
        Recibe la clase 'Paciente' como argumento para evitar importaciones circulares.
        """
        pacientes_recuperados = []
        if not os.path.exists(GestorDatos.ARCHIVO_PACIENTES):
            print("⚠️ No hay base de datos previa de pacientes. Iniciando desde cero.")
            return pacientes_recuperados

        with open(GestorDatos.ARCHIVO_PACIENTES, "r", encoding="utf-8") as f:
            for linea in f:
                if linea.strip():
                    # REQUISITO: Llama al Factory Method de la clase
                    nuevo_paciente = clase_paciente.desde_csv(linea)
                    pacientes_recuperados.append(nuevo_paciente)
                    
        print(f"📂 Se cargaron {len(pacientes_recuperados)} pacientes exitosamente.")
        return pacientes_recuperados

    # ─────────────────────────────────────────
    # 🆕 MÉTODOS PARA MÉDICOS (Nueva implementación)
    # ─────────────────────────────────────────

    @staticmethod
    def guardar_medicos(lista_medicos):
        """
        Guarda la lista de objetos Medico en su propio archivo CSV.
        """
        with open(GestorDatos.ARCHIVO_MEDICOS, "w", encoding="utf-8") as f:
            for m in lista_medicos:
                # Orden basado en los atributos de la clase Medico
                linea = f"{m.nombre},{m.edad},{m._dni},{m.salario},{m.especialidad},{m.identificacion}\n"
                f.write(linea)
        print(f"✅ Se guardaron {len(lista_medicos)} médicos en la base de datos.")

    @staticmethod
    def cargar_medicos(clase_medico):
        """
        Lee el archivo CSV y reconstruye los objetos Medico.
        Recibe la clase 'Medico' para usar su Factory Method.
        """
        medicos_recuperados = []
        if not os.path.exists(GestorDatos.ARCHIVO_MEDICOS):
            print("⚠️ No hay base de datos previa de médicos. Iniciando desde cero.")
            return medicos_recuperados

        with open(GestorDatos.ARCHIVO_MEDICOS, "r", encoding="utf-8") as f:
            for linea in f:
                if linea.strip():
                    # Llama a Medico.desde_csv()
                    nuevo_medico = clase_medico.desde_csv(linea)
                    medicos_recuperados.append(nuevo_medico)
                    
        print(f"📂 Se cargaron {len(medicos_recuperados)} médicos exitosamente.")
        return medicos_recuperados

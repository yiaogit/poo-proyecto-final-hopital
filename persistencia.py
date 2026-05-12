import os
from utilidades import escribir_log, NIVEL_INFO, NIVEL_CITA, NIVEL_ERROR


class GestorDatos:
    """
    Clase responsable de guardar y cargar los datos del hospital.
    No necesita ser instanciada, usa métodos estáticos.
    """
    ARCHIVO_PACIENTES = "pacientes_db.csv"
    ARCHIVO_MEDICOS   = "medicos_db.csv"
    ARCHIVO_CITAS     = "citas_db.csv"

    # ─────────────────────────────────────────
    # MÉTODOS PARA PACIENTES
    # ─────────────────────────────────────────

    @staticmethod
    def guardar_pacientes(lista_pacientes):
        """Guarda la lista de objetos Paciente en CSV."""
        with open(GestorDatos.ARCHIVO_PACIENTES, "w", encoding="utf-8") as f:
            for p in lista_pacientes:
                linea = f"{p.nombre},{p.edad},{p.dni},{p.peso},{p.altura},{p.seguro}\n"
                f.write(linea)
        escribir_log(NIVEL_INFO, f"Persistidos {len(lista_pacientes)} pacientes en {GestorDatos.ARCHIVO_PACIENTES}.")
        print(f"✅ Se guardaron {len(lista_pacientes)} pacientes en la base de datos.")

    @staticmethod
    def cargar_pacientes(clase_paciente):
        """Lee el CSV y reconstruye los objetos Paciente."""
        pacientes_recuperados = []
        if not os.path.exists(GestorDatos.ARCHIVO_PACIENTES):
            print("⚠️ No hay base de datos previa de pacientes. Iniciando desde cero.")
            return pacientes_recuperados

        with open(GestorDatos.ARCHIVO_PACIENTES, "r", encoding="utf-8") as f:
            for linea in f:
                if linea.strip():
                    nuevo_paciente = clase_paciente.desde_csv(linea)
                    pacientes_recuperados.append(nuevo_paciente)

        escribir_log(NIVEL_INFO, f"Cargados {len(pacientes_recuperados)} pacientes desde {GestorDatos.ARCHIVO_PACIENTES}.")
        print(f"📂 Se cargaron {len(pacientes_recuperados)} pacientes exitosamente.")
        return pacientes_recuperados

    # ─────────────────────────────────────────
    # MÉTODOS PARA MÉDICOS
    # ─────────────────────────────────────────

    @staticmethod
    def guardar_medicos(lista_medicos):
        """Guarda la lista de objetos Medico en su propio CSV."""
        with open(GestorDatos.ARCHIVO_MEDICOS, "w", encoding="utf-8") as f:
            for m in lista_medicos:
                linea = f"{m.nombre},{m.edad},{m.dni},{m.salario},{m.especialidad},{m.identificacion}\n"
                f.write(linea)
        escribir_log(NIVEL_INFO, f"Persistidos {len(lista_medicos)} médicos en {GestorDatos.ARCHIVO_MEDICOS}.")
        print(f"✅ Se guardaron {len(lista_medicos)} médicos en la base de datos.")

    @staticmethod
    def cargar_medicos(clase_medico):
        """Lee el CSV y reconstruye los objetos Medico."""
        medicos_recuperados = []
        if not os.path.exists(GestorDatos.ARCHIVO_MEDICOS):
            print("⚠️ No hay base de datos previa de médicos. Iniciando desde cero.")
            return medicos_recuperados

        with open(GestorDatos.ARCHIVO_MEDICOS, "r", encoding="utf-8") as f:
            for linea in f:
                if linea.strip():
                    nuevo_medico = clase_medico.desde_csv(linea)
                    medicos_recuperados.append(nuevo_medico)

        escribir_log(NIVEL_INFO, f"Cargados {len(medicos_recuperados)} médicos desde {GestorDatos.ARCHIVO_MEDICOS}.")
        print(f"📂 Se cargaron {len(medicos_recuperados)} médicos exitosamente.")
        return medicos_recuperados

    # ─────────────────────────────────────────
    # MÉTODOS PARA CITAS
    # ─────────────────────────────────────────
    # Formato de cada línea:
    # dni_paciente,id_medico,fecha_hora,motivo,tipo_tratamiento,descripcion_tratamiento
    # Si la cita no tiene tratamiento, los dos últimos campos quedan vacíos.

    @staticmethod
    def guardar_citas(lista_citas):
        """
        Guarda las citas en CSV.
        Las citas no se persistían antes — ahora se conservan entre sesiones.
        """
        with open(GestorDatos.ARCHIVO_CITAS, "w", encoding="utf-8") as f:
            for c in lista_citas:
                if c.tratamiento is not None:
                    tipo = c.tratamiento.tipo
                    desc = c.tratamiento.descripcion.replace(",", " ")  # protección básica
                else:
                    tipo, desc = "", ""
                # Sanitizamos también el motivo por si el usuario metió una coma
                motivo_limpio = c.motivo.replace(",", " ")
                linea = f"{c.paciente.dni},{c.medico.identificacion},{c.fecha_hora},{motivo_limpio},{tipo},{desc}\n"
                f.write(linea)
        escribir_log(NIVEL_CITA, f"Persistidas {len(lista_citas)} citas en {GestorDatos.ARCHIVO_CITAS}.")
        print(f"✅ Se guardaron {len(lista_citas)} citas en la base de datos.")

    @staticmethod
    def cargar_citas(hospital, clase_cita, clase_tratamiento):
        """
        Lee las citas del CSV y las reconstruye, vinculándolas a los médicos
        y pacientes ya existentes en el hospital.

        Devuelve la lista de citas cargadas. Las citas que no se puedan
        reconstruir (porque falta el médico o el paciente) se omiten con
        un aviso en el log.
        """
        citas_recuperadas = []
        if not os.path.exists(GestorDatos.ARCHIVO_CITAS):
            print("⚠️ No hay base de datos previa de citas. Iniciando desde cero.")
            return citas_recuperadas

        from entidades import Paciente, Medico   # import local para evitar ciclos

        with open(GestorDatos.ARCHIVO_CITAS, "r", encoding="utf-8") as f:
            for n_linea, linea in enumerate(f, 1):
                if not linea.strip():
                    continue
                partes = linea.strip().split(",")
                if len(partes) < 4:
                    escribir_log(NIVEL_ERROR, f"Línea {n_linea} de citas malformada: {linea!r}")
                    continue

                # Rellenamos los campos opcionales si faltan
                while len(partes) < 6:
                    partes.append("")

                dni_pac, id_med, fecha_hora, motivo, tipo_trat, desc_trat = partes[:6]

                # Resolvemos médico y paciente por sus identificadores
                paciente = hospital.buscar_por_dni(dni_pac, registrar=False)
                medico = next(
                    (m for m in hospital
                     if isinstance(m, Medico) and m.identificacion == id_med),
                    None
                )

                if paciente is None or not isinstance(paciente, Paciente):
                    escribir_log(NIVEL_ERROR, f"Cita ignorada: paciente DNI {dni_pac} no existe.")
                    continue
                if medico is None:
                    escribir_log(NIVEL_ERROR, f"Cita ignorada: médico ID {id_med} no existe.")
                    continue

                try:
                    cita = clase_cita(medico, paciente, fecha_hora, motivo, validar_pasado=False)
                    if tipo_trat:
                        clase_tratamiento(cita, tipo_trat, desc_trat or "Restaurado desde CSV")
                    citas_recuperadas.append(cita)
                except Exception as e:
                    escribir_log(NIVEL_ERROR, f"No se pudo restaurar cita en línea {n_linea}: {e}")

        escribir_log(NIVEL_CITA, f"Cargadas {len(citas_recuperadas)} citas desde {GestorDatos.ARCHIVO_CITAS}.")
        print(f"📂 Se cargaron {len(citas_recuperadas)} citas exitosamente.")
        return citas_recuperadas

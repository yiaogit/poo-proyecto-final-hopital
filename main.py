# -*- coding: utf-8 -*-
"""
Módulo Principal (main.py)
Punto de entrada del programa. Gestiona la interfaz de usuario por consola
y coordina los módulos de entidades, lógica, persistencia y contenedor.
"""

from entidades import Paciente, Medico, DatoInvalidoError
from persistencia import GestorDatos
from logica import Cita, Tratamiento, MedicoNoDisponibleError, CitaDuplicadaError
from hospital import Hospital, DniDuplicadoError, PersonaNoEncontradaError


def _recolectar_citas(hospital):
    """Recolecta y deduplica todas las citas del hospital atravesando las agendas de los médicos."""
    todas = []
    for m in hospital:
        if isinstance(m, Medico):
            for c in m.agenda:
                if c not in todas:
                    todas.append(c)
    return todas


def menu():
    hospital_uev = Hospital("Hospital Universitario UEV")

    # ─── Carga inicial ───
    for p in GestorDatos.cargar_pacientes(Paciente):
        try:
            hospital_uev.agregar_persona(p)
        except DniDuplicadoError as e:
            print(f"⚠️ {e}")

    for m in GestorDatos.cargar_medicos(Medico):
        try:
            hospital_uev.agregar_persona(m)
        except DniDuplicadoError as e:
            print(f"⚠️ {e}")

    # Restaurar citas históricas (no validamos fechas pasadas al cargar)
    GestorDatos.cargar_citas(hospital_uev, Cita, Tratamiento)

    while True:
        print(f"\n--- MENÚ: {hospital_uev.nombre} ---")
        print("1. Agregar paciente")
        print("2. Agregar médico")
        print("3. Mostrar personas (polimorfismo)")
        print("4. Programar cita y tratamiento")
        print("5. Buscar persona por DNI")
        print("6. Eliminar persona por DNI")
        print("7. Salir y guardar")

        opcion = input("Seleccione una opción: ").strip()

        # ────────────── 1. AGREGAR PACIENTE ──────────────
        if opcion == "1":
            try:
                nombre = input("Nombre del paciente: ")
                edad = int(input("Edad: "))
                peso = float(input("Peso (kg): "))
                altura = float(input("Altura (m): "))
                dni = input("DNI: ")

                while True:
                    resp = input("¿Tiene seguro? (s/n): ").lower()
                    if resp in ['s', 'n']:
                        tiene_seguro = (resp == 's')
                        break
                    print("❌ Error: Ingrese 's' o 'n'.")

                p = Paciente(nombre, edad, dni, peso, altura, seguro=tiene_seguro)
                hospital_uev.agregar_persona(p)
                print(f"✅ Paciente {nombre} registrado exitosamente.")

            except DniDuplicadoError as e:
                print(f"❌ {e}")
            except (ValueError, DatoInvalidoError) as e:
                print(f"❌ Error en los datos: {e}")

        # ────────────── 2. AGREGAR MÉDICO ──────────────
        elif opcion == "2":
            print("\n--- Registro de Nuevo Médico ---")
            try:
                nombre = input("Nombre del doctor/a: ")
                if not nombre.strip():
                    raise ValueError("El nombre no puede estar vacío.")

                edad = int(input("Edad: "))
                dni = input("DNI: ")
                salario = float(input("Salario mensual: "))
                especialidad = input("Especialidad: ")
                id_colegiado = input("ID Colegiado: ")

                m = Medico(nombre, edad, dni, salario, especialidad, id_colegiado)
                hospital_uev.agregar_persona(m)
                print(f"✅ Dr./Dra. {nombre} ha sido registrado/a exitosamente.")

            except DniDuplicadoError as e:
                print(f"❌ {e}")
            except (ValueError, DatoInvalidoError) as e:
                print(f"❌ Error en los datos: {e}")

        # ────────────── 3. MOSTRAR DIRECTORIO ──────────────
        elif opcion == "3":
            print(f"\n--- DIRECTORIO ({len(hospital_uev)} registros) ---")
            if len(hospital_uev) == 0:
                print("El hospital está vacío.")
            else:
                for persona in hospital_uev:
                    print(persona.mostrar_datos())
                    print("-" * 40)

        # ────────────── 4. PROGRAMAR CITA ──────────────
        elif opcion == "4":
            pacientes = [p for p in hospital_uev if isinstance(p, Paciente)]
            medicos = [m for m in hospital_uev if isinstance(m, Medico)]

            if not pacientes or not medicos:
                print("⚠️ Necesita al menos un médico y un paciente registrados.")
                continue

            print("\n--- Seleccione un Médico ---")
            for i, m in enumerate(medicos):
                print(f"{i+1}. {m.nombre} ({m.especialidad})")
            try:
                idx_m = int(input("Número del médico: ")) - 1
                m_actual = medicos[idx_m]
            except (ValueError, IndexError):
                print("❌ Selección inválida.")
                continue

            print("\n--- Seleccione un Paciente ---")
            for i, p in enumerate(pacientes):
                print(f"{i+1}. {p.nombre} (DNI: {p.dni})")
            try:
                idx_p = int(input("Número del paciente: ")) - 1
                p_actual = pacientes[idx_p]
            except (ValueError, IndexError):
                print("❌ Selección inválida.")
                continue

            fecha = input("Fecha de la cita (DD/MM/AAAA HH:MM): ")
            motivo = input("Motivo: ")

            try:
                cita = Cita(m_actual, p_actual, fecha, motivo)
                print("✅ Cita creada:", cita)

                tipo = input("Tipo de tratamiento (consulta/analisis/cirugia/vacuna/revision, vacío para omitir): ").lower().strip()
                if tipo:
                    tratam = Tratamiento(cita, tipo, "Programado desde consola")
                    print("💰", tratam)

            except (MedicoNoDisponibleError, CitaDuplicadaError) as e:
                print(f"🚨 Conflicto de agenda: {e}")
            except (ValueError, TypeError) as e:
                print(f"❌ Datos inválidos: {e}")

        # ────────────── 5. BUSCAR POR DNI ──────────────
        elif opcion == "5":
            dni = input("DNI a buscar: ").strip()
            persona = hospital_uev.buscar_por_dni(dni)
            if persona:
                print("\n✅ Persona encontrada:")
                print(persona.mostrar_datos())
            else:
                print(f"❌ No se encontró a nadie con DNI {dni}.")

        # ────────────── 6. ELIMINAR POR DNI ──────────────
        elif opcion == "6":
            dni = input("DNI de la persona a eliminar: ").strip()
            persona = hospital_uev.buscar_por_dni(dni, registrar=False)
            if not persona:
                print(f"❌ No existe nadie con DNI {dni}.")
                continue
            confirm = input(f"¿Confirma eliminar a {persona.nombre}? (s/n): ").lower()
            if confirm == 's':
                try:
                    hospital_uev.eliminar_por_dni(dni)
                    print(f"✅ {persona.nombre} eliminado del sistema.")
                except PersonaNoEncontradaError as e:
                    print(f"❌ {e}")
            else:
                print("Operación cancelada.")

        # ────────────── 7. SALIR Y GUARDAR ──────────────
        elif opcion == "7":
            solo_pacientes = [p for p in hospital_uev if isinstance(p, Paciente)]
            solo_medicos = [m for m in hospital_uev if isinstance(m, Medico)]
            todas_las_citas = _recolectar_citas(hospital_uev)

            GestorDatos.guardar_pacientes(solo_pacientes)
            GestorDatos.guardar_medicos(solo_medicos)
            GestorDatos.guardar_citas(todas_las_citas)

            print("💾 Datos guardados. ¡Hasta pronto!")
            break

        else:
            print("❌ Opción no válida.")


if __name__ == "__main__":
    menu()

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


TAMANO_PAGINA = 10   # Número de filas por página en los listados


def _recolectar_citas(hospital):
    """Recolecta y deduplica todas las citas atravesando las agendas de los médicos."""
    todas = []
    for m in hospital:
        if isinstance(m, Medico):
            for c in m.agenda:
                if c not in todas:
                    todas.append(c)
    return todas


def _mostrar_paginado(items, formato_linea, titulo="Listado"):
    """
    Muestra una lista paginada de elementos.
    `formato_linea` es una función que recibe un elemento y devuelve la línea a imprimir.
    Permite navegar con n (siguiente), p (anterior), q (salir).
    """
    if not items:
        print(f"\n(Lista vacía: no hay nada que mostrar)\n")
        return

    total = len(items)
    total_paginas = (total + TAMANO_PAGINA - 1) // TAMANO_PAGINA
    pagina = 0

    while True:
        inicio = pagina * TAMANO_PAGINA
        fin = min(inicio + TAMANO_PAGINA, total)

        print(f"\n{'─'*70}")
        print(f" {titulo}  —  Página {pagina+1}/{total_paginas}  "
              f"(mostrando {inicio+1}-{fin} de {total})")
        print('─'*70)

        for i in range(inicio, fin):
            print(f" {i+1:3}. {formato_linea(items[i])}")

        print('─'*70)
        # Construir las opciones disponibles según la página actual
        opciones = []
        if pagina > 0:
            opciones.append("[p]revia")
        if pagina < total_paginas - 1:
            opciones.append("[n]ext")
        opciones.append("[q]uit")
        print(" Navegación: " + "  ".join(opciones))

        accion = input(" > ").strip().lower()
        if accion == "n" and pagina < total_paginas - 1:
            pagina += 1
        elif accion == "p" and pagina > 0:
            pagina -= 1
        elif accion == "q":
            break
        elif accion == "":
            # Enter por defecto avanza
            if pagina < total_paginas - 1:
                pagina += 1
            else:
                break
        else:
            print(" ⚠️ Opción no válida.")


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

    GestorDatos.cargar_citas(hospital_uev, Cita, Tratamiento)

    while True:
        print(f"\n╔══ MENÚ: {hospital_uev.nombre} ══╗")
        print("║ 1. Agregar paciente")
        print("║ 2. Agregar médico")
        print("║ 3. Mostrar personas (polimorfismo, paginado)")
        print("║ 4. Programar cita y tratamiento")
        print("║ 5. Buscar persona (por DNI o ID Colegiado)")
        print("║ 6. Eliminar persona por DNI")
        print("║ 7. Mostrar todas las citas")
        print("║ 8. Salir y guardar")
        print("╚════════════════════════════════════╝")

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
                print(f"✅ Dr./Dra. {nombre} registrado/a exitosamente.")

            except DniDuplicadoError as e:
                print(f"❌ {e}")
            except (ValueError, DatoInvalidoError) as e:
                print(f"❌ Error en los datos: {e}")

        # ────────────── 3. MOSTRAR DIRECTORIO PAGINADO ──────────────
        elif opcion == "3":
            personas = list(hospital_uev)
            # Ordenamos: primero médicos, luego pacientes; dentro de cada grupo alfabéticamente
            personas.sort(key=lambda p: (0 if isinstance(p, Medico) else 1, p.nombre))
            _mostrar_paginado(
                items=personas,
                formato_linea=lambda p: p.resumen(),
                titulo=f"📋 Directorio del hospital ({len(personas)} registros)"
            )

        # ────────────── 4. PROGRAMAR CITA ──────────────
        elif opcion == "4":
            pacientes = [p for p in hospital_uev if isinstance(p, Paciente)]
            medicos = [m for m in hospital_uev if isinstance(m, Medico)]

            if not pacientes or not medicos:
                print("⚠️ Necesita al menos un médico y un paciente.")
                continue

            print("\n--- Seleccione un Médico ---")
            for i, m in enumerate(medicos[:15]):  # mostramos máximo 15 para no saturar
                print(f"{i+1}. {m.nombre} ({m.especialidad})")
            if len(medicos) > 15:
                print(f"  ... y {len(medicos) - 15} más (use búsqueda por ID Colegiado en menú 5).")
            try:
                idx_m = int(input("Número del médico: ")) - 1
                m_actual = medicos[idx_m]
            except (ValueError, IndexError):
                print("❌ Selección inválida.")
                continue

            print("\n--- Seleccione un Paciente (introduce el DNI directamente) ---")
            dni_pac = input("DNI del paciente: ").strip()
            p_actual = hospital_uev.buscar_por_dni(dni_pac)
            if not isinstance(p_actual, Paciente):
                print("❌ Ese DNI no corresponde a ningún paciente.")
                continue

            fecha = input("Fecha de la cita (DD/MM/AAAA HH:MM): ")
            motivo = input("Motivo: ")

            try:
                cita = Cita(m_actual, p_actual, fecha, motivo)
                print("✅ Cita creada:", cita)

                tipo = input("Tipo de tratamiento (consulta/analisis/cirugia/vacuna/revision, vacío=omitir): ").lower().strip()
                if tipo:
                    tratam = Tratamiento(cita, tipo, "Programado desde consola")
                    print("💰", tratam)

            except (MedicoNoDisponibleError, CitaDuplicadaError) as e:
                print(f"🚨 Conflicto de agenda: {e}")
            except (ValueError, TypeError) as e:
                print(f"❌ Datos inválidos: {e}")

        # ────────────── 5. BUSCAR (DNI o ID Colegiado) ──────────────
        elif opcion == "5":
            ident = input("Introduce DNI o ID Colegiado: ").strip()
            persona = hospital_uev.buscar(ident)
            if persona:
                print("\n✅ Persona encontrada:")
                print(persona.mostrar_datos())
            else:
                print(f"❌ No se encontró a nadie con identificador '{ident}'.")

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

        # ────────────── 7. MOSTRAR CITAS PAGINADAS ──────────────
        elif opcion == "7":
            citas = sorted(_recolectar_citas(hospital_uev))

            def _formato_cita(c):
                trat = f" → {c.tratamiento.tipo} ({c.tratamiento.calcular_costo():.2f}€)" if c.tratamiento else ""
                return (
                    f"{c.fecha_hora}  "
                    f"{c.paciente.nombre[:22]:<22} con {c.medico.nombre[:22]:<22}"
                    f"{trat}"
                )

            _mostrar_paginado(
                items=citas,
                formato_linea=_formato_cita,
                titulo=f"📅 Todas las citas ({len(citas)} en total)"
            )

        # ────────────── 8. SALIR Y GUARDAR ──────────────
        elif opcion == "8":
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

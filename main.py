# -*- coding: utf-8 -*-
"""
Módulo Principal (main.py)
Responsable: Integrante 4 (El Integrador y Director)
Descripción: Punto de entrada del programa. Gestiona la interfaz de usuario
y coordina los módulos de entidades, lógica y persistencia.
"""

# REQUISITO: Importar todos los módulos
from entidades import Paciente, Medico, DatoInvalidoError
from persistencia import GestorDatos
from logica import Cita, Tratamiento, MedicoNoDisponibleError
from hospital import Hospital

def menu():
    hospital_uev = Hospital("Hospital Universitario UEV")

    # 1. Cargamos pacientes desde su base de datos específica
    lista_pacientes = GestorDatos.cargar_pacientes(Paciente)
    for p in lista_pacientes:
        hospital_uev.agregar_persona(p)

    # 2. Cargamos médicos desde su base de datos específica (Nueva implementación)
    lista_medicos = GestorDatos.cargar_medicos(Medico)
    for m in lista_medicos:
        hospital_uev.agregar_persona(m)


    while True:
        print(f"\n--- MENÚ: {hospital_uev.nombre} ---")
        print("1. Agregar paciente")
        print("2. Agregar médico (Requisito: Lista Heterogénea)")
        print("3. Mostrar personas (Demostración de Polimorfismo)")
        print("4. Programar Cita y Tratamiento (Lógica de Negocio)")
        print("5. Salir y Guardar")

        opcion = input("Seleccione una opción: ")

        # --- FUNCIONALIDAD 1: AGREGAR PACIENTE ---
        if opcion == "1":
            nombre = input("Nombre del paciente: ")
            try:
                edad = int(input("Edad: "))
                peso = float(input("Peso (kg): "))
                altura = float(input("Altura (m): "))
                dni = input("DNI: ")
                
                # Bucle de validación para el seguro médico
                while True:
                    resp = input("¿Tiene seguro? (s/n): ").lower()
                    if resp in ['s', 'n']:
                        tiene_seguro = (resp == 's')
                        break
                    print("❌ Error: Ingrese 's' para sí o 'n' para no.")

                # Instanciación (Llama a los setters y validaciones del Integrante 1)
                p = Paciente(nombre, edad, dni, peso, altura, seguro=tiene_seguro)
                hospital_uev.agregar_persona(p)
                print(f"✅ Paciente {nombre} registrado exitosamente.")
                
            except (ValueError, DatoInvalidoError) as e:
                # Captura de excepciones de tipo de dato o lógica de dominio
                print(f"❌ Error en los datos ingresados: {e}")

       # --- FUNCIONALIDAD 2: AGREGAR MÉDICO ---
        elif opcion == "2":
            print("\n--- Registro de Nuevo Médico ---")
            
            while True:
                try:
                    nombre = input("Nombre del doctor/a: ")
                    if not nombre.strip():
                        raise ValueError("El nombre no puede estar vacío.")
                        
                    edad = int(input("Edad: "))
                    dni = input("DNI: ")
                    salario = float(input("Salario mensual: "))
                    especialidad = input("Especialidad (ej. Cardiología): ")
                    id_colegiado = input("ID Colegiado (ej. COL-123): ")

                    # 💡 Aquí se activan automáticamente todos los setters de validación
                    # Si algo está mal (edad negativa, texto vacío), saltará al 'except'
                    m = Medico(nombre, edad, dni, salario, especialidad, id_colegiado)
                    
                    hospital_uev.agregar_persona(m)
                    print(f"✅ {nombre} ha sido registrado/a exitosamente.")
                    
                    break # Si todo fue bien, rompemos el bucle y volvemos al menú principal
                    
                except ValueError as e:
                    # Captura errores de tipo (ej. poner letras en la edad) o el nombre vacío
                    print(f"❌ Error de entrada: {e}. Por favor, intente de nuevo.\n")
                except DatoInvalidoError as e:
                    # Captura las restricciones específicas de nuestra lógica de negocio
                    print(f"❌ Error de validación: {e}. Por favor, intente de nuevo.\n")
        # --- FUNCIONALIDAD 3: MOSTRAR DIRECTORIO (POLIMORFISMO) ---
        elif opcion == "3":
            # Uso implícito del método mágico __len__ de la clase Hospital
            print(f"\n--- DIRECTORIO ({len(hospital_uev)} registros) ---")
            
            if len(hospital_uev) == 0:
                print("El hospital está vacío.")
            else:
                # Iteración sobre el Hospital (Uso implícito del método mágico __getitem__)
                for persona in hospital_uev:
                    # REQUISITO: Polimorfismo. 
                    # Python decide en tiempo de ejecución qué versión de mostrar_datos() ejecutar.
                    print(persona.mostrar_datos())
                    print("-" * 40)

        # --- FUNCIONALIDAD 4: LÓGICA DE CITAS (INTERACTIVO) ---
        elif opcion == "4":
            pacientes = [p for p in hospital_uev if isinstance(p, Paciente)]
            medicos = [m for m in hospital_uev if isinstance(m, Medico)]

            if not pacientes or not medicos:
                print("⚠️ Atención: Necesita registrar al menos un médico y un paciente para crear una cita.")
                continue

            # 🌟 1. Mostrar menú interactivo para elegir al MÉDICO
            print("\n--- Seleccione un Médico ---")
            for i, m in enumerate(medicos):
                print(f"{i+1}. {m.nombre} ({m.especialidad})")
            try:
                idx_m = int(input("Seleccione el número del médico: ")) - 1
                if idx_m < 0 or idx_m >= len(medicos): raise ValueError
                m_actual = medicos[idx_m]
            except ValueError:
                print("❌ Selección inválida. Operación cancelada.")
                continue

            # 🌟 2. Mostrar menú interactivo para elegir al PACIENTE
            print("\n--- Seleccione un Paciente ---")
            for i, p in enumerate(pacientes):
                print(f"{i+1}. {p.nombre} (DNI: {p.dni})")
            try:
                idx_p = int(input("Seleccione el número del paciente: ")) - 1
                if idx_p < 0 or idx_p >= len(pacientes): raise ValueError
                p_actual = pacientes[idx_p]
            except ValueError:
                print("❌ Selección inválida. Operación cancelada.")
                continue
            
            # 🌟 3. Crear la cita con el médico y paciente elegidos
            print(f"\nGenerando cita para: {p_actual.nombre} con {m_actual.nombre}")
            fecha = input("Fecha de la cita (ej. 20/06/2026 10:00): ")
            motivo = input("Motivo de la consulta: ")

            try:
                # Composición (Integrante 2)
                cita = Cita(m_actual, p_actual, fecha, motivo)
                print("✅ Cita creada con éxito:", cita)

                tipo = input("Tipo de tratamiento (consulta/analisis/cirugia/vacuna/revision): ").lower()
                tratam = Tratamiento(cita, tipo, "Revisión programada por sistema")
                print("💰 Resumen de facturación:", tratam)
                
            except MedicoNoDisponibleError as e:
                print(f"🚨 Conflicto de agenda: {e}")
            except Exception as e:
                print(f"❌ Error inesperado: {e}")

        # --- FUNCIONALIDAD 5: SALIR Y GUARDAR (TRABAJO DEL INTEGRANTE 3) ---
        elif opcion == "5":
            # ---------------------------------------------------------
            # PASO 2: Persistencia - Guardado de datos al finalizar
            # ---------------------------------------------------------
            
            # REQUISITO: Procesamiento de lista heterogénea mediante isinstance
            # Separamos los objetos según su clase para guardarlos en archivos distintos
            solo_pacientes = [p for p in hospital_uev if isinstance(p, Paciente)]
            solo_medicos = [m for m in hospital_uev if isinstance(m, Medico)]
            
            # Llamada a los métodos estáticos del Gestor de Datos
            GestorDatos.guardar_pacientes(solo_pacientes)
            GestorDatos.guardar_medicos(solo_medicos) 
            
            print("💾 Sincronización completada. Los archivos CSV han sido actualizados.")
            print("¡Hasta pronto!")
            break

        else:
            print("❌ Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    menu()

# -*- coding: utf-8 -*-
"""
seed_data.py — Genera un citas_db.csv realista a partir de los CSVs
existentes de pacientes y médicos.

Reglas de generación:
- Se garantiza que cada DNI de paciente y cada ID Colegiado existen.
- Se evita que un médico tenga dos citas a la misma hora.
- Se evita que un paciente tenga dos citas a la misma hora.
- Distribución temporal: desde hace 3 meses hasta dentro de 6 meses
  (necesario para que la nómina trimestral del médico tenga contenido).
- ~70% de las citas llevan tratamiento, 30% sin tratamiento.
- Al menos 6 médicos terminan con 5+ citas cada uno.
- Al menos 10 pacientes terminan con 2+ citas cada uno.

Uso:
    python seed_data.py            # Genera citas_db.csv (sobrescribe si existe)
"""

import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

random.seed(42)   # reproducibilidad

DIR = Path(__file__).parent
ARCHIVO_PACIENTES = DIR / "pacientes_db.csv"
ARCHIVO_MEDICOS   = DIR / "medicos_db.csv"
ARCHIVO_CITAS     = DIR / "citas_db.csv"

TIPOS_TRATAMIENTO = ["consulta", "analisis", "vacuna", "revision", "cirugia"]

# Motivos de consulta variados, agrupados por especialidad
MOTIVOS_POR_ESPECIALIDAD = {
    "Cardiología":      ["Dolor torácico", "Control hipertensión", "Electrocardiograma anual",
                         "Seguimiento arritmia", "Revisión post-infarto"],
    "Pediatría":        ["Revisión rutinaria", "Vacunación infantil", "Control crecimiento",
                         "Fiebre persistente", "Otitis recurrente"],
    "Neurología":       ["Cefalea crónica", "Evaluación migraña", "Control epilepsia",
                         "Mareos y vértigo", "Pérdida memoria"],
    "Cirugía General":  ["Valoración prequirúrgica", "Seguimiento postoperatorio",
                         "Hernia inguinal", "Apendicectomía consulta"],
    "Dermatología":     ["Revisión de lunares", "Acné severo", "Eczema",
                         "Lesión dérmica", "Control psoriasis"],
    "Traumatología":    ["Esguince de tobillo", "Dolor lumbar", "Revisión rodilla",
                         "Lesión deportiva", "Fractura seguimiento"],
    "Ginecología":      ["Revisión anual", "Control embarazo", "Citología",
                         "Consulta menopausia", "Planificación familiar"],
    "Oncología":        ["Seguimiento oncológico", "Resultado biopsia",
                         "Control postquimioterapia", "Consulta familiar"],
    "Psiquiatría":      ["Evaluación ansiedad", "Seguimiento depresión",
                         "Trastorno del sueño", "Revisión medicación"],
    "Urgencias":        ["Dolor abdominal agudo", "Traumatismo leve",
                         "Reacción alérgica", "Crisis hipertensiva"],
    "Oftalmología":     ["Revisión visión", "Control glaucoma", "Conjuntivitis",
                         "Examen fondo de ojo", "Renovación gafas"],
    "Anestesiología":   ["Valoración preanestésica", "Consulta dolor crónico",
                         "Seguimiento postanestesia"],
}
MOTIVOS_DEFAULT = ["Consulta general", "Revisión periódica", "Control rutinario"]


# ────────────────────────────────────────────────────────────
def cargar_pacientes():
    """Devuelve lista de DNIs de pacientes (orden del archivo)."""
    dnis = []
    with open(ARCHIVO_PACIENTES, "r", encoding="utf-8") as f:
        for linea in f:
            if linea.strip():
                campos = linea.strip().split(",")
                dnis.append(campos[2])   # DNI está en la posición 2
    return dnis


def cargar_medicos():
    """Devuelve lista de (id_colegiado, especialidad)."""
    medicos = []
    with open(ARCHIVO_MEDICOS, "r", encoding="utf-8") as f:
        for linea in f:
            if linea.strip():
                campos = linea.strip().split(",")
                medicos.append((campos[5], campos[4]))  # (ID Colegiado, especialidad)
    return medicos


def fecha_aleatoria(dias_atras=90, dias_adelante=180):
    """Genera una fecha aleatoria en horario laboral (lun-vie, 09:00-18:00, en :00 o :30)."""
    while True:
        delta_dias = random.randint(-dias_atras, dias_adelante)
        fecha = datetime.now() + timedelta(days=delta_dias)
        # Solo lunes-viernes
        if fecha.weekday() < 5:
            hora = random.randint(9, 17)
            minuto = random.choice([0, 30])
            return fecha.replace(hour=hora, minute=minuto, second=0, microsecond=0)


def generar_citas(n_objetivo=55):
    """
    Genera ~n_objetivo citas garantizando que:
    - No haya colisiones de horario por médico
    - No haya colisiones de horario por paciente
    - Al menos 6 médicos tengan 5+ citas
    - Al menos 10 pacientes tengan 2+ citas
    """
    pacientes = cargar_pacientes()
    medicos = cargar_medicos()

    print(f"📊 Cargados {len(pacientes)} pacientes y {len(medicos)} médicos")

    # Agendas en memoria para detectar colisiones
    agenda_medico = {id_col: set() for id_col, _ in medicos}
    agenda_paciente = {dni: set() for dni in pacientes}

    citas = []
    intentos = 0
    max_intentos = n_objetivo * 10

    # --- Fase 1: asegurar que los primeros 6 médicos tengan 5+ citas ---
    medicos_top = medicos[:6]
    for id_col, especialidad in medicos_top:
        for _ in range(5):
            if intentos > max_intentos:
                break
            cita = _intentar_cita(id_col, especialidad, pacientes,
                                   agenda_medico, agenda_paciente)
            if cita:
                citas.append(cita)
            intentos += 1

    # --- Fase 2: rellenar hasta n_objetivo con elecciones aleatorias ---
    while len(citas) < n_objetivo and intentos < max_intentos:
        id_col, especialidad = random.choice(medicos)
        cita = _intentar_cita(id_col, especialidad, pacientes,
                               agenda_medico, agenda_paciente)
        if cita:
            citas.append(cita)
        intentos += 1

    return citas


def _intentar_cita(id_colegiado, especialidad, pacientes,
                    agenda_medico, agenda_paciente, max_intentos=20):
    """Intenta crear una cita válida; devuelve la fila o None si falla."""
    for _ in range(max_intentos):
        dni_pac = random.choice(pacientes)
        fecha = fecha_aleatoria()

        if fecha in agenda_medico[id_colegiado]:
            continue
        if fecha in agenda_paciente[dni_pac]:
            continue

        # Reservamos el slot
        agenda_medico[id_colegiado].add(fecha)
        agenda_paciente[dni_pac].add(fecha)

        # Generar motivo según especialidad
        motivos = MOTIVOS_POR_ESPECIALIDAD.get(especialidad, MOTIVOS_DEFAULT)
        motivo = random.choice(motivos)

        # Tratamiento: 70% de las citas tienen uno
        if random.random() < 0.70:
            tipo_trat = random.choice(TIPOS_TRATAMIENTO)
            desc_trat = f"Procedimiento {tipo_trat} programado"
        else:
            tipo_trat = ""
            desc_trat = ""

        fecha_str = fecha.strftime("%d/%m/%Y %H:%M")
        return [dni_pac, id_colegiado, fecha_str, motivo, tipo_trat, desc_trat]
    return None


def guardar(citas):
    """Escribe las citas en el CSV."""
    with open(ARCHIVO_CITAS, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        for fila in citas:
            writer.writerow(fila)
    print(f"✅ Generadas {len(citas)} citas → {ARCHIVO_CITAS.name}")


def estadisticas(citas):
    """Imprime un resumen de cuántas citas tiene cada médico/paciente."""
    from collections import Counter
    medicos_count = Counter(c[1] for c in citas)
    pacientes_count = Counter(c[0] for c in citas)
    pasadas = sum(1 for c in citas
                  if datetime.strptime(c[2], "%d/%m/%Y %H:%M") < datetime.now())
    con_trat = sum(1 for c in citas if c[4])

    print(f"\n📈 Estadísticas:")
    print(f"   • Total citas: {len(citas)}")
    print(f"   • Citas pasadas (para nómina): {pasadas}")
    print(f"   • Citas futuras: {len(citas) - pasadas}")
    print(f"   • Con tratamiento: {con_trat} ({con_trat*100//len(citas)}%)")
    print(f"   • Médicos con 5+ citas: {sum(1 for v in medicos_count.values() if v >= 5)}")
    print(f"   • Pacientes con 2+ citas: {sum(1 for v in pacientes_count.values() if v >= 2)}")
    print(f"\n   Top 5 médicos más ocupados:")
    for id_col, n in medicos_count.most_common(5):
        print(f"     {id_col}: {n} citas")


if __name__ == "__main__":
    print("🌱 Generando datos sintéticos de citas...\n")
    citas = generar_citas(n_objetivo=55)
    guardar(citas)
    estadisticas(citas)
    print("\n✨ Listo. Reinicia la app para cargar los datos.")

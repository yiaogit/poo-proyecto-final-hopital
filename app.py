# -*- coding: utf-8 -*-
"""
app.py — Capa de presentación web del Hospital Universitario UEV.
Reutiliza directamente las clases del modelo de dominio:
    Paciente, Medico, Cita, Tratamiento, Hospital, GestorDatos.
No reimplementa ninguna lógica de negocio: Flask es solo "la piel".
"""

from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime

from entidades import Paciente, Medico, DatoInvalidoError
from logica import (
    Cita,
    Tratamiento,
    MedicoNoDisponibleError,
    CitaDuplicadaError,
)
from persistencia import GestorDatos
from hospital import Hospital


# ─────────────────────────────────────────
# Inicialización de la app y del dominio
# ─────────────────────────────────────────
app = Flask(__name__)
app.secret_key = "cambia-esta-clave-en-produccion"   # necesaria para flash()

# Instancia única del hospital (vive mientras dure el proceso)
hospital = Hospital("Hospital Universitario UEV")

# Carga inicial desde los CSV (reutiliza el Factory Method desde_csv)
for p in GestorDatos.cargar_pacientes(Paciente):
    hospital.agregar_persona(p)
for m in GestorDatos.cargar_medicos(Medico):
    hospital.agregar_persona(m)


# ─────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────
def _pacientes():
    return [p for p in hospital if isinstance(p, Paciente)]


def _medicos():
    return [m for m in hospital if isinstance(m, Medico)]


def _todas_las_citas():
    """Recolecta todas las citas atravesando las agendas de los médicos."""
    citas = []
    for m in _medicos():
        citas.extend(m.agenda)
    # quitar duplicados (una cita aparece en agenda de médico y paciente)
    vistos = []
    for c in citas:
        if c not in vistos:
            vistos.append(c)
    return sorted(vistos)   # usa __lt__ con datetime → orden cronológico real


def _persistir():
    """Guarda el estado actual del hospital en los CSV."""
    GestorDatos.guardar_pacientes(_pacientes())
    GestorDatos.guardar_medicos(_medicos())


# ─────────────────────────────────────────
# Rutas
# ─────────────────────────────────────────
@app.route("/")
def index():
    """Dashboard: resumen general y citas próximas."""
    citas = _todas_las_citas()
    proximas = [c for c in citas if c._fecha_obj >= datetime.now()][:5]
    return render_template(
        "index.html",
        hospital=hospital,
        n_pacientes=len(_pacientes()),
        n_medicos=len(_medicos()),
        n_citas=len(citas),
        proximas=proximas,
    )


# ─────────── PACIENTES ──────────────
@app.route("/pacientes", methods=["GET", "POST"])
def pacientes():
    if request.method == "POST":
        try:
            p = Paciente(
                nombre=request.form["nombre"].strip(),
                edad=int(request.form["edad"]),
                dni=request.form["dni"].strip(),
                peso=float(request.form["peso"]),
                altura=float(request.form["altura"]),
                seguro=("seguro" in request.form),
            )
            hospital.agregar_persona(p)
            _persistir()
            flash(f"Paciente {p.nombre} registrado correctamente.", "success")
        except (ValueError, DatoInvalidoError) as e:
            flash(f"Error de validación: {e}", "danger")
        except Exception as e:
            flash(f"Error inesperado: {e}", "danger")
        return redirect(url_for("pacientes"))

    return render_template("pacientes.html", pacientes=_pacientes())


# ─────────── MÉDICOS ──────────────
@app.route("/medicos", methods=["GET", "POST"])
def medicos():
    if request.method == "POST":
        try:
            m = Medico(
                nombre=request.form["nombre"].strip(),
                edad=int(request.form["edad"]),
                dni=request.form["dni"].strip(),
                salario=float(request.form["salario"]),
                especialidad=request.form["especialidad"].strip(),
                identificacion=request.form["identificacion"].strip(),
            )
            hospital.agregar_persona(m)
            _persistir()
            flash(f"Dr./Dra. {m.nombre} registrado/a correctamente.", "success")
        except (ValueError, DatoInvalidoError) as e:
            flash(f"Error de validación: {e}", "danger")
        except Exception as e:
            flash(f"Error inesperado: {e}", "danger")
        return redirect(url_for("medicos"))

    return render_template("medicos.html", medicos=_medicos())


# ─────────── CITAS Y TRATAMIENTOS ──────────────
@app.route("/citas", methods=["GET", "POST"])
def citas():
    if request.method == "POST":
        # Localizar los objetos elegidos por el usuario
        dni_paciente = request.form["paciente"]
        id_medico = request.form["medico"]
        fecha_html = request.form["fecha"]      # llega como 'YYYY-MM-DDTHH:MM'
        motivo = request.form["motivo"]
        tipo_trat = request.form.get("tipo_tratamiento", "").strip()

        paciente_obj = next((p for p in _pacientes() if p.dni == dni_paciente), None)
        medico_obj = next((m for m in _medicos() if m.identificacion == id_medico), None)

        if not paciente_obj or not medico_obj:
            flash("Paciente o médico no encontrado.", "danger")
            return redirect(url_for("citas"))

        # Convertir el formato del input HTML al que espera la clase Cita
        try:
            dt = datetime.strptime(fecha_html, "%Y-%m-%dT%H:%M")
            fecha_str = dt.strftime("%d/%m/%Y %H:%M")
        except ValueError:
            flash("Formato de fecha inválido.", "danger")
            return redirect(url_for("citas"))

        # Crear la cita reutilizando toda la lógica del modelo
        try:
            cita = Cita(medico_obj, paciente_obj, fecha_str, motivo)
            mensaje = f"Cita creada para {paciente_obj.nombre} el {fecha_str}."

            # Si se indicó un tipo de tratamiento, lo asociamos
            if tipo_trat:
                trat = Tratamiento(cita, tipo_trat, "Programado desde la web")
                mensaje += f" Tratamiento '{tipo_trat}' añadido — coste: {trat.calcular_costo():.2f}€."

            flash(mensaje, "success")
        except (MedicoNoDisponibleError, CitaDuplicadaError) as e:
            flash(f"Conflicto de agenda: {e}", "warning")
        except (ValueError, TypeError) as e:
            flash(f"Datos inválidos: {e}", "danger")
        except Exception as e:
            flash(f"Error inesperado: {e}", "danger")

        return redirect(url_for("citas"))

    return render_template(
        "citas.html",
        pacientes=_pacientes(),
        medicos=_medicos(),
        citas=_todas_las_citas(),
        tarifas=Tratamiento.TARIFAS,
    )


# ─────────── Endpoint manual para guardar ──────────────
@app.route("/guardar", methods=["POST"])
def guardar():
    _persistir()
    flash("Datos guardados en los archivos CSV.", "success")
    return redirect(request.referrer or url_for("index"))


# ─────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)

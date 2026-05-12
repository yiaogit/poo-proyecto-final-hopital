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
from hospital import Hospital, DniDuplicadoError, PersonaNoEncontradaError


# ─────────────────────────────────────────
# Inicialización
# ─────────────────────────────────────────
app = Flask(__name__)
app.secret_key = "cambia-esta-clave-en-produccion"

hospital = Hospital("Hospital Universitario UEV")

# Carga inicial
for p in GestorDatos.cargar_pacientes(Paciente):
    try:
        hospital.agregar_persona(p)
    except DniDuplicadoError:
        pass   # silenciamos duplicados de la carga inicial

for m in GestorDatos.cargar_medicos(Medico):
    try:
        hospital.agregar_persona(m)
    except DniDuplicadoError:
        pass

# Restaurar citas históricas
GestorDatos.cargar_citas(hospital, Cita, Tratamiento)


# ─────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────
def _pacientes():
    return [p for p in hospital if isinstance(p, Paciente)]


def _medicos():
    return [m for m in hospital if isinstance(m, Medico)]


def _todas_las_citas():
    """Recolecta y deduplica todas las citas atravesando las agendas."""
    citas = []
    for m in _medicos():
        for c in m.agenda:
            if c not in citas:
                citas.append(c)
    return sorted(citas)


def _persistir():
    """Guarda todo el estado actual (pacientes + médicos + citas) en los CSV."""
    GestorDatos.guardar_pacientes(_pacientes())
    GestorDatos.guardar_medicos(_medicos())
    GestorDatos.guardar_citas(_todas_las_citas())


# ─────────────────────────────────────────
# Rutas
# ─────────────────────────────────────────
@app.route("/")
def index():
    """Dashboard: resumen general y próximas citas."""
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


# ─────────────── PACIENTES ───────────────
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
        except DniDuplicadoError as e:
            flash(f"DNI duplicado: {e}", "warning")
        except (ValueError, DatoInvalidoError) as e:
            flash(f"Error de validación: {e}", "danger")
        except Exception as e:
            flash(f"Error inesperado: {e}", "danger")
        return redirect(url_for("pacientes"))

    return render_template("pacientes.html", pacientes=_pacientes())


# ─────────────── MÉDICOS ───────────────
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
        except DniDuplicadoError as e:
            flash(f"DNI duplicado: {e}", "warning")
        except (ValueError, DatoInvalidoError) as e:
            flash(f"Error de validación: {e}", "danger")
        except Exception as e:
            flash(f"Error inesperado: {e}", "danger")
        return redirect(url_for("medicos"))

    return render_template("medicos.html", medicos=_medicos())


# ─────────────── ELIMINAR ───────────────
@app.route("/eliminar/<dni>", methods=["POST"])
def eliminar(dni):
    """Elimina una persona del directorio por DNI."""
    try:
        persona = hospital.eliminar_por_dni(dni)
        _persistir()
        tipo = "Paciente" if isinstance(persona, Paciente) else "Médico"
        flash(f"{tipo} {persona.nombre} eliminado/a correctamente.", "success")
    except PersonaNoEncontradaError as e:
        flash(f"{e}", "danger")
    except Exception as e:
        flash(f"Error inesperado: {e}", "danger")

    # Volver a la página de procedencia
    return redirect(request.referrer or url_for("index"))


# ─────────────── BUSCAR ───────────────
@app.route("/buscar", methods=["GET"])
def buscar():
    """Busca a una persona por DNI y muestra el resultado."""
    dni = request.args.get("dni", "").strip()
    resultado = None
    if dni:
        resultado = hospital.buscar_por_dni(dni)
        if resultado is None:
            flash(f"No se encontró a nadie con DNI {dni}.", "warning")
    return render_template("buscar.html", dni=dni, resultado=resultado)


# ─────────────── CITAS Y TRATAMIENTOS ───────────────
@app.route("/citas", methods=["GET", "POST"])
def citas():
    if request.method == "POST":
        dni_paciente = request.form["paciente"]
        id_medico = request.form["medico"]
        fecha_html = request.form["fecha"]
        motivo = request.form["motivo"]
        tipo_trat = request.form.get("tipo_tratamiento", "").strip()

        paciente_obj = next((p for p in _pacientes() if p.dni == dni_paciente), None)
        medico_obj = next((m for m in _medicos() if m.identificacion == id_medico), None)

        if not paciente_obj or not medico_obj:
            flash("Paciente o médico no encontrado.", "danger")
            return redirect(url_for("citas"))

        try:
            dt = datetime.strptime(fecha_html, "%Y-%m-%dT%H:%M")
            fecha_str = dt.strftime("%d/%m/%Y %H:%M")
        except ValueError:
            flash("Formato de fecha inválido.", "danger")
            return redirect(url_for("citas"))

        try:
            cita = Cita(medico_obj, paciente_obj, fecha_str, motivo)
            mensaje = f"Cita creada para {paciente_obj.nombre} el {fecha_str}."

            if tipo_trat:
                trat = Tratamiento(cita, tipo_trat, "Programado desde la web")
                mensaje += f" Tratamiento '{tipo_trat}' añadido — coste: {trat.calcular_costo():.2f}€."

            _persistir()
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


# ─────────────── Persistencia manual ───────────────
@app.route("/guardar", methods=["POST"])
def guardar():
    _persistir()
    flash("Datos guardados en los archivos CSV.", "success")
    return redirect(request.referrer or url_for("index"))


# ─────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)

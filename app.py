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

    return render_template("pacientes.html", pacientes=_pacientes(), todas_citas=_todas_las_citas())


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
    """Busca a una persona por DNI o ID Colegiado y muestra el resultado completo."""
    identificador = request.args.get("dni", "").strip()  # 'dni' por compat. con plantilla
    resultado = None
    tipo_match = None   # "DNI" o "ID Colegiado", para mostrar en la plantilla
    if identificador:
        # Primero intentamos como DNI
        resultado = hospital.buscar_por_dni(identificador, registrar=False)
        if resultado:
            tipo_match = "DNI"
        else:
            # Si no, probamos como ID Colegiado
            resultado = hospital.buscar_por_id_colegiado(identificador, registrar=False)
            if resultado:
                tipo_match = "ID Colegiado"
        if resultado is None:
            flash(f"No se encontró a nadie con identificador '{identificador}'.", "warning")
    return render_template(
        "buscar.html",
        dni=identificador,
        resultado=resultado,
        tipo_match=tipo_match,
        es_paciente=isinstance(resultado, Paciente),
        es_medico=isinstance(resultado, Medico),
        todas_citas=_todas_las_citas(),
    )


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


# ═════════════════════════════════════════════════════════════
# RUTAS DE IMPRESIÓN
# ═════════════════════════════════════════════════════════════

def _contexto_documento():
    """Datos comunes a todas las plantillas de impresión."""
    ahora = datetime.now()
    return {
        "fecha_emision": ahora.strftime("%d/%m/%Y"),
        "hora_emision": ahora.strftime("%H:%M"),
        "year": ahora.year,
    }


def _localizar_cita(cita_idx):
    """Devuelve la cita en la posición cita_idx (entre todas las citas, ordenadas)."""
    todas = _todas_las_citas()
    if 0 <= cita_idx < len(todas):
        return todas[cita_idx]
    return None


# ── 1. COMPROBANTE DE CITA (paciente) ──
@app.route("/print/cita/<int:cita_idx>")
def print_cita(cita_idx):
    cita = _localizar_cita(cita_idx)
    if not cita:
        flash("Cita no encontrada.", "danger")
        return redirect(url_for("citas"))

    ctx = _contexto_documento()
    ctx.update({
        "cita": cita,
        "cita_idx": cita_idx + 1,
        "cita_ref": f"{cita.paciente.dni}-{cita_idx}",
    })

    return render_template("print_cita.html", **ctx)


# ── 2. FACTURA (paciente) ──
@app.route("/print/factura/<int:cita_idx>")
def print_factura(cita_idx):
    cita = _localizar_cita(cita_idx)
    if not cita:
        flash("Cita no encontrada.", "danger")
        return redirect(url_for("citas"))
    if not cita.tratamiento:
        flash("Esta cita no tiene tratamiento asociado, no se puede facturar.", "warning")
        return redirect(url_for("citas"))

    tarifa_base = Tratamiento.TARIFAS[cita.tratamiento.tipo]
    total = cita.tratamiento.calcular_costo()
    descuento = tarifa_base - total

    ctx = _contexto_documento()
    ctx.update({
        "cita": cita,
        "cita_idx": cita_idx + 1,
        "cita_ref": f"{cita.paciente.dni}-FACT-{cita_idx}",
        "tarifa_base": tarifa_base,
        "descuento": descuento,
        "subtotal": total,
        "total": total,
    })

    return render_template("print_factura.html", **ctx)


# ── 3. INFORME CLÍNICO / IMC (paciente) ──
@app.route("/print/informe/<dni>")
def print_informe(dni):
    paciente = hospital.buscar_por_dni(dni, registrar=False)
    if not paciente or not isinstance(paciente, Paciente):
        flash("Paciente no encontrado.", "danger")
        return redirect(url_for("pacientes"))

    ctx = _contexto_documento()
    ctx["paciente"] = paciente

    return render_template("print_informe.html", **ctx)


# ── 4. AGENDA DEL MÉDICO (interno) ──
@app.route("/print/agenda/<id_colegiado>")
def print_agenda(id_colegiado):
    medico = hospital.buscar_por_id_colegiado(id_colegiado, registrar=False)
    if not medico:
        flash("Médico no encontrado.", "danger")
        return redirect(url_for("medicos"))

    ahora = datetime.now()
    citas_pasadas = sorted(
        [c for c in medico.agenda if c._fecha_obj < ahora],
        reverse=True   # más recientes primero
    )
    citas_futuras = sorted(c for c in medico.agenda if c._fecha_obj >= ahora)

    ctx = _contexto_documento()
    ctx.update({
        "medico": medico,
        "citas_pasadas": citas_pasadas,
        "citas_futuras": citas_futuras,
    })

    return render_template("print_agenda_medico.html", **ctx)


# ── 5. NÓMINA TRIMESTRAL (interno) ──
@app.route("/print/nomina/<id_colegiado>")
def print_nomina(id_colegiado):
    medico = hospital.buscar_por_id_colegiado(id_colegiado, registrar=False)
    if not medico:
        flash("Médico no encontrado.", "danger")
        return redirect(url_for("medicos"))

    from datetime import timedelta
    ahora = datetime.now()
    hace_3_meses = ahora - timedelta(days=90)

    # Filtrar citas pasadas en los últimos 3 meses
    citas_periodo = sorted(
        c for c in medico.agenda
        if hace_3_meses <= c._fecha_obj <= ahora
    )

    # Agrupar por mes
    from collections import defaultdict
    meses_data = defaultdict(lambda: {"n_citas": 0, "ingresos": 0.0})
    NOMBRES_MES = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
                   "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]

    for c in citas_periodo:
        clave = (c._fecha_obj.year, c._fecha_obj.month)
        meses_data[clave]["n_citas"] += 1
        if c.tratamiento:
            meses_data[clave]["ingresos"] += c.tratamiento.calcular_costo()

    # Construir lista ordenada de meses (incluyendo los que tengan 0 citas para mostrar el rango completo)
    meses_lista = []
    for k in sorted(meses_data.keys()):
        anyo, mes = k
        meses_lista.append({
            "nombre": f"{NOMBRES_MES[mes-1]} {anyo}",
            "n_citas": meses_data[k]["n_citas"],
            "ingresos": meses_data[k]["ingresos"],
        })

    total_citas = sum(m["n_citas"] for m in meses_lista)
    total_ingresos = sum(m["ingresos"] for m in meses_lista)
    trimestre = ((ahora.month - 1) // 3) + 1

    ctx = _contexto_documento()
    ctx.update({
        "medico": medico,
        "meses": meses_lista,
        "citas_detalle": citas_periodo,
        "total_citas": total_citas,
        "total_ingresos": total_ingresos,
        "periodo_desde": hace_3_meses.strftime("%d/%m/%Y"),
        "periodo_hasta": ahora.strftime("%d/%m/%Y"),
        "trimestre": trimestre,
        "tarifas": Tratamiento.TARIFAS,
    })

    return render_template("print_nomina.html", **ctx)


# ─────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)

# 📦 Guía de Publicación en GitHub — v2.5

Textos listos para copiar y pegar al publicar esta versión.
(Este archivo es interno: NO es parte de la documentación pública, lo puedes borrar antes del commit final si quieres.)

---

## Release v2.5

### Tag
```
v2.5.0
```

### Title
```
v2.5 — Búsqueda por ID Colegiado, paginación y agenda integrada
```

### Description (Markdown)

```markdown
## 🎉 Versión 2.5 — Mejor experiencia de usuario

Versión menor que pule la experiencia de uso del sistema: ahora puedes
encontrar a un médico por su ID Colegiado, navegar listados largos con
paginación y ver todas las citas de una persona desde su ficha.

### ✨ Lo nuevo

- 🔍 **Búsqueda combinada**: el buscador (CLI opción 5 y `/buscar` web) acepta
  tanto DNI como ID Colegiado y muestra qué tipo de coincidencia encontró.
- 📑 **Listados paginados** en CLI: 10 entradas por página con navegación
  `[n]ext` / `[p]revia` / `[q]uit`.
- 📅 **Nueva opción "Mostrar todas las citas"** (CLI opción 7) con orden
  cronológico y paginación.
- 👁️ **Agenda integrada en cada ficha**: `mostrar_datos()` de pacientes y
  médicos ahora lista todas sus citas con fecha, contraparte y tratamiento.
- 🩺 **DNI del médico visible** en `__str__`, en la tabla web y en los
  resultados de búsqueda. ID Colegiado y DNI quedan vinculados visualmente.
- 📊 **Datos de prueba ampliados**: 22 pacientes y 12 médicos en los CSVs
  iniciales (antes 8 y 5), suficientes para ver la paginación en acción.

### 🔧 Cambios técnicos

- `Hospital.buscar_por_id_colegiado()` y `Hospital.buscar()` (búsqueda
  unificada que prueba DNI primero, luego ID Colegiado).
- Método `resumen()` en `Paciente` y `Medico` para listados breves.
- `Medico.__str__` ahora incluye DNI e ID Colegiado.

### 🧪 Tests

43 tests pasando (sin cambios desde v2.0).

### 📋 Historial completo

Ver [`CHANGELOG.md`](CHANGELOG.md).
```

---

## Configuración del repositorio (página "About")

Pulsa el icono ⚙️ junto al título del repo y configura:

**Description**
```
Sistema de gestión hospitalaria en Python aplicando POO. Incluye CLI con paginación e interfaz web Flask + Bootstrap.
```

**Topics**
```
python oop poo flask bootstrap hospital-management csv unittest spanish educational-project
```

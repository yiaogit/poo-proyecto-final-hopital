# Changelog

Todas las modificaciones notables de este proyecto quedan documentadas aquí.

El formato sigue las convenciones de [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/)
y el proyecto se adhiere al [Versionado Semántico](https://semver.org/lang/es/).

---

## [2.0.0] — 2026-05-12

### Añadido
- **CRUD completo en `Hospital`**: nuevos métodos `buscar_por_dni`, `eliminar_por_dni` y el método mágico `__contains__` (permite `"DNI" in hospital`).
- **Búsqueda por DNI en la CLI** (opción 5 del menú) y en la web (`/buscar` con plantilla `buscar.html`).
- **Eliminación por DNI** en la CLI (opción 6) y en la web (botón 🗑 en las tablas de pacientes y médicos, ruta `/eliminar/<dni>`).
- **Persistencia de citas en CSV**: `GestorDatos.guardar_citas` y `cargar_citas` con un nuevo archivo `citas_db.csv`. Las citas (con sus tratamientos) ya se conservan entre sesiones.
- **Sistema de niveles en el log**: cada entrada lleva una categoría (`[CREAR]`, `[ELIMINAR]`, `[BUSCAR]`, `[CITA]`, `[INFO]`, `[ERROR]`), lo que permite filtrar con `grep`.
- **Nuevas excepciones personalizadas**: `DniDuplicadoError` (subclase de `DatoInvalidoError`) y `PersonaNoEncontradaError`.
- **Validación de DNI**: ahora se rechazan DNIs vacíos o con solo espacios.
- **Parámetro `validar_pasado`** en `Cita.__init__` para permitir restaurar citas históricas desde CSV sin que choquen con la regla "no se pueden programar citas en el pasado".
- **9 tests nuevos**: `TestHospitalCRUD` (7) y `TestPersistenciaCitas` (2). Total: 43 tests.
- **`.gitignore`** para evitar subir `venv/`, `__pycache__/`, `*.log`, etc.
- **Función auxiliar `escribir_log(nivel, mensaje)`** en `utilidades.py` para que módulos no-Persona (Hospital, GestorDatos) también puedan registrar eventos.

### Corregido
- **Bug crítico de unicidad de DNI**: aunque `Persona.__eq__` comparaba por DNI, `Hospital.agregar_persona` no validaba duplicados, lo que permitía registrar al mismo DNI varias veces. Ahora se lanza `DniDuplicadoError` y se registra en el log.
- **Mensajes de error coherentes** en la web: las excepciones de duplicado se muestran como `warning` (amarillo), las de validación como `danger` (rojo), igual que en CLI.

### Cambiado
- **`utilidades.py`**: la firma de `LogMixin.registrar_log` ahora acepta un parámetro opcional `nivel` (por defecto `"CREAR"`, compatible con código previo).
- **Menú CLI**: pasa de 5 a 7 opciones (se añaden buscar y eliminar).
- **Navegación web**: se añade el enlace "Buscar" y se elimina el botón "Guardar CSV" del navbar (los cambios ya se guardan automáticamente en cada operación).
- **Acceso a DNI**: `persistencia.py` ahora usa el atributo público `p.dni` en lugar del atributo protegido `p._dni`.
- **README**: secciones de tests, formatos de archivo y excepciones actualizadas para reflejar todo lo nuevo.

---

## [1.0.0] — 2026-05-05

### Añadido (versión inicial)
- Jerarquía de clases `Persona` → `Paciente`, `Medico` con herencia múltiple desde `LogMixin`.
- Encapsulamiento con `@property` y validación de peso, altura, edad, salario, especialidad, identificación.
- Polimorfismo con `mostrar_datos()` sobrescrito.
- Composición: `Cita` contiene `Medico` + `Paciente`; `Tratamiento` contiene `Cita`.
- Patrón Factory: `Paciente.desde_csv` y `Medico.desde_csv`.
- Persistencia de pacientes y médicos en CSV.
- Excepciones personalizadas: `DatoInvalidoError`, `MedicoNoDisponibleError`, `CitaDuplicadaError`.
- Mixin `LogMixin` con escritura en `hospital_registro.log`.
- Contenedor `Hospital` con métodos mágicos `__len__` y `__getitem__`.
- Interfaz CLI con menú de 5 opciones.
- Interfaz web Flask con 4 rutas (`/`, `/pacientes`, `/medicos`, `/citas`) y plantillas Bootstrap 5.
- Suite de 34 tests unitarios con fechas dinámicas.
- Documentación completa: README con UML, badges, instrucciones multiplataforma y solución de problemas.

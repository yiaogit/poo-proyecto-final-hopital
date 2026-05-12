# 📦 Guía de Publicación en GitHub — v2.0

Este documento contiene todos los textos y comandos listos para copiar y pegar
al publicar la versión 2.0 en GitHub.

---

## 1️⃣ Mensaje de commit recomendado

Al subir todos los cambios de la v2, usa este mensaje en español
(convención **Conventional Commits**, muy valorada profesionalmente):

```
feat(v2): CRUD completo, búsqueda por DNI y persistencia de citas

Funcionalidades nuevas:
- Hospital.buscar_por_dni, eliminar_por_dni y __contains__
- Búsqueda en CLI (opción 5) y web (/buscar + buscar.html)
- Eliminación en CLI (opción 6) y web (/eliminar + botones en tablas)
- GestorDatos.guardar_citas y cargar_citas con nuevo citas_db.csv
- Sistema de niveles en el log: [CREAR] [ELIMINAR] [BUSCAR] [CITA] [INFO] [ERROR]
- Nuevas excepciones: DniDuplicadoError, PersonaNoEncontradaError

Correcciones:
- Bug: unicidad de DNI no se validaba al agregar al hospital
- Validación de DNI vacío en Persona

Tests:
- 9 tests nuevos (TestHospitalCRUD y TestPersistenciaCitas)
- Total: 43 tests pasando

Documentación:
- README actualizado con las nuevas funcionalidades, rutas y excepciones
- Nuevo CHANGELOG.md siguiendo Keep a Changelog
- Añadidos .gitignore y LICENSE (MIT)
```

---

## 2️⃣ Pasos para subir la v2

Desde PowerShell, en tu carpeta local del repositorio:

```powershell
# 1. Asegúrate de estar en el directorio del proyecto
cd C:\Users\tangy\Desktop\poo-proyecto-final-hopital-main\poo-proyecto-final-hopital-main

# 2. Sustituye TODOS los archivos por los de la v2
#    (descomprime el ZIP en una carpeta nueva y copia su contenido aquí)

# 3. Verifica que .git/ sigue existiendo y que NO subes venv/ o __pycache__/
git status

# 4. Añade los cambios y commitea
git add .
git commit -F mensaje_commit.txt    # o usa -m "..." directamente

# 5. Push al remoto
git push
```

Si quieres usar el mensaje largo del paso 1, guárdalo primero en `mensaje_commit.txt` y usa `-F`.

---

## 3️⃣ Crear un Release en GitHub

Una vez que el push esté completo:

1. Ve a `https://github.com/yiaogit/poo-proyecto-final-hopital`
2. En la columna derecha: **Releases → Draft a new release**
3. **Choose a tag**: escribe `v2.0.0` y selecciona "Create new tag: v2.0.0 on publish"
4. **Release title**: `v2.0 — CRUD, búsqueda y persistencia de citas`
5. **Description**: copia el bloque de abajo
6. Pulsa **Publish release**

### Texto para la descripción del Release

```markdown
## 🎉 Versión 2.0 — Funcionalidad completa de gestión

Esta versión transforma el proyecto de una demostración POO en un sistema
de gestión hospitalaria realmente operativo: ahora puedes buscar, eliminar
y conservar todo el estado del hospital (incluidas las citas) entre sesiones.

### ✨ Lo nuevo

- 🔍 **Búsqueda por DNI** en CLI y web (`/buscar`)
- 🗑️ **Eliminación de personas** con confirmación visual
- 💾 **Persistencia de citas** en `citas_db.csv` (incluye tratamientos)
- 📜 **Log categorizado**: `[CREAR]` `[ELIMINAR]` `[BUSCAR]` `[CITA]` `[INFO]` `[ERROR]`
- ⚠️ **Dos excepciones nuevas**: `DniDuplicadoError`, `PersonaNoEncontradaError`

### 🐛 Bug corregido

La unicidad de DNI no se validaba al agregar al hospital, lo que permitía
registrar la misma persona varias veces. Ahora se lanza `DniDuplicadoError`.

### 🧪 Tests

- **43 tests pasando** (antes 34)
- Dos nuevos `TestCase`: `TestHospitalCRUD` y `TestPersistenciaCitas`

### 📦 Instalación

Consulta el [README](README.md) para las instrucciones multiplataforma
(Windows / macOS / Linux).

### 📋 Historial completo

Ver [`CHANGELOG.md`](CHANGELOG.md).
```

---

## 4️⃣ Personalizar el "About" del repositorio

En la página principal del repo, junto al título, pulsa el icono ⚙️ "About"
de la columna derecha y rellena:

- **Description**:
  ```
  Sistema de gestión hospitalaria en Python aplicando POO. Incluye CLI y interfaz web con Flask.
  ```

- **Website**: (déjalo vacío o pon una URL de demo si la subes)

- **Topics** (etiquetas, separadas por espacio o intro):
  ```
  python oop poo flask bootstrap hospital-management
  csv unittest mvc spanish educational-project
  ```

- Marca ✅ **Releases** para que aparezca en la barra lateral.

---

## 5️⃣ Verificación post-publicación

Después de publicar, comprueba en la web del repo:

- [ ] El badge `tests-43 passing` aparece en verde en el README
- [ ] El badge `version-2.0` aparece en violeta
- [ ] El UML de Mermaid se renderiza correctamente
- [ ] Hay un Release `v2.0.0` listado en la columna derecha
- [ ] Los Topics están visibles bajo el About
- [ ] LICENSE aparece como "MIT license" al lado del About
- [ ] El CHANGELOG.md se ve en la lista de archivos

Si todo está marcado, el repositorio está listo para presentar y/o defender. 🎓

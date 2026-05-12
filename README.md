# 🏥 Sistema de Gestión Hospitalaria — Hospital UEV

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![Flask](https://img.shields.io/badge/flask-3.0+-lightgrey.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![POO](https://img.shields.io/badge/paradigma-POO-orange.svg)
![Tests](https://img.shields.io/badge/tests-34%20passing-brightgreen.svg)

Simulación de un sistema de gestión hospitalaria desarrollado en **Python**, aplicando los pilares fundamentales de la **Programación Orientada a Objetos (POO)**. Permite gestionar médicos, pacientes, citas y tratamientos con persistencia en CSV, trazabilidad mediante logs y dos interfaces de usuario (CLI y Web).

---

## 📑 Tabla de Contenidos

- [✨ Características](#-características)
- [🚀 Estructura del Proyecto](#-estructura-del-proyecto)
- [⚙️ Instalación](#️-instalación)
- [🖥️ Uso](#️-uso)
- [❓ Solución de problemas comunes](#-solución-de-problemas-comunes)
- [👥 Roles y Responsabilidades](#-roles-y-responsabilidades)
- [📊 Arquitectura del Sistema (UML)](#-arquitectura-del-sistema-uml)
- [🧪 Tests](#-tests)
- [🎓 Conceptos POO Demostrados](#-conceptos-poo-demostrados)
- [📁 Formatos de archivo](#-formatos-de-archivo)

---

## ✨ Características

- 🧬 **Jerarquía de clases** con herencia simple y múltiple (Mixin)
- 🔒 **Encapsulamiento** con validación automática vía `@property`
- 🎭 **Polimorfismo** sobre lista heterogénea de personas
- 🧩 **Composición** entre citas, médicos, pacientes y tratamientos
- 🏭 **Patrón Factory** para reconstrucción desde CSV
- ⚠️ **Excepciones personalizadas** para reglas de dominio
- 💾 **Persistencia automática** en archivos CSV
- 📜 **Sistema de logs** con timestamps mediante Mixin
- 🖥️ **Doble interfaz**: menú por consola (CLI) e interfaz web (Flask + Bootstrap)
- 🧪 **Suite de 34 tests unitarios** con fechas dinámicas (no caducan)

---

## 🚀 Estructura del Proyecto

```
poo-proyecto-final-hospital/
│
├── 📄 entidades.py         # Persona, Paciente, Medico, DatoInvalidoError
├── 📄 logica.py            # Cita, Tratamiento + excepciones de negocio
├── 📄 persistencia.py      # GestorDatos (lectura/escritura CSV)
├── 📄 hospital.py          # Hospital (contenedor heterogéneo)
├── 📄 utilidades.py        # LogMixin (auditoría automática)
├── 📄 main.py              # CLI: menú interactivo
├── 📄 app.py               # Web: servidor Flask
│
├── 📂 templates/           # Plantillas HTML (Jinja2 + Bootstrap 5)
│   ├── base.html
│   ├── index.html
│   ├── pacientes.html
│   ├── medicos.html
│   └── citas.html
│
├── 📊 pacientes_db.csv     # Base de datos de pacientes
├── 📊 medicos_db.csv       # Base de datos de médicos
├── 🧪 test_sistema.py      # 34 tests unitarios
├── 📋 requirements.txt     # Dependencias
└── 📖 README.md            # Este archivo
```

---

## ⚙️ Instalación

### Requisitos previos

- **Python 3.10 o superior** — [Descargar Python](https://www.python.org/downloads/)
- **Git** (opcional, solo si vas a clonar en lugar de descargar el ZIP) — [Descargar Git](https://git-scm.com/downloads)

> 💡 **Verifica tu versión de Python** antes de empezar:
> ```bash
> python --version      # Windows
> python3 --version     # macOS / Linux
> ```
> Si la versión es inferior a 3.10, descarga una más reciente del enlace de arriba.

### Obtener el código

**Opción A — Clonar con Git** (recomendado):
```bash
git clone https://github.com/yiaogit/poo-proyecto-final-hopital.git
cd poo-proyecto-final-hopital
```

**Opción B — Descargar ZIP**:
1. Ve a la página del repositorio
2. Pulsa el botón verde **Code → Download ZIP**
3. Descomprime el archivo y abre una terminal dentro de la carpeta resultante

### Instalación según tu sistema operativo

<details>
<summary><b>🪟 Windows (PowerShell)</b></summary>

```powershell
# 1. Crear entorno virtual
python -m venv venv

# 2. Activar el entorno
venv\Scripts\Activate.ps1

# Si PowerShell rechaza ejecutar scripts, ejecuta UNA VEZ:
# Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned

# 3. Instalar dependencias
pip install -r requirements.txt
```

Verás `(venv)` al inicio de tu prompt cuando el entorno esté activo.
</details>

<details>
<summary><b>🪟 Windows (CMD)</b></summary>

```cmd
python -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt
```
</details>

<details>
<summary><b>🍎 macOS</b></summary>

```bash
# 1. Crear entorno virtual (usa python3 en macOS)
python3 -m venv venv

# 2. Activar el entorno
source venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt
```

> Si `python3` no está instalado, instálalo con [Homebrew](https://brew.sh):
> ```bash
> brew install python
> ```
</details>

<details>
<summary><b>🐧 Linux (Ubuntu / Debian)</b></summary>

```bash
# Si Python no está instalado:
sudo apt update && sudo apt install python3 python3-venv python3-pip -y

# 1. Crear entorno virtual
python3 -m venv venv

# 2. Activar el entorno
source venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt
```
</details>

---

## 🖥️ Uso

> ℹ️ En **macOS/Linux** sustituye `python` por `python3` en todos los comandos.
> En **Windows** usa `python` tal cual.

### Interfaz por consola (CLI)

```bash
python main.py
```

```
--- MENÚ: Hospital Universitario UEV ---
1. Agregar paciente
2. Agregar médico
3. Mostrar personas (Polimorfismo)
4. Programar Cita y Tratamiento
5. Salir y Guardar
```

### Interfaz web (Flask)

```bash
python app.py
```

Abre <http://127.0.0.1:5000> en el navegador. La interfaz web reutiliza **exactamente las mismas clases** del modelo de dominio — Flask actúa solo como capa de presentación.

Para detener el servidor, pulsa `Ctrl + C` en la terminal.

### Salir del entorno virtual

Cuando termines de trabajar:

```bash
deactivate
```

---

## ❓ Solución de problemas comunes

<details>
<summary><b>"python no se reconoce como comando" (Windows)</b></summary>

Python no está en el `PATH`. Reinstala desde [python.org](https://www.python.org/downloads/) marcando la casilla **"Add Python to PATH"** durante la instalación.
</details>

<details>
<summary><b>"command not found: python" (macOS)</b></summary>

En macOS el comando es `python3`, no `python`. Si tampoco existe, instala vía Homebrew: `brew install python`.
</details>

<details>
<summary><b>"jinja2.exceptions.TemplateNotFound: index.html"</b></summary>

La carpeta `templates/` debe estar **al mismo nivel** que `app.py`. Comprueba que existe y contiene los 5 archivos HTML.
</details>

<details>
<summary><b>"No se pueden programar citas en el pasado" al ejecutar tests</b></summary>

Esto solo pasaría si usaras versiones antiguas de los tests con fechas fijas. El `test_sistema.py` de este repositorio usa fechas dinámicas y nunca caduca.
</details>

<details>
<summary><b>PowerShell: "no se puede cargar el archivo Activate.ps1"</b></summary>

Ejecuta una sola vez con permisos de administrador:
```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```
</details>

---

## 👥 Roles y Responsabilidades

### 👤 Integrante 1 · Arquitecto de Entidades
- **Jerarquía de Herencia**: Diseño de `Persona` como clase base y derivación de `Paciente` y `Medico`.
- **Encapsulamiento**: Uso intensivo de `@property` con validaciones (peso, altura, edad, salario, especialidad, identificación).
- **Polimorfismo**: Sobrescritura del método `mostrar_datos()` en cada subclase.
- **Excepción personalizada**: Implementación de `DatoInvalidoError`.
- **Métodos mágicos en `Persona`**: `__eq__` (igualdad por DNI) y `__lt__` (orden alfabético).

### 👤 Integrante 2 · Gestor de Operaciones
- **Composición**: `Cita` posee un `Medico` y un `Paciente`; `Tratamiento` posee una `Cita`.
- **Excepciones personalizadas**: `MedicoNoDisponibleError` y `CitaDuplicadaError`.
- **Validaciones de negocio**: Formato de fecha `DD/MM/AAAA HH:MM`, rechazo de fechas pasadas, validación del motivo y verificación de tipos.
- **Sistema de tarifas**: `TARIFAS` con cinco tipos de tratamiento y descuento automático del 40% para pacientes con seguro.
- **Métodos mágicos en `Cita` y `Tratamiento`**: `__str__`, `__repr__`, `__eq__`, `__lt__` (orden cronológico real).

### 👤 Integrante 3 · Especialista en Datos
- **Persistencia**: Clase `GestorDatos` con métodos estáticos para guardar y cargar pacientes y médicos en CSV independientes.
- **Patrón Factory**: `@classmethod desde_csv()` en `Paciente` y `Medico` con flag `es_nuevo=False` para evitar logs duplicados.
- **Mixin de logging**: `LogMixin` con `registrar_log()`, heredado por `Paciente` y `Medico`.
- **Gestión de archivos**: Uso de `with open(...)` y comprobación de existencia con `os.path.exists`.

### 👤 Integrante 4 · Integrador
- **Contenedor `Hospital`**: Lista heterogénea `_directorio` con `__len__` y `__getitem__`.
- **Flujo principal**: Menú interactivo en `main.py` con cinco opciones.
- **Manejo de excepciones**: Captura escalonada de `ValueError`, `DatoInvalidoError`, `MedicoNoDisponibleError`.
- **Integración**: Orquestación del ciclo carga → operaciones → guardado.

---

## 📊 Arquitectura del Sistema (UML)

```mermaid
classDiagram
    class Persona {
        +str nombre
        #int _edad
        #str _dni
        +edad() property
        +dni() property
        +mostrar_datos()
        +__eq__(other)
        +__lt__(other)
    }

    class LogMixin {
        +registrar_log(mensaje)
    }

    class Paciente {
        +float peso
        +float altura
        +bool seguro
        +list agenda
        +imc() property
        +clasificar_imc()
        +mostrar_datos()
        +desde_csv(linea_csv)$
    }

    class Medico {
        +float salario
        +str especialidad
        +str identificacion
        +list agenda
        +mostrar_datos()
        +desde_csv(linea_csv)$
    }

    class Cita {
        +Medico medico
        +Paciente paciente
        +str fecha_hora
        +datetime _fecha_obj
        +str motivo
        +Tratamiento tratamiento
    }

    class Tratamiento {
        +dict TARIFAS$
        +float DESCUENTO_SEGURO$
        +Cita cita
        +str tipo
        +calcular_costo()
    }

    class Hospital {
        +str nombre
        -list _directorio
        +agregar_persona(persona)
        +__len__()
        +__getitem__(index)
    }

    class GestorDatos {
        +str ARCHIVO_PACIENTES$
        +str ARCHIVO_MEDICOS$
        +guardar_pacientes(lista)$
        +cargar_pacientes(clase)$
        +guardar_medicos(lista)$
        +cargar_medicos(clase)$
    }

    Persona <|-- Paciente
    Persona <|-- Medico
    LogMixin <|-- Paciente : Mixin
    LogMixin <|-- Medico  : Mixin

    Cita *-- Medico    : Composición
    Cita *-- Paciente  : Composición
    Tratamiento *-- Cita : Composición

    Hospital o-- Persona : Agregación

    GestorDatos ..> Paciente : Factory
    GestorDatos ..> Medico   : Factory
```

### Excepciones del sistema

| Excepción | Definida en | Se lanza cuando... |
|---|---|---|
| `DatoInvalidoError` | `entidades.py` | Peso/altura ≤ 0, salario negativo, especialidad o ID vacíos. |
| `MedicoNoDisponibleError` | `logica.py` | El médico ya tiene una cita en ese horario. |
| `CitaDuplicadaError` | `logica.py` | El paciente ya tiene una cita en ese horario. |

---

## 🧪 Tests

Suite con `unittest` que cubre clases del dominio, patrón Factory, métodos mágicos y excepciones personalizadas:

```bash
python -m unittest test_sistema -v
```

```
Ran 34 tests in 0.012s
OK
```

Los tests usan fechas dinámicas (`datetime.now() + timedelta`), por lo que **no caducan** con el paso del tiempo.

---

## 🎓 Conceptos POO Demostrados

| Concepto | Dónde se ve |
|---|---|
| **Herencia simple** | `Paciente(Persona)`, `Medico(Persona)` |
| **Herencia múltiple** | `Paciente(Persona, LogMixin)`, `Medico(Persona, LogMixin)` |
| **Encapsulamiento** | `@property` + `@setter` con validación en cada atributo crítico |
| **Polimorfismo** | `mostrar_datos()` sobrescrito; iteración sobre lista heterogénea de `Persona` |
| **Composición** | `Cita` ⟶ `Medico` + `Paciente`; `Tratamiento` ⟶ `Cita` |
| **Agregación** | `Hospital` agrupa objetos `Persona` |
| **Mixin** | `LogMixin` añade logging sin ser parte de la jerarquía principal |
| **Patrón Factory** | `Paciente.desde_csv()` y `Medico.desde_csv()` |
| **Métodos mágicos** | `__eq__`, `__lt__`, `__str__`, `__repr__`, `__len__`, `__getitem__` |
| **Excepciones personalizadas** | `DatoInvalidoError`, `MedicoNoDisponibleError`, `CitaDuplicadaError` |
| **Gestión de archivos** | `with open(...)` en `GestorDatos` y `LogMixin` |

---

## 📁 Formatos de archivo

**`pacientes_db.csv`** — `nombre,edad,dni,peso,altura,seguro`
```
María García López,34,12345678A,62,1.65,True
Carlos Martínez Ruiz,58,23456789B,88,1.78,True
```

**`medicos_db.csv`** — `nombre,edad,dni,salario,especialidad,identificacion`
```
Ana Torres Vidal,45,11111111X,3500,Cardiología,COL-001
Roberto Sánchez Pérez,52,22222222Y,4200,Pediatría,COL-002
```

**`hospital_registro.log`**
```
[2026-05-12 14:23:01] Nuevo paciente creado: María García López (DNI: 12345678A)
[2026-05-12 14:23:05] Nuevo médico registrado: Dr./Dra. Ana Torres Vidal (Especialidad: Cardiología, ID: COL-001)
```

---

## 📝 Licencia

Este proyecto se distribuye bajo licencia MIT — uso libre con atribución.

## 👨‍💻 Autores

Equipo de 4 integrantes — Proyecto Final de Programación Orientada a Objetos.

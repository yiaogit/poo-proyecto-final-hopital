# 🏗️ Sistema de Gestión Hospitalaria - Proyecto POO

Este proyecto es una simulación de un sistema de gestión hospitalaria desarrollado en **Python**, aplicando los pilares fundamentales de la **Programación Orientada a Objetos (POO)**. El sistema permite gestionar médicos, pacientes, citas y tratamientos con persistencia de datos y trazabilidad mediante logs.

## 🚀 Estructura del Proyecto

El sistema está diseñado de forma modular para facilitar la colaboración y el mantenimiento:

* **`entidades.py`**: Contiene las clases base y modelos principales (`Persona`, `Paciente`, `Medico`) y validaciones de datos.
* **`logica.py`**: Define la lógica de negocio, incluyendo la gestión de `Cita`, `Tratamiento` y excepciones personalizadas.
* **`persistencia.py`**: Encargado de la lectura y escritura de objetos en archivos CSV.
* **`utilidades.py`**: Contiene herramientas transversales como el `LogMixin`.
* **`main_py.py`**: El punto de entrada principal con el menú interactivo para el usuario.

## 👥 Roles y Responsabilidades

### 👤 Integrante 1: Arquitecto de Entidades
* **Aportes**: Implementación de la jerarquía de **Herencia**, uso de **Encapsulamiento** con `@property` (validación de edad, peso, altura) y **Polimorfismo** con `mostrar_datos()`.

### 👤 Integrante 2: Gestor de Operaciones
* **Aportes**: Implementación de **Composición** (`Cita` posee un médico y un paciente; `Tratamiento` posee una cita) y creación de **Excepciones** específicas (`MedicoNoDisponibleError`).

### 👤 Integrante 3: Especialista en Datos (Tu Rol)
* **Aportes**: 
    * **Persistencia**: Clase `GestorDatos` con manejo de archivos `with open()`.
    * **Patrón Factory**: Método `@classmethod desde_csv()` en la clase `Paciente`.
    * **Mixins**: Implementación de `LogMixin` para registrar acciones automáticamente.
    * **Métodos Mágicos**: Implementación de `__eq__` (comparación por DNI) y `__str__`.

### 👤 Integrante 4: Integrador
* **Aportes**: Desarrollo del flujo principal en `main_py.py`, integración de módulos y gestión del ciclo de vida de los datos (carga al inicio, guardado al salir).

## 📊 Arquitectura del Sistema (UML)

```mermaid
classDiagram
    class Persona {
        +str nombre
        #int _edad
        #str _dni
        +mostrar_datos()
    }

    class LogMixin {
        +registrar_log(mensaje)
    }

    class Paciente {
        +float peso
        +float altura
        +bool seguro
        +imc() property
        +desde_csv(linea)$
    }

    class Medico {
        +float salario
        +str especialidad
        +identificacion
    }

    class Cita {
        +Medico medico
        +Paciente paciente
        +str fecha_hora
        +str motivo
    }

    class Tratamiento {
        +Cita cita
        +str tipo
        +calcular_costo()
    }

    Persona <|-- Paciente
    Persona <|-- Medico
    LogMixin <|-- Paciente : Mixin
    Cita *-- Medico : Composición
    Cita *-- Paciente : Composición
    Tratamiento *-- Cita : Composición

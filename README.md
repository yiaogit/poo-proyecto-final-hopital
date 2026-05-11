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
* **Aportes**: Implementación de la jerarquía de **Herencia**, uso de **Encapsulamiento** con `@property` y **Polimorfismo** con el método `mostrar_datos()` sobrescrito en las subclases.

### 👤 Integrante 2: Gestor de Operaciones
* **Aportes**: Implementación de **Composición** (`Cita` posee un médico y un paciente) y creación de **Excepciones** específicas (`MedicoNoDisponibleError`).

### 👤 Integrante 3: Especialista en Datos (Tu Rol)
* **Aportes**: 
    * **Persistencia**: Clase `GestorDatos` para la gestión técnica de archivos CSV.
    * **Patrón Factory**: Método `@classmethod desde_csv()` en `Paciente` para reconstruir objetos desde texto.
    * **Mixins**: Implementación de `LogMixin` para registro automático de eventos.
    * **Métodos Mágicos**: Implementación de `__eq__` (comparación por DNI) y `__lt__` para ordenamiento.

### 👤 Integrante 4: Integrador
* **Aportes**: Desarrollo del flujo principal en `main_py.py`, gestión del ciclo de vida de los datos e integración de módulos.

## 📊 Arquitectura del Sistema (UML Preciso)

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

    class GestorDatos {
        +str ARCHIVO_PACIENTES$
        +guardar_pacientes(lista_pacientes)$
        +cargar_pacientes(clase_paciente)$
    }

    class Paciente {
        +float peso
        +float altura
        +bool seguro
        +list agenda
        +imc() property
        +desde_csv(linea_csv)$
        +mostrar_datos()
    }

    class Medico {
        +float salario
        +str especialidad
        +str identificacion
        +list agenda
        +mostrar_datos()
    }

    class Cita {
        +Medico medico
        +Paciente paciente
        +str fecha_hora
        +str motivo
        +Tratamiento tratamiento
    }

    class Tratamiento {
        +Cita cita
        +str tipo
        +str descripcion
        +calcular_costo()
    }

    Persona <|-- Paciente
    Persona <|-- Medico
    LogMixin <|-- Paciente : Mixin
    GestorDatos ..> Paciente : Dependencia (Factory)
    
    Cita *-- Medico : Composición
    Cita *-- Paciente : Composición
    Tratamiento *-- Cita : Composición

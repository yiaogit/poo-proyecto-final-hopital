import unittest
from datetime import datetime, timedelta
from entidades import Paciente, Medico, Persona, DatoInvalidoError
from logica import Cita, Tratamiento, MedicoNoDisponibleError


# ─────────────────────────────────────────
# Helper: genera fechas futuras dinámicamente
# Así los tests no caducan con el paso del tiempo.
# ─────────────────────────────────────────
def _fecha_futura(dias=30, hora="10:00"):
    """Devuelve una cadena 'DD/MM/YYYY HH:MM' con una fecha futura."""
    f = datetime.now() + timedelta(days=dias)
    return f.strftime("%d/%m/%Y") + " " + hora


class TestPersona(unittest.TestCase):
    """Tests para la clase base Persona (a través de Paciente y Medico)."""

    def test_edad_valida(self):
        """Un paciente con edad válida se crea correctamente."""
        p = Paciente("Ana Garcia", 30, "12345678A", 65, 1.68)
        self.assertEqual(p.edad, 30)

    def test_edad_invalida_negativa(self):
        """Una edad negativa lanza DatoInvalidoError."""
        with self.assertRaises((DatoInvalidoError, ValueError)):
            Paciente("Test", -1, "00000000X", 65, 1.68)

    def test_edad_invalida_mayor_120(self):
        """Una edad mayor de 120 lanza DatoInvalidoError."""
        with self.assertRaises((DatoInvalidoError, ValueError)):
            Paciente("Test", 200, "00000000X", 65, 1.68)

    def test_dni_solo_lectura(self):
        """El DNI no se puede modificar desde fuera."""
        p = Paciente("Ana Garcia", 30, "12345678A", 65, 1.68)
        with self.assertRaises(AttributeError):
            p.dni = "99999999Z"

    # CRITICAL
    def test_eq_mismo_dni(self):
        """Dos personas con el mismo DNI son iguales (__eq__)."""
        p1 = Paciente("Ana Garcia", 30, "12345678A", 65, 1.68)
        p2 = Paciente("Otra Persona", 25, "12345678A", 70, 1.70)
        self.assertEqual(p1, p2)  # mismo DNI → iguales

    def test_eq_distinto_dni(self):
        """Dos personas con distinto DNI no son iguales."""
        p1 = Paciente("Ana Garcia", 30, "12345678A", 65, 1.68)
        p2 = Paciente("Ana Garcia", 30, "99999999Z", 65, 1.68)
        self.assertNotEqual(p1, p2)

    def test_lt_orden_alfabetico(self):
        """__lt__ ordena personas alfabéticamente por nombre."""
        p = Paciente("Ana Garcia", 30, "12345678A", 65, 1.68)
        m = Medico("Luis Perez", 45, "87654321B", 50000, "Cardiologia", "COL-001")
        self.assertLess(p, m)  # Ana < Luis


class TestPaciente(unittest.TestCase):
    """Tests para la clase Paciente."""

    def setUp(self):
        """Crea un paciente base para reutilizar en los tests."""
        self.paciente = Paciente("Ana Garcia", 30, "12345678A", 65, 1.68, True)

    def test_str(self):
        """__str__ devuelve el formato correcto."""
        self.assertIn("Ana Garcia", str(self.paciente))
        self.assertIn("12345678A", str(self.paciente))

    def test_imc_calculado(self):
        """El IMC se calcula correctamente a partir de peso y altura."""
        imc_esperado = round(65 / (1.68 ** 2), 2)
        self.assertEqual(self.paciente.imc, imc_esperado)

    def test_peso_invalido(self):
        """Un peso negativo o cero lanza DatoInvalidoError."""
        with self.assertRaises(DatoInvalidoError):
            Paciente("Test", 30, "00000000X", -10, 1.68)

    def test_altura_invalida(self):
        """Una altura de cero lanza DatoInvalidoError."""
        with self.assertRaises(DatoInvalidoError):
            Paciente("Test", 30, "00000000X", 65, 0)

    def test_seguro_por_defecto(self):
        """El seguro es False por defecto si no se especifica."""
        p = Paciente("Test", 30, "00000000X", 65, 1.68)
        self.assertFalse(p.seguro)

    # CRITICAL
    def test_desde_csv(self):
        """
        Factory pattern: desde_csv crea un Paciente correcto
        a partir de una línea de texto CSV.
        """
        linea = "Carlos Ruiz,25,11111111C,80,1.75,True"
        p = Paciente.desde_csv(linea)
        self.assertEqual(p.nombre, "Carlos Ruiz")
        self.assertEqual(p.edad, 25)
        self.assertEqual(p.dni, "11111111C")
        self.assertAlmostEqual(p.peso, 80.0)
        self.assertAlmostEqual(p.altura, 1.75)
        self.assertTrue(p.seguro)

    def test_mostrar_datos_con_seguro(self):
        """mostrar_datos incluye 'Con seguro' si el paciente tiene seguro."""
        resultado = self.paciente.mostrar_datos()
        self.assertIn("Con seguro", resultado)

    def test_mostrar_datos_sin_seguro(self):
        """mostrar_datos incluye 'Sin seguro' si el paciente no tiene seguro."""
        p = Paciente("Test", 30, "00000000X", 65, 1.68, False)
        self.assertIn("Sin seguro", p.mostrar_datos())


class TestMedico(unittest.TestCase):
    """Tests para la clase Medico."""

    def setUp(self):
        self.medico = Medico("Luis Perez", 45, "87654321B", 50000, "Cardiologia", "COL-001")

    def test_especialidad_vacia(self):
        """Una especialidad vacía lanza DatoInvalidoError."""
        with self.assertRaises(DatoInvalidoError):
            Medico("Test", 40, "00000000X", 3000, "   ", "COL-002")

    def test_identificacion_vacia(self):
        """Un ID colegiado vacío lanza DatoInvalidoError."""
        with self.assertRaises(DatoInvalidoError):
            Medico("Test", 40, "00000000X", 3000, "Cardiologia", "")

    def test_str(self):
        """__str__ incluye Dr./Dra. y la especialidad."""
        resultado = str(self.medico)
        self.assertIn("Dr.", resultado)
        self.assertIn("Cardiologia", resultado)

    def test_salario_invalido(self):
        """Un salario negativo lanza DatoInvalidoError."""
        with self.assertRaises(DatoInvalidoError):
            Medico("Test", 40, "00000000X", -100, "Pediatria", "COL-002")

    def test_salario_cero_valido(self):
        """Un salario de 0 es válido (becario, residente)."""
        m = Medico("Test", 30, "00000000X", 0, "Pediatria", "COL-002")
        self.assertEqual(m.salario, 0)

    def test_agenda_empieza_vacia(self):
        """La agenda de un médico empieza vacía."""
        self.assertEqual(len(self.medico.agenda), 0)


class TestPolimorfismo(unittest.TestCase):
    """
    Tests que demuestran polimorfismo: misma llamada a mostrar_datos()
    produce resultados distintos según el tipo de objeto.
    """

    def setUp(self):
        self.paciente = Paciente("Ana Garcia", 30, "12345678A", 65, 1.68, True)
        self.medico = Medico("Luis Perez", 45, "87654321B", 50000, "Cardiologia", "COL-001")

    # CRITICAL
    def test_polimorfismo_mostrar_datos(self):
        """
        Una lista heterogénea de Persona llama a mostrar_datos() en cada objeto
        y cada uno devuelve su propia representación (polimorfismo).
        """
        personas = [self.paciente, self.medico]
        resultados = [p.mostrar_datos() for p in personas]

        # Paciente muestra IMC y seguro
        self.assertIn("IMC", resultados[0])
        self.assertIn("Con seguro", resultados[0])

        # Medico muestra colegiado, no IMC
        self.assertIn("COL-001", resultados[1])
        self.assertNotIn("IMC", resultados[1])

    def test_todos_son_persona(self):
        """Paciente y Medico son instancias de Persona (herencia)."""
        self.assertIsInstance(self.paciente, Persona)
        self.assertIsInstance(self.medico, Persona)

    def test_sorted_por_nombre(self):
        """sorted() funciona en una lista mixta gracias a __lt__."""
        personas = [self.medico, self.paciente]  # Luis, Ana
        ordenados = sorted(personas)
        self.assertEqual(ordenados[0].nombre, "Ana Garcia")
        self.assertEqual(ordenados[1].nombre, "Luis Perez")


class TestCita(unittest.TestCase):
    """Tests para la clase Cita."""

    def setUp(self):
        self.medico = Medico("Luis Perez", 45, "87654321B", 50000, "Cardiologia", "COL-001")
        self.paciente = Paciente("Ana Garcia", 30, "12345678A", 65, 1.68, True)
        # Fecha base reutilizada por varios tests (siempre en el futuro)
        self.fecha_base = _fecha_futura(30, "10:00")

    def test_cita_fecha_invalida(self):
        """Un formato de fecha incorrecto o fecha irreal lanza ValueError."""
        # Formato incorrecto (guiones en lugar de barras). Usamos año futuro
        # para que el fallo sea SOLO por formato, no por fecha pasada.
        with self.assertRaises(ValueError):
            Cita(self.medico, self.paciente, "15-06-2099", "Revisión")
        # Fecha irreal (32 de enero) en año futuro
        with self.assertRaises(ValueError):
            Cita(self.medico, self.paciente, "32/01/2099 10:00", "Revisión")

    def test_motivo_vacio(self):
        """Un motivo vacío o lleno de espacios lanza ValueError."""
        with self.assertRaises(ValueError):
            Cita(self.medico, self.paciente, self.fecha_base, "   ")

    def test_cita_se_crea_correctamente(self):
        """Una cita válida se crea y aparece en la agenda del médico."""
        cita = Cita(self.medico, self.paciente, self.fecha_base, "Revisión")
        self.assertIn(cita, self.medico.agenda)

    def test_str_cita(self):
        """__str__ de Cita incluye médico, paciente y fecha."""
        cita = Cita(self.medico, self.paciente, self.fecha_base, "Revisión")
        resultado = str(cita)
        self.assertIn(self.fecha_base, resultado)
        self.assertIn("Luis Perez", resultado)

    def test_cita_duplicada_lanza_excepcion(self):
        """Crear dos citas en el mismo horario lanza MedicoNoDisponibleError."""
        Cita(self.medico, self.paciente, self.fecha_base, "Primera")
        with self.assertRaises(MedicoNoDisponibleError):
            Cita(self.medico, self.paciente, self.fecha_base, "Duplicada")

    def test_orden_cronologico(self):
        """sorted() ordena citas cronológicamente gracias a __lt__."""
        fecha_temprana = _fecha_futura(30, "10:00")
        fecha_tardia = _fecha_futura(60, "09:00")
        cita1 = Cita(self.medico, self.paciente, fecha_tardia, "Segunda")
        cita2 = Cita(self.medico, self.paciente, fecha_temprana, "Primera")
        ordenadas = sorted([cita1, cita2])
        self.assertEqual(ordenadas[0].fecha_hora, fecha_temprana)


class TestTratamiento(unittest.TestCase):
    """Tests para la clase Tratamiento y cálculo de costos."""

    def setUp(self):
        medico = Medico("Luis Perez", 45, "87654321B", 50000, "Cardiologia", "COL-001")
        medico2 = Medico("Sara Lopez", 40, "22222222B", 45000, "Pediatria", "COL-002")
        self.paciente_con_seguro = Paciente("Ana Garcia", 30, "12345678A", 65, 1.68, True)
        self.paciente_sin_seguro = Paciente("Carlos Ruiz", 25, "11111111C", 80, 1.75, False)
        # Fechas futuras dinámicas para evitar caducidad
        fecha1 = _fecha_futura(30, "10:00")
        fecha2 = _fecha_futura(30, "11:00")
        self.cita_con_seguro = Cita(medico, self.paciente_con_seguro, fecha1, "Revisión")
        self.cita_sin_seguro = Cita(medico2, self.paciente_sin_seguro, fecha2, "Consulta")

    def test_costo_sin_seguro(self):
        """Sin seguro el costo es la tarifa completa."""
        t = Tratamiento(self.cita_sin_seguro, "consulta", "Revisión general")
        self.assertEqual(t.calcular_costo(), 50.0)

    def test_costo_con_seguro(self):
        """Con seguro se aplica un 40% de descuento."""
        t = Tratamiento(self.cita_con_seguro, "consulta", "Revisión general")
        self.assertEqual(t.calcular_costo(), 30.0)  # 50 * 0.60

    def test_tipo_invalido(self):
        """Un tipo de tratamiento no reconocido lanza ValueError."""
        with self.assertRaises(ValueError):
            Tratamiento(self.cita_con_seguro, "masaje", "No existe")

    def test_str_tratamiento(self):
        """__str__ incluye el tipo y el costo."""
        t = Tratamiento(self.cita_con_seguro, "consulta", "Electrocardiograma")
        resultado = str(t)
        self.assertIn("Consulta", resultado)
        self.assertIn("30.00", resultado)


# ─────────────────────────────────────────
# Tests para las funcionalidades nuevas de la V2:
# CRUD del Hospital, unicidad de DNI y persistencia de citas.
# ─────────────────────────────────────────

class TestHospitalCRUD(unittest.TestCase):
    """Tests para las operaciones CRUD del contenedor Hospital."""

    def setUp(self):
        from hospital import Hospital
        self.hospital = Hospital("Test")
        self.p = Paciente("Ana", 30, "11111111A", 60, 1.65, es_nuevo=False)
        self.m = Medico("Dr. X", 45, "22222222B", 4000, "Pediatría", "COL-X", es_nuevo=False)

    def test_dni_unico(self):
        """No se puede registrar dos veces el mismo DNI."""
        from hospital import DniDuplicadoError
        self.hospital.agregar_persona(self.p)
        duplicado = Paciente("Otra", 25, "11111111A", 70, 1.70, es_nuevo=False)
        with self.assertRaises(DniDuplicadoError):
            self.hospital.agregar_persona(duplicado)

    def test_dni_vacio_rechazado(self):
        """Un DNI vacío o con solo espacios lanza DatoInvalidoError."""
        with self.assertRaises(DatoInvalidoError):
            Paciente("X", 30, "", 70, 1.70, es_nuevo=False)
        with self.assertRaises(DatoInvalidoError):
            Paciente("X", 30, "   ", 70, 1.70, es_nuevo=False)

    def test_buscar_por_dni_existente(self):
        """buscar_por_dni devuelve la persona si el DNI existe."""
        self.hospital.agregar_persona(self.p)
        encontrado = self.hospital.buscar_por_dni("11111111A")
        self.assertIs(encontrado, self.p)

    def test_buscar_por_dni_inexistente(self):
        """buscar_por_dni devuelve None si el DNI no existe."""
        self.assertIsNone(self.hospital.buscar_por_dni("99999999Z"))

    def test_eliminar_por_dni(self):
        """eliminar_por_dni quita a la persona del directorio."""
        self.hospital.agregar_persona(self.p)
        self.hospital.agregar_persona(self.m)
        self.assertEqual(len(self.hospital), 2)
        eliminado = self.hospital.eliminar_por_dni("11111111A")
        self.assertEqual(eliminado.nombre, "Ana")
        self.assertEqual(len(self.hospital), 1)

    def test_eliminar_inexistente(self):
        """eliminar_por_dni lanza PersonaNoEncontradaError si no existe."""
        from hospital import PersonaNoEncontradaError
        with self.assertRaises(PersonaNoEncontradaError):
            self.hospital.eliminar_por_dni("99999999Z")

    def test_contains_dni(self):
        """El operador 'in' devuelve True si el DNI está en el hospital."""
        self.hospital.agregar_persona(self.p)
        self.assertIn("11111111A", self.hospital)
        self.assertNotIn("99999999Z", self.hospital)


class TestPersistenciaCitas(unittest.TestCase):
    """Tests para guardar y cargar citas en CSV."""

    def setUp(self):
        import os
        from hospital import Hospital
        from persistencia import GestorDatos

        # Usamos un archivo de citas distinto para no pisar el real
        self.archivo_original = GestorDatos.ARCHIVO_CITAS
        GestorDatos.ARCHIVO_CITAS = "test_citas_tmp.csv"
        if os.path.exists(GestorDatos.ARCHIVO_CITAS):
            os.remove(GestorDatos.ARCHIVO_CITAS)

        self.GestorDatos = GestorDatos
        self.hospital = Hospital("Test")
        self.p = Paciente("Luis", 40, "33333333C", 75, 1.78, seguro=True, es_nuevo=False)
        self.m = Medico("Sara", 38, "44444444D", 3500, "Cardiología", "COL-Z", es_nuevo=False)
        self.hospital.agregar_persona(self.p)
        self.hospital.agregar_persona(self.m)

    def tearDown(self):
        import os
        if os.path.exists(self.GestorDatos.ARCHIVO_CITAS):
            os.remove(self.GestorDatos.ARCHIVO_CITAS)
        self.GestorDatos.ARCHIVO_CITAS = self.archivo_original

    def test_guardar_y_cargar_cita(self):
        """Una cita persiste correctamente entre sesiones."""
        fecha = _fecha_futura(20)
        cita = Cita(self.m, self.p, fecha, "Revisión")
        Tratamiento(cita, "consulta", "Test descripción")

        self.GestorDatos.guardar_citas([cita])

        # Limpiar agendas como si fuera una sesión nueva
        self.m.agenda.clear()
        self.p.agenda.clear()

        citas_cargadas = self.GestorDatos.cargar_citas(self.hospital, Cita, Tratamiento)
        self.assertEqual(len(citas_cargadas), 1)
        restaurada = citas_cargadas[0]
        self.assertEqual(restaurada.paciente.dni, "33333333C")
        self.assertEqual(restaurada.medico.identificacion, "COL-Z")
        self.assertEqual(restaurada.fecha_hora, fecha)
        self.assertIsNotNone(restaurada.tratamiento)
        self.assertEqual(restaurada.tratamiento.tipo, "consulta")

    def test_cita_sin_tratamiento(self):
        """Una cita sin tratamiento también se persiste y restaura correctamente."""
        fecha = _fecha_futura(25)
        Cita(self.m, self.p, fecha, "Sin trat")

        self.GestorDatos.guardar_citas(self.m.agenda)
        self.m.agenda.clear()
        self.p.agenda.clear()

        citas_cargadas = self.GestorDatos.cargar_citas(self.hospital, Cita, Tratamiento)
        self.assertEqual(len(citas_cargadas), 1)
        self.assertIsNone(citas_cargadas[0].tratamiento)


if __name__ == "__main__":
    unittest.main(verbosity=2)

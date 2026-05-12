# 📦 Guía de Publicación en GitHub — v2.6

Documentación interna con los textos y pasos listos para publicar esta versión.
**Este archivo no es parte de la documentación pública** — bórralo del repo
público si no quieres mostrarlo.

---

## 🚀 Pasos para subir la v2.6

### 1. Preparar el repositorio local

```powershell
# Ve a tu carpeta local del repo
cd C:\Users\tangy\Desktop\poo-proyecto-final-hopital-main\poo-proyecto-final-hopital-main

# Descomprime el ZIP de v2.6 en otra carpeta y COPIA todo su contenido aquí
# (sobrescribe los archivos antiguos, mantén la carpeta .git oculta)

# Verifica los cambios
git status
```

Deberías ver muchos modified/new file. Confirma que NO aparece `venv/` ni `__pycache__/`.

### 2. Eliminar los archivos internos (opcional)

```powershell
# Quita esta guía si no quieres que sea pública
del GITHUB_RELEASE.md
```

### 3. Commit + push

```powershell
git add .
git commit -m "feat(v2.6): sistema de impresión profesional con identidad UEV" `
  -m "- 5 tipos de documentos imprimibles (cita, factura, informe, agenda, nómina)" `
  -m "- 5 rutas Flask /print/* con renderizado HTML y descarga PDF opcional (xhtml2pdf)" `
  -m "- Aislamiento de privacidad: documentos paciente ocultan DNI del médico" `
  -m "- Tema UEV oficial (#E63946 rojo, #1B2444 azul) + logo en navegación y cabeceras" `
  -m "- print-color-adjust: exact para impresión a color cross-platform" `
  -m "- Generador seed_data.py: 55 citas precargadas con DNI/ID coherentes" `
  -m "- Datos ampliados: 30 pacientes (antes 22), citas distribuidas en 9 meses" `
  -m "- Botones de impresión en pacientes.html, medicos.html, buscar.html, citas.html"
git push
```

### 4. Crear el Release v2.6.0

Abre en el navegador:
```
https://github.com/yiaogit/poo-proyecto-final-hopital/releases/new
```

Rellena:

| Campo | Valor |
|---|---|
| **Choose a tag** | escribe `v2.6.0` → "Create new tag: v2.6.0 on publish" |
| **Target** | `main` |
| **Title** | `v2.6 — Sistema de impresión profesional con identidad UEV` |
| **Set as latest** | ✅ |

Descripción (copia y pega):

```markdown
## 🎉 Versión 2.6 — Sistema de impresión profesional

Esta versión convierte el proyecto en un sistema de gestión hospitalaria
**completo y listo para uso interno**, con cinco tipos de documentos
imprimibles que respetan la identidad visual de la Universidad Europea
y los requisitos de privacidad médico-paciente.

### ✨ Lo nuevo

#### 🖨️ Sistema de impresión (5 documentos)

**Para el paciente:**
- 📅 Comprobante de cita
- 🧾 Factura con desglose de descuento por seguro
- 🩺 Informe clínico con IMC y clasificación OMS

**Para el personal interno:**
- 📋 Agenda completa del médico (con DNIs de pacientes)
- 💰 Nómina trimestral (últimos 3 meses, desglose mensual)

#### 🔒 Aislamiento de privacidad
Los documentos para paciente **nunca exponen el DNI del médico**,
solo el número de colegiado público (`COL-XXX`). Los documentos
internos sí incluyen toda la información, conforme a la LOPDGDD
y al RGPD UE 2016/679.

#### 🎨 Identidad visual UEV
- Logo institucional integrado en navegación y cabeceras de documentos
- Tema CSS con colores corporativos (`#E63946` rojo, `#1B2444` azul)
- Tipografía Inter para una estética moderna y profesional
- Impresión forzada a color con `print-color-adjust: exact`

#### 🌐 Cross-platform sin instalación
El sistema delega en el diálogo de impresión nativo del navegador,
funcionando en Windows, macOS y Linux sin necesidad de drivers.
Adicionalmente, cada documento puede descargarse como PDF
(`?format=pdf`, requiere `xhtml2pdf`).

#### 📊 Datos precargados
- **30 pacientes** (antes 22)
- **12 médicos**
- **55 citas** generadas por `seed_data.py`, distribuidas entre los últimos
  3 meses y los próximos 6 — perfecto para probar la nómina trimestral

### 🧪 Tests

43 tests pasando (sin cambios desde v2.5).

### 📋 Historial completo

Ver [`CHANGELOG.md`](CHANGELOG.md).
```

Pulsa **Publish release**.

---

## 🏷️ Configuración del "About" del repositorio

En la página principal, junto al título, ⚙️ "About":

**Description**:
```
Sistema interno de gestión hospitalaria en Python con POO. CLI + interfaz web Flask con impresión profesional de documentos.
```

**Topics**:
```
python oop poo flask bootstrap hospital-management healthcare csv unittest spanish printing pdf educational-project universidad-europea
```

**Marca también**: ✅ Releases

---

## ✅ Checklist post-publicación

- [ ] El badge `version-2.6` aparece en violeta en el README
- [ ] El badge `tests-43 passing` aparece en verde
- [ ] Hay un Release v2.6.0 listado como "Latest"
- [ ] La carpeta `static/` aparece con `css/` e `img/`
- [ ] Los 6 `print_*.html` aparecen en `templates/`
- [ ] No hay `venv/` ni `__pycache__/` en el repo
- [ ] El UML de Mermaid se renderiza
- [ ] El logo SVG se ve correctamente en GitHub (clic en `static/img/uev-logo.svg`)

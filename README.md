
# pyInegi

Framework en Python para facilitar el acceso, manejo, análisis y explotación de información **geográfica y estadística** del Instituto Nacional de Estadística y Geografía (INEGI).

> **Estado:** En desarrollo (versión inicial / experimental)  
> **Ámbito:** Proyecto desarrollado dentro del INEGI, sujeto a las políticas institucionales vigentes.  
> <!-- Ajusta esta nota según lo que Comunicación/Área Jurídica indique -->

---

## 🎯 Objetivo

`pyInegi` busca ofrecer una interfaz **simple, consistente y extensible** para que cualquier persona desarrolladora, analista o investigadora pueda:

- Descargar y utilizar fácilmente capas geográficas públicas del INEGI.
- Integrar datos propios con información oficial del INEGI.
- Realizar comparaciones, cálculos e indicadores geoespaciales de forma reproducible.
- Reducir el esfuerzo técnico de “pelearse” con formatos, proyecciones, claves geográficas y servicios.

---

## 🌍 Casos de uso típicos

Algunos ejemplos de lo que se busca que `pyInegi` pueda hacer:

1. **Obtener capas geográficas públicas del INEGI**  
   - Descargar el Marco Geoestadístico (AGEB, manzana, municipios, etc.).  
   - Filtrar por entidad o área de interés.  
   - Convertir a formatos estándar (GeoJSON, Shapefile, GeoPackage, etc.).

2. **Comparar datos propios contra datos oficiales del INEGI**  
   - Recibir datos de usuario (CSV, Excel, capas vectoriales).  
   - Detectar o especificar el nivel geográfico (municipio, localidad, AGEB, etc.).  
   - Unir (join) contra datos oficiales y calcular diferencias, indicadores, tasas.

3. **Automatizar flujos de análisis geoespacial**  
   - Integrar `pyInegi` dentro de scripts, notebooks o pipelines más grandes.  
   - Estandarizar el acceso a datos oficiales dentro de proyectos institucionales.

---

## 🧱 Arquitectura general

La librería está organizada en dos grandes componentes principales:

- `geografia`  
  Funcionalidades relacionadas con:
  - Capas geográficas (marco geoestadístico, límites administrativos, etc.).
  - Operaciones espaciales básicas.
  - Descarga/lectura de datasets geográficos oficiales.

- `estadistica`  
  Funcionalidades relacionadas con:
  - Indicadores estadísticos (censos, encuestas, etc.).  
  - Descarga/consulta de datos tabulares.
  - Integración y comparación con datos proporcionados por el usuario.

> La idea es que ambos componentes puedan trabajar de forma conjunta, por ejemplo:
> unir capas geográficas con indicadores estadísticos y datos del usuario.

---

## 📦 Instalación

> ⚠️ Ajusta esto según el estado real del proyecto (p. ej. si usas Git en lugar de PyPI).

```bash
pip install git+https://github.com/INEGI-Python/pyInegi.git

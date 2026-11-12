# Trabajo Práctico Integrador: Visión Artificial (Ciclo 2026)

**Carrera:** Licenciatura en Inteligencia Artificial  
**Materia:** 2026-1IA1(1) Visión Artificial y Lenguaje Natural  
**Caso de Estudio Seleccionado:** **Img 3: Retinografía Vascular Digital** (Fondo de Ojo)  
**Imagen Principal:** `data/images/3.png` ($1024 \times 680$ px)  
**Rama de Trabajo:** `Vision_Cristian`  

---

## 👥 Integrantes del Equipo de Trabajo
- **Bringas, Mateo Lautaro** — Legajo: `435719`
- **Castro, Cristian Leonel** — Legajo: `435837`
- **Garcia Pintos, Valentin** — Legajo: `435804`

---

## 📁 Estructura del Repositorio

```text
Cristulo/TPI_VisionArtificial_LenguajeNatural/
├── CONSIGNA_TPI_VisionArtificial.md          # Enunciado y pautas oficiales de la cátedra
├── README.md                                 # Documentación general del repositorio
├── data/
│   ├── images/                               # Banco de imágenes provistas
│   │   ├── 1.jpg
│   │   ├── 2.jpg
│   │   ├── 3.png                             # [IMAGEN PRINCIPAL OFICIAL]
│   │   └── 4.png
│   ├── results_metrologia_retina.csv         # Exportación oficial de métricas CCA
│   └── resumen_estadistico.txt               # Resumen de valores cuantitativos globales
├── src/
│   ├── pipeline_retina.py                    # Pipeline determinista en Python (5 etapas)
│   └── requirements.txt                      # Dependencias del entorno de procesamiento
└── docs/
    ├── TP_Integrador_VA_Grupo_XX.pdf         # [ENTREGABLE A] Informe Técnico Oficial (5 págs, PDF)
    ├── protocolo_fiji_imagej.md              # Protocolo paso a paso para Fiji No-Code GUI
    ├── cuestionario_moodle_preparacion.md    # [ENTREGABLE B] Banco de 10 preguntas y respuestas
    └── informe_latex/                        # Código fuente del informe académico
        ├── TP_Integrador_VA_Retina.tex       # Código fuente LaTeX
        ├── TP_Integrador_VA_Retina.pdf       # PDF compilado
        └── figuras/                          # Figuras y diagramas de alta resolución
            ├── fig1_diagnostico_histograma.png
            ├── fig2_flujograma_pipeline.png
            ├── fig3_memoria_grafica_etapas.png
            ├── fig4_comparativa_filtros_clahe.png
            ├── fig5_outlines_etiquetadas.png
            └── fig6_distribucion_metrologica.png
```

---

## 🔬 Síntesis del Pipeline de Procesamiento (5 Etapas)

1. **Etapa 1: Ingesta, Espacio de Intensidad y Diagnóstico de Histograma**
   - Aislamiento del Canal Verde ($G$) por máxima absorción óptica de la hemoglobina ($\lambda \approx 540\text{--}575\text{ nm}$).
   - Delimitación del campo visual útil retiniano ($A_{\text{FOV}} = 311\,605\text{ px}^2$).
   - Diagnóstico fotométrico: histograma unimodal asimétrico ($\mu = 53.4$, $\sigma = 26.3$), rango dinámico comprimido en sombras y gradiente esférico por viñeteado.

2. **Etapa 2: Preprocesamiento y Filtrado Espacial**
   - Filtro no lineal de **Mediana ($3\times 3$)**: atenuación de ruido térmico con preservación de aristas vivas de microcapilares finos (evitando la degradación del filtro Gaussiano).
   - **CLAHE (Contrast Limited Adaptive Histogram Equalization)**: ecualización local contextual (rejilla $8\times 8$, *clip limit* $2.5$) para compensar la iluminación heterogénea.
   - Sustracción de fondo morfológica para aplanar el gradiente esférico.

3. **Etapa 3: Segmentación y Binarización**
   - Umbralización global automática de **Otsu** ($T^* = 42.0$) por maximización de varianza inter-clase.
   - Polaridad con **Dark Background** (Vasos sanguíneos $= 255$ blanco, Fondo $= 0$ negro).

4. **Etapa 4: Acondicionamiento Morfológico Binario y Separación**
   - **Apertura morfológica (disco $r=1\text{ px}$)**: supresión de espículas y ruido residual.
   - **Cierre morfológico y relleno de huecos (disco $r=2\text{ px}$)**: sellado del reflejo axial del lumen vascular.
   - **Transformada de Watershed**: desacople topológico de bifurcaciones y cruces agrupados.

5. **Etapa 5: Análisis de Componentes Conectados (CCA) y Extracción Metrológica**
   - Exclusión de objetos perimetrales truncados (`Exclude on edges`) y filtrado por área mínima ($A \ge 20\text{ px}^2$).
   - Generación del mapa de contornos numerados (*outlines*) y exportación a `data/results_metrologia_retina.csv`.

---

## 📊 Cuadro Resumen de Metrología Cuantitativa

| Descriptor Métrico | Valor Medido |
| :--- | :---: |
| **Área Útil Fondo de Ojo (FOV)** | $311\,605\text{ px}^2$ |
| **Recuento de Componentes Válidos ($N$)** | **38 segmentos** |
| **Umbral de Otsu Calculado ($T^*$)** | **42.00** |
| **Área Vascular Total Segmentada** | $101\,901.00\text{ px}^2$ |
| **Área Media por Componente ($\mu_A$)** | $2\,681.61\text{ px}^2$ |
| **Mediana de Área** | $78.00\text{ px}^2$ |
| **Área Mínima** | $22.00\text{ px}^2$ |
| **Área Máxima (Tronco Principal)** | $96\,280.00\text{ px}^2$ |
| **Desviación Estándar de Área** | $15\,594.71\text{ px}^2$ |
| **Circularidad Promedio ($\mu_C$)** | **0.4399** |
| **Circularidad Mediana** | **0.3287** |
| **Porcentaje de Ocupación Superficial** | **32.70\%** |

---

## 🚀 Cómo Replicar la Solución

### Opción A: Reproducción No-Code en Fiji / ImageJ (GUI)
Seguir detalladamente la guía ilustrada con menús y atajos en inglés en [`docs/protocolo_fiji_imagej.md`](docs/protocolo_fiji_imagej.md).

### Opción B: Reproducción Automatizada en Python
```bash
# 1. Crear entorno e instalar dependencias
uv venv .venv
source .venv/bin/activate
uv pip install -r src/requirements.txt

# 2. Ejecutar el pipeline completo
python src/pipeline_retina.py

# 3. Compilar el informe en LaTeX a PDF (5 páginas)
cd docs/informe_latex
pdflatex -interaction=nonstopmode TP_Integrador_VA_Retina.tex
pdflatex -interaction=nonstopmode TP_Integrador_VA_Retina.tex
```

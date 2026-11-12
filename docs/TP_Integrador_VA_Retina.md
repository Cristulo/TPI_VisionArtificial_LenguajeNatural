# Trabajo Práctico Integrador: Visión Artificial (Ciclo 2026)

**Carrera:** Licenciatura en Inteligencia Artificial  
**Materia:** 2026-1IA1(1) Visión Artificial y Lenguaje Natural  
**Caso Seleccionado:** Img 3 – Retinografía Vascular Digital (Recurso: `Retina` / `3.png`)  
**Herramienta Utilizada:** Fiji / ImageJ (Interfaz Gráfica No-Code)

---

## 1. Carátula y Datos Institucionales

- **Título del Trabajo:** Pipeline de Procesamiento y Metrología en Retinografía Vascular Digital
- **Imagen Seleccionada:** Caso 3 – Retinografía Vascular Digital (`3.png`, resolución $1024 \times 680$ píxeles)
- **Integrantes del Grupo:**
  - **Bringas, Mateo Lautaro** — Legajo: 435719 — `435719@tecnologia.edu.ar`
  - **Castro, Cristian Leonel** — Legajo: 435837 — `435837@tecnologia.edu.ar`
  - **Garcia Pintos, Valentin** — Legajo: 435804 — `435804@tecnologia.edu.ar`

---

## 2. Diagnóstico Fotométrico y de Adquisición

Para comenzar el trabajo en Fiji/ImageJ, abrimos la imagen `3.png` ($1024 \times 680$ píxeles). Al tratarse de una imagen a color (RGB) de fondo de ojo, el primer paso antes de pasar a 8 bits fue evaluar los canales por separado mediante `Image > Color > Split Channels`.

Observamos que el canal Rojo está muy saturado (los vasos casi no se distinguen del tejido) y el canal Azul es demasiado oscuro y ruidoso. En cambio, el **Canal Verde (G)** muestra el mejor contraste porque la sangre absorbe mucha luz en esa longitud de onda, haciendo que las venas y arterias se vean bien oscuras respecto al fondo de la retina. Por eso nos quedamos con el canal verde como imagen monocromática de 8 bits (valores discretos en $[0, 255]$).

*(Insertar aquí Figura 1: `docs/informe_latex/figuras/fig1_diagnostico_histograma.png`)*

### Interpretación del Histograma y Rango Dinámico
- **Distribución:** Si miramos toda la imagen completa, el histograma parecería bimodal por el recuadro negro que rodea al ojo. Pero analizando únicamente el círculo útil de la retina (*Field of View* de $311,605\text{ px}^2$), la distribución es **unimodal asimétrica**, con una media de $53.4$ y desvío estándar de $26.3$.
- **Exposición y Rango Dinámico:** El rango dinámico está **comprimido hacia las sombras y tonos medios** (el $90\%$ de los píxeles de la retina cae entre los niveles $19$ y $94$). Además, se nota un fuerte gradiente de iluminación esférico (viñeteado): el centro y la zona del disco óptico están mucho más iluminados que los bordes periféricos.
- **Tipología de Ruido:** No se observan píxeles blancos o negros aislados extremos, por lo que descartamos ruido impulsivo (*Sal y Pimienta*). El ruido presente es de tipo **Gaussiano / térmico de sensor**, propio de la cámara en zonas de baja iluminación, que se percibe como una textura granulada suave sobre el fondo del tejido.

---

## 3. Diagrama de Flujo del Pipeline

`[Etapa 1: Ingesta e Histograma]` → `[Etapa 2: Preprocesamiento]` → `[Etapa 3: Segmentación]` → `[Etapa 4: Morfología]` → `[Etapa 5: Extracción Metrológica]`

*(Insertar aquí Figura 2: `docs/informe_latex/figuras/fig2_flujograma_pipeline.png`)*

| Etapa | Operación | Ruta en Fiji / ImageJ | Parámetros Exactos |
| :--- | :--- | :--- | :--- |
| **1. Ingesta** | Canal Verde 8-bit | `Image > Color > Split Channels` | Selección canal G ($[0, 255]$) |
| | Histograma | `Analyze > Histogram` | 256 bins (Región FOV) |
| **2. Preproceso** | Filtro Espacial | `Process > Filters > Median...` | Radio $= 1.5\text{ px}$ (Kernel $3\times 3$) |
| | Realce Local (CLAHE) | `Process > Enhance Local Contrast` | Blocksize=63, Bins=256, Slope=2.5 |
| | Sustracción de Fondo | `Process > Subtract Background` | Rolling ball radius $= 30\text{ px}$ |
| **3. Segmentación** | Umbralización | `Image > Adjust > Threshold` | Método: **Otsu** ($T = 42$), *Dark background* |
| **4. Morfología** | Apertura Binaria | `Process > Binary > Open` | Elemento estructurante $3\times 3$ (disco $r=1$) |
| | Cierre y Relleno | `Process > Binary > Close / Fill Holes` | Sella huecos internos del vaso ($r=2$) |
| | División de Aguas | `Process > Binary > Watershed` | Mapa de distancia euclídea (EDM) |
| **5. Metrología** | Set Measurements | `Analyze > Set Measurements` | Area, Centroid, Perimeter, Shape Descriptors |
| | Conteo y Medición | `Analyze > Analyze Particles` | Size: `20-Infinity`, *Exclude on edges* |

---

## 4. Justificación Teórica y Analítica

### 1. Filtro de Mediana ($3\times 3$) vs. Filtro Gaussiano o de Media
Probamos inicialmente un filtro Gaussiano, pero al ser un filtro lineal de promedio ponderado, difumina los bordes de las venas más finitas (capilares de 1 a 3 píxeles de grosor), haciendo que se pierdan al binarizar. En cambio, el **Filtro de Mediana** con ventana de $3\times 3$ (radio $1.5\text{ px}$) es un filtro no lineal de orden que suaviza la granulosidad del ruido térmico pero preserva los bordes nítidos (*edge-preserving*). Elegimos un kernel pequeño de $3\times 3$ porque una ventana mayor ($5\times 5$ o $7\times 7$) borraría las ramificaciones vasculares más delgadas.

*(Insertar aquí Figura 3: `docs/informe_latex/figuras/fig4_comparativa_filtros_clahe.png`)*

### 2. Ecualización Adaptativa CLAHE vs. Ecualización Global
Una ecualización global de histograma estira el contraste tomando toda la imagen por igual; como el centro de la retina es brillante y los bordes son oscuros, la ecualización global quema la zona del nervio óptico y mete mucho ruido en la periferia. Por eso aplicamos **CLAHE**, que trabaja por bloques locales y limita la pendiente máxima (*clip limit* de $2.5$). Así logramos resaltar las venas en las zonas oscuras sin saturar el centro, acompañado de una sustracción de fondo (*Rolling Ball* de $30\text{ px}$) para emparejar la iluminación general.

### 3. Umbral de Otsu vs. Umbral Manual y Polaridad
El algoritmo de **Otsu** busca automáticamente el umbral que maximiza la varianza entre dos clases (vasos y fondo), dando un valor exacto de $T = 42$. Al compararlo con un ajuste manual empírico, vimos que bajar el umbral manualmente a $T \approx 30$ permite recuperar algunos microcapilares más, pero mete muchísimo ruido de fondo que ensucia las mediciones; subirlo a $T > 55$ corta las arterias principales en pedazos. Por lo tanto, el umbral de Otsu ($T = 42$) resultó el punto de equilibrio más objetivo y reproducible. Se activó *Dark background* sobre el mapa de vasos realzado para que los vasos queden blancos ($255$) y el fondo negro ($0$).

### 4. Operaciones Morfológicas y Watershed
- **Apertura (*Open*):** Aplica erosión seguida de dilatación. Nos sirvió para borrar pequeños puntitos blancos aislados y espículas en los bordes que quedaron tras binarizar.
- **Cierre (*Close*) y Relleno (*Fill Holes*):** Las arterias suelen tener un brillo central que al binarizar deja huecos alargados adentro del vaso. El cierre y relleno sellan esos poros internos para que el vaso sea compacto.
- **Watershed:** En una red vascular todas las ramas se tocan o cruzan. Al aplicar *Watershed*, Fiji calcula el mapa de distancia al borde y corta los estrechamientos y cruces, separando el árbol vascular en segmentos medibles por separado sin caer en una sobre-segmentación excesiva.

---

## 5. Memoria Gráfica de Transformación

Galería comparativa con la imagen en cada hito del proceso (`Original` → `Filtrada + CLAHE` → `Binarizada Otsu` → `Morfológica` → `Watershed` → `Contornos numerados`):

*(Insertar aquí Figura 4: `docs/informe_latex/figuras/fig3_memoria_grafica_etapas.png`)*

---

## 6. Cuadro Estadístico y Metrología

Para la Etapa 5 configuramos `Analyze Particles` filtrando el ruido residual menor a $20\text{ px}^2$ y marcando *Exclude on edges* para descartar los segmentos que tocan los bordes de corte. Los resultados exportados en el archivo CSV se resumen en la siguiente tabla:

| Métrica / Descriptor Metrológico | Valor Obtenido |
| :--- | :---: |
| **Recuento total de objetos válidos ($N$)** | **38 segmentos vasculares** |
| **Área útil del fondo de ojo (FOV de referencia)** | $311,605\text{ px}^2$ |
| **Área total ocupada por vasos sanguíneos** | $101,901.00\text{ px}^2$ |
| **Área media por objeto ($\mu_A$)** | $2,681.61\text{ px}^2$ (Mediana: $78.00\text{ px}^2$) |
| **Área mínima registrada** | $22.00\text{ px}^2$ |
| **Área máxima registrada (tronco vascular principal)** | $96,280.00\text{ px}^2$ |
| **Desviación estándar del área ($\sigma_A$)** | $15,594.71\text{ px}^2$ |
| **Circularidad promedio ($C = 4\pi \cdot \text{Área} / \text{Perímetro}^2$)** | **0.4399** (Mediana: **0.3287**) |
| **Porcentaje de ocupación superficial vascular** | **32.70%** |

### Análisis de los resultados numéricos
Llama la atención que la **circularidad promedio sea baja ($0.4399$ y mediana de $0.3287$)**. Esto tiene total sentido físico y anatómico: a diferencia de monedas o células redondas (donde $C$ ronda $0.85$ a $1.0$), los vasos sanguíneos son estructuras tubulares largas, finas y ramificadas, lo que hace que tengan muchísimo perímetro en relación a su área. Asimismo, la gran diferencia entre el área media ($2,681\text{ px}^2$) y la mediana ($78\text{ px}^2$) se debe a que el árbol vascular principal mantiene una estructura grande conectada mientras que las ramificaciones periféricas desacopladas por Watershed son segmentos más cortos.

---

## 7. Auditoría de Errores y Conclusiones

### Auditoría crítica de errores observados
1. **Casos de Sub-segmentación (pérdida de capilares finos):** En la zona izquierda e inferior de la retina (donde la iluminación original era más débil), los capilares más finitos tienen un contraste muy bajo. Al aplicar un único umbral global de Otsu ($T=42$) y luego una apertura morfológica, varios de estos microvasos delgados quedan desconectados o por debajo del corte de $20\text{ px}^2$.
2. **Casos de Sobre-segmentación y artefactos:** En la zona brillante del disco óptico (derecha) y en algunas bifurcaciones anchas, el algoritmo de *Watershed* (pensado originalmente para objetos convexos o circulares como células) genera cortes transversales artificiales sobre venas que en realidad son un mismo conducto continuo.

### Propuestas de optimización
- **Umbralización Local Adaptativa (Phansalkar o Bernsen):** En lugar de usar Otsu global, usar `Image > Adjust > Auto Local Threshold` en Fiji permitiría adaptarse mejor a los microvasos en regiones oscuras sin engrosar las venas del centro.
- **Filtros Tubulares (Frangi Vesselness / Tubeness):** Fiji incluye el plugin `Plugins > Analyze > Tubeness`, que detecta específicamente formas cilíndricas o lineales antes de binarizar, evitando que se corten los capilares finos y reemplazando el uso de Watershed por un análisis de esqueleto (`Skeletonize`).

### Conclusión
El pipeline desarrollado en 5 etapas permitió acondicionar con éxito una imagen médica compleja con iluminación despareja y bajo contraste local. La combinación del canal verde, el filtro de Mediana ($3\times 3$) y el realce CLAHE fue clave para que la segmentación de Otsu y la morfología binaria lograran aislar la red vascular, determinando una ocupación superficial del $32.70\%$ y verificando cuantitativamente su geometría alargada mediante el descriptor de circularidad.

# Protocolo Paso a Paso para Fiji / ImageJ (Régimen No-Code GUI)

**Materia:** 2026-1IA1(1) Visión Artificial y Lenguaje Natural (Ciclo 2026)  
**Proyecto:** Trabajo Práctico Integrador (TPI) - Visión Artificial  
**Caso de Estudio:** Img 3 - Retinografía Vascular Digital (`3.png`)  
**Autores:**
- Bringas, Mateo Lautaro (Legajo: 435719)
- Castro, Cristian Leonel (Legajo: 435837)
- Garcia Pintos, Valentin (Legajo: 435804)

---

## 1. Herramientas Recomendadas
- **Fiji Desktop (Recomendada):** Versión completa de ImageJ para Windows, macOS o Linux con plugins preinstalados. Descarga en `fiji.sc`.
- **ImageJ.js (Web):** Ejecutable sin instalación desde cualquier navegador web en `https://ij.imjoy.io/`.

> **Nota de idioma:** Las interfaces gráficas de Fiji e ImageJ están íntegramente en inglés. En este protocolo se indican las rutas exactas de menú en inglés junto con sus atajos de teclado oficiales.

---

## 2. Ejecución Paso a Paso por Etapas

### Etapa 1: Ingesta, Espacio de Intensidad y Diagnóstico de Histograma
1. **Abrir la imagen:**
   - Menú: `File > Open...` (`Ctrl + O`).
   - Seleccionar el archivo `data/images/3.png`.
2. **Descomposición espectral y aislamiento del Canal Verde ($G$):**
   - Menú: `Image > Color > Split Channels`.
   - Se abrirán 3 ventanas individuales: `3.png (red)`, `3.png (green)` y `3.png (blue)`.
   - Cerrar las ventanas roja y azul. Conservar únicamente `3.png (green)` debido a que la hemoglobina absorbe máximamente en $\approx 540\text{--}575\text{ nm}$ (máximo contraste de la red vascular).
   - Verificar que esté en escala de grises de 8 bits (`Image > Type > 8-bit`).
3. **Diagnóstico del Histograma:**
   - Menú: `Analyze > Histogram` (`Ctrl + H`).
   - **Diagnóstico observable:**
     - Distribución unimodal asimétrica con sesgo hacia tonos oscuros y medios ($\mu \approx 53.4$, $\sigma \approx 26.3$).
     - Rango dinámico comprimido en sombras (pérdida de reflectancia en el parénquima de fondo).
     - Ruido gaussiano aditivo y térmico de sensor en baja iluminación.
     - Gradiente esférico de iluminación (viñeteado óptico del retinógrafo).

---

### Etapa 2: Preprocesamiento y Filtrado Espacial
1. **Filtrado no lineal para reducción de ruido térmico:**
   - Menú: `Process > Filters > Median...`
   - Configuración de Radio: `Radius: 1.5` o `2.0 pixels`.
   - Clic en `OK`.
   - *Justificación:* A diferencia del filtro Gaussiano (`Process > Filters > Gaussian Blur...`), el filtro de mediana preserva los bordes filiformes de microcapilares finos sin difuminarlos con el tejido de fondo.
2. **Compensación de Iluminación Heterogénea mediante CLAHE:**
   - Menú: `Process > Enhance Local Contrast (CLAHE)`
   - Configuración de parámetros:
     - `Blocksize: 63` (o `127`)
     - `Histogram bins: 256`
     - `Maximum slope: 2.5`
     - `Fast: Yes`
   - Clic en `OK`.
   - *Justificación:* Ecualiza el histograma localmente en teselas contiguas con limitación de contraste (*clip limit*), haciendo visibles los vasos periféricos sin sobre-amplificar el ruido en zonas homogéneas.
3. **Sustracción de Fondo Morfológica:**
   - Menú: `Process > Subtract Background...`
   - Parámetros:
     - `Rolling ball radius: 30.0 pixels`
     - `Light background: Desmarcado` (fondo oscuro)
     - `Sliding paraboloid: Marcado`
   - Clic en `OK`.

---

### Etapa 3: Segmentación y Binarización
1. **Configuración de Opciones Binarias:**
   - Menú: `Process > Binary > Options...`
   - Marcar `Black background` (fondo negro 0, objetos blancos 255).
   - `Iterations: 1`, `Count: 1`, `EDM output: Overwrite`.
   - Clic en `OK`.
2. **Umbralización Automática de Otsu:**
   - Menú: `Image > Adjust > Threshold...` (`Ctrl + Shift + T`).
   - En el selector desplegable izquierdo, elegir el método **`Otsu`**.
   - En el desplegable derecho, seleccionar **`Red`** o **`B&W`**.
   - Asegurarse de que esté marcada la casilla **`Dark background`**.
   - Notar que el umbral calculado automáticamente es $T \approx 42$.
   - Presionar el botón **`Apply`**.
   - Ahora los vasos sanguíneos aparecen como estructuras blancas ($255$) sobre fondo negro ($0$).

---

### Etapa 4: Acondicionamiento Morfológico Binario y Separación
1. **Apertura Morfológica (Erosión seguida de Dilatación):**
   - Menú: `Process > Binary > Open`.
   - *Propósito:* Elimina pequeñas espículas y falsos positivos de ruido granular ($< 2\text{ px}$).
2. **Cierre Morfológico y Relleno de Huecos:**
   - Menú: `Process > Binary > Close`.
   - Menú: `Process > Binary > Fill Holes`.
   - *Propósito:* Sella el reflejo axial de luz (*arteriolar light reflex*) dentro del lumen de los vasos sanguíneos, evitando que queden huecos longitudinales artificiales.
3. **Desacople de Ramificaciones mediante Watershed:**
   - Menú: `Process > Binary > Watershed`.
   - *Propósito:* Calcula el mapa de distancia euclídea e inserta líneas divisorias de fondo ($0$) que desacoplan bifurcaciones y cruces agrupados en componentes independientes.

---

### Etapa 5: Análisis de Componentes Conectados (CCA) y Extracción Metrológica
1. **Configuración de Parámetros de Medición:**
   - Menú: `Analyze > Set Measurements...`
   - Marcar obligatoriamente las siguientes casillas:
     - `Area`
     - `Standard deviation`
     - `Min & max gray value`
     - `Centroid`
     - `Perimeter`
     - `Bounding rectangle`
     - `Shape descriptors` (incluye Circularity)
     - `Display label`
   - Clic en `OK`.
2. **Ejecución del Análisis de Partículas:**
   - Menú: `Analyze > Analyze Particles...`
   - Configuración:
     - `Size (pixel^2): 20-Infinity` (excluye ruido granular residual).
     - `Circularity: 0.00-1.00`.
     - `Show: Outlines` (genera la ventana con los contornos numerados de cada componente).
     - `Display results: Marcado`.
     - `Clear results: Marcado`.
     - `Summarize: Marcado`.
     - `Exclude on edges: Marcado` (evita distorsiones con vasos truncados en el borde).
     - `Include holes: Desmarcado`.
   - Clic en `OK`.
3. **Exportación de Resultados:**
   - En la ventana emergente **`Results`**:
     - Menú: `File > Save As...` (`Ctrl + S`).
     - Guardar como `Results.csv` en la carpeta `data/`.
   - En la ventana **`Summary`**:
     - Copiar los valores globales: `Count`, `Total Area`, `Average Size`, `%Area`.
   - En la ventana **`Drawing of ...`** (Outlines):
     - Menú: `File > Save As > PNG...` para incluirla en la memoria gráfica.

---

## 3. Resumen de Atajos de Teclado Útiles en Fiji
| Atajo | Función |
| :--- | :--- |
| `Ctrl + O` | Abrir archivo de imagen |
| `Ctrl + S` | Guardar resultados / imagen |
| `Ctrl + H` | Mostrar histograma de la imagen activa |
| `Ctrl + Shift + T` | Abrir ventana de Umbralización (*Threshold*) |
| `Ctrl + Shift + M` | Abrir *Measure* (medir selección activa) |
| `Ctrl + Shift + D` | Duplicar imagen activa |

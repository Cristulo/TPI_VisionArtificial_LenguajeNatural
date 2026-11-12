# Banco de Preparación y Respuestas para el Cuestionario de Moodle

**Materia:** 2026-1IA1(1) Visión Artificial y Lenguaje Natural (Ciclo 2026)  
**Actividad:** Entregable B - Cuestionario Interactivo en Campus Virtual  
**Caso de Estudio:** Img 3 - Retinografía Vascular Digital (`3.png`)  
**Autores:** Bringas, Mateo Lautaro (435719) | Castro, Cristian Leonel (435837) | Garcia Pintos, Valentin (435804)

---

## 1. Parámetros Numéricos Clave (Tolerancia $\pm 2$)

| Parámetro / Métrica | Valor Exacto | Rango Válido ($\pm 2$) | Unidad / Formato |
| :--- | :---: | :---: | :--- |
| **Umbral de Otsu Calculado ($T^*$)** | **42** | $[40, 44]$ | Nivel de intensidad en escala $[0, 255]$ |
| **Recuento de Componentes Válidos ($N$)** | **38** | $[36, 40]$ | Componentes conexos independientes |
| **Área Total de la Retina (FOV)** | **311,605** | $\pm 2\%$ | Píxeles cuadrados ($\text{px}^2$) |
| **Área Vascular Total Segmentada** | **101,901** | $\pm 2\%$ | Píxeles cuadrados ($\text{px}^2$) |
| **Porcentaje de Ocupación Superficial** | **32.70\%** | $[31\%, 35\%]$ | Porcentaje de la superficie retiniana |
| **Circularidad Promedio ($\mu_C$)** | **0.44** (exacto 0.4399) | $[0.42, 0.46]$ | Adimensional ($[0, 1]$) |
| **Circularidad Mediana** | **0.33** (exacto 0.3287) | $[0.31, 0.35]$ | Adimensional ($[0, 1]$) |
| **Área Media por Componente ($\mu_A$)** | **2,682** | $\pm 2\%$ | Píxeles cuadrados ($\text{px}^2$) |
| **Área Mínima de Componente Válido** | **22** | $[20, 24]$ | Píxeles cuadrados ($\text{px}^2$) |
| **Radio de Kernel Filtro Mediana** | **1.5 / 3x3** | $[1, 2]$ | Píxeles de radio / Tamaño de ventana |

---

## 2. Banco de 10 Preguntas y Respuestas Justificadas

### Pregunta 1 (Numérica): Umbral de Otsu
- **Enunciado:** ¿Cuál es el valor del umbral global calculado automáticamente por el método de Otsu para segmentar los vasos en el mapa de contraste?
- **Respuesta Correcta:** `42` (Margen de tolerancia: $40$ a $44$).
- **Fundamento:** El algoritmo de Otsu busca el nivel $t$ que maximiza la varianza inter-clase $\sigma_B^2(t)$. Sobre la imagen de contraste vascular compensada, este óptimo se alcanza en $t = 42.0$.

---

### Pregunta 2 (Opción Múltiple): Aislamiento Espectral y Canales Cromáticos
- **Enunciado:** En una retinografía RGB de fondo de ojo, ¿por qué motivo se selecciona el canal Verde ($G$) en lugar del Rojo ($R$) o Azul ($B$) para el análisis vascular?
- **Respuesta Correcta:** Porque la hemoglobina de la sangre presenta su pico máximo de absorción óptica en longitudes de onda medias ($\approx 540\text{--}575\text{ nm}$), generando el mayor contraste entre los vasos sanguíneos y el parénquima de fondo.
- **Distractores:**
  - *Incorrecto (Canal R):* El canal rojo satura la reflectancia del tejido coroideo y anula el contraste de bordes.
  - *Incorrecto (Canal B):* El canal azul sufre fuerte dispersión de Rayleigh y absorción tisular, quedando severamente subexpuesto.

---

### Pregunta 3 (Emparejamiento / Conceptual): Operaciones Morfológicas
- **Enunciado:** Empareje cada operación morfológica binaria con su propósito técnico en el pipeline:
  1. **Apertura Morfológica (Erosión $\rightarrow$ Dilatación):** $\rightarrow$ *Eliminar espículas, falsos positivos diminutos y ruido impulsivo residual.*
  2. **Cierre Morfológico (Dilatación $\rightarrow$ Erosión):** $\rightarrow$ *Sellar huecos internos y discontinuidades en el lumen causadas por el reflejo axial de luz.*
  3. **Transformada de Watershed (División de Aguas):** $\rightarrow$ *Desacoplar bifurcaciones y ramas adosadas insertando líneas divisorias de fondo.*
  4. **Filtro de Área Mínima ($A \ge 20\text{ px}^2$):** $\rightarrow$ *Excluir partículas espurias y ruido granular microscópico sin significancia anatómica.*

---

### Pregunta 4 (Fórmula Matemática): Factor de Circularidad
- **Enunciado:** ¿Cuál es la fórmula matemática utilizada por ImageJ para cuantificar la circularidad de una partícula binaria?
- **Respuesta Correcta:** $C = \frac{4\pi \cdot \text{Área}}{\text{Perímetro}^2}$
- **Interpretación:** Para un círculo perfecto, $C = 1.0$. Un valor de $C \ll 0.5$ (como el $0.33\text{--}0.44$ obtenido en los vasos) indica una morfología marcadamente alargada, filiforme o ramificada.

---

### Pregunta 5 (Opción Múltiple): Elección de Filtro Espacial
- **Enunciado:** ¿Por qué se prefiere un filtro espacial de Mediana frente a un filtro de Media o Gaussiano para el preprocesamiento de microcapilares?
- **Respuesta Correcta:** Porque el filtro de mediana es un filtro no lineal de orden estadístico que suprime ruido térmico preservando las aristas vivas y la energía de bordes delgados, mientras que los filtros de media o gaussianos difuminan los vasos finos haciéndolos desaparecer durante la umbralización.

---

### Pregunta 6 (Numérica): Porcentaje de Ocupación Superficial Vascular
- **Enunciado:** Indique el porcentaje aproximado de ocupación superficial de la red vascular respecto al área total útil del fondo de ojo (FOV):
- **Respuesta Correcta:** `32.7%` (o en el rango `31% a 35%`).
- **Cálculo:** $\% = \frac{101\,901\text{ px}^2}{311\,605\text{ px}^2} \times 100 \approx 32.70\%$.

---

### Pregunta 7 (Opción Múltiple): Justificación de CLAHE
- **Enunciado:** ¿Qué ventaja crítica ofrece la ecualización adaptativa CLAHE frente a una ecualización de histograma global convencional?
- **Respuesta Correcta:** CLAHE opera sobre bloques locales contiguos y limita la pendiente de contraste (*clip limit*), evitando la sobre-amplificación del ruido en regiones de fondo homogéneas y compensando el gradiente esférico de iluminación (viñeteado).

---

### Pregunta 8 (Completamiento de Frase / Polaridad Binaria):
- **Enunciado:** En Fiji/ImageJ, al realizar la segmentación de objetos de interés sobre fondo oscuro con la opción `Dark background` activada, los píxeles de los vasos sanguíneos toman el valor numérico de **[255]** (blanco) y el parénquima de fondo toma el valor de **[0]** (negro).

---

### Pregunta 9 (Numérica / Conceptual): Rango de Circularidad en Vasos Retinianos
- **Enunciado:** ¿Por qué la circularidad promedio de los vasos retinianos ($C \approx 0.44$) es significativamente menor que la de células en citología ($C \approx 0.85$) o monedas ($C \approx 0.98$)?
- **Respuesta Correcta:** Debido a la alta relación perímetro-área inherente a estructuras biomédicas filiformes y ramificadas, donde la longitud tubular maximiza el perímetro $P$ reduciendo drásticamente el valor de $\frac{4\pi \cdot A}{P^2}$.

---

### Pregunta 10 (Opción Múltiple): Exclusión en Bordes (*Exclude on Edges*)
- **Enunciado:** ¿Qué problema estadístico previene activar la opción `Exclude on edges` durante el análisis de partículas?
- **Respuesta Correcta:** Evita el sesgo estadístico introducido por partículas o vasos truncados artificialmente por el límite del encuadre o diafragma de la cámara, los cuales presentarían mediciones espurias de área y circularidad incompleta.

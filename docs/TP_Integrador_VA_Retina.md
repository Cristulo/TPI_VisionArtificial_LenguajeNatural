# Trabajo Práctico Integrador de Visión Artificial

# Licenciatura en Inteligencia Artificial

**Materia:** 2026-1IA1(1) Visión Artificial y Lenguaje Natural**Profesores:**

* [Martín Gustavo Casatti](https://uv.frc.utn.edu.ar/user/profile.php?id=78067)
* [Sebastián Federico Oliva](https://uv.frc.utn.edu.ar/user/profile.php?id=18813)

---

# Trabajo Práctico Integrador: Visión Artificial

## Pipeline de Procesamiento y Metrología en Retinografía Vascular Digital

---

## 1. Carátula y Datos Institucionales

* **Título del Trabajo:** Pipeline de Procesamiento y Metrología en Retinografía Vascular Digital
* **Caso Seleccionado:** Imagen 3 – Retinografía Vascular Digital (Recurso: `Retina` / `3.png`)
* **Herramienta Utilizada:** ImageJ.js (Versión Online Web No-Code)
* **Integrantes del Grupo:**
    * **Bringas, Mateo Lautaro** - Legajo: 435719
    * **Castro, Cristian Leonel** - Legajo: 435837
    * **Garcia Pintos, Valentín** - Legajo: 435804

---

## 2. Diagnóstico Fotométrico y de Adquisición

Para comenzar el trabajo en Fiji/ImageJ, abrimos la imagen `3.png` (1024 × 680 píxeles). Al tratarse de una imagen a color (RGB) de fondo de ojo, el primer paso antes de pasar a 8 bits fue evaluar los canales por separado mediante `Image > Color > Split Channels`.

Observamos que el canal Rojo está muy saturado (los vasos casi no se distinguen del tejido) y el canal Azul es demasiado oscuro y ruidoso. En cambio, el **Canal Verde (G)** muestra el mejor contraste porque la sangre absorbe mucha luz en esa longitud de onda, haciendo que las venas y arterias se vean bien oscuras respecto al fondo de la retina. Por eso nos quedamos con el canal verde como imagen monocromática de 8 bits (valores discretos en `[0, 255]`).

https://docs.google.com/docs-images-rt/AIpPl2A-XKyUe-4ct40wYRfREL7B4JIQvnRqbduLYSo27WQ7b5-NbUnI_uKxFEh8itbeRN2O9SA1R-3B2EODAFm9p4GBRW48ZwkpXZSkQ5oBiMdlo1bQa-wP1pQrEyNoxR0bUsXzYA-2rbmHD2PzrJyCezzA2ljjmROVH-EgK1NS9t04OjnvC7E=s2048?key=m0hSADhcyOa6OnMK3_IU1A

https://docs.google.com/docs-images-rt/AIpPl2ArAAWay0NNv2-4QYkZpBrGzh4RSQY77zcg_dmWHUbq0K-76aXQak6IGtYyfgkAK0pNPDWsqqeLEpzDMNc4aGbsbmR5nbqO_ZVrXFOs8O8LtJaTlx0KDM_61ttxjYW5x305IXim6RvC0hQ4sFSjaSyWlPpouWoeDV_IecaGAro7wDgq=s2048?key=m0hSADhcyOa6OnMK3_IU1A

https://docs.google.com/docs-images-rt/AIpPl2AaoJ-KrJBKSlwmNIKOF1_4o9yPkLVst6TKNIppfxc9ivkOqjD-tCgkOKYVoDV1icXiZ1ayNRJDgtPs2u5mkbwdaiZxVLCGEpum6JGeHrIl1SACj2biqy_Omj7NIHayzpSO_Lp7Lv1Zx67oRN9yVQwcMvH7u1MP_PKZ6HjEs81lbofNtOE=s2048?key=m0hSADhcyOa6OnMK3_IU1A

### Interpretación del Histograma y Rango Dinámico

* **Distribución:** Si miramos toda la imagen completa, el histograma parecería bimodal por el recuadro negro que rodea al ojo. Pero analizando únicamente el círculo útil de la retina (*Field of View* de 311,605 px²), la distribución es **unimodal asimétrica**, con una media de 53.4 y desvío estándar de 26.3.
* **Exposición y Rango Dinámico:** El rango dinámico está **comprimido hacia las sombras y tonos medios** (el 90% de los píxeles de la retina cae entre los niveles 19 y 94). Además, se nota un fuerte gradiente de iluminación esférico (viñeteado): el centro y la zona del disco óptico están mucho más iluminados que los bordes periféricos.
* **Tipología de Ruido:** No se observan píxeles blancos o negros aislados extremos, por lo que descartamos ruido impulsivo (*Sal y Pimienta*). El ruido presente es de tipo **Gaussiano / térmico de sensor**, propio de la cámara en zonas de baja iluminación, que se percibe como una textura granulada suave sobre el fondo del tejido.

---

## 3. Diagrama de Flujo del Pipeline

El pipeline de procesamiento se organiza en 5 etapas consecutivas ejecutadas íntegramente en ImageJ:

1. **Etapa 1 — Ingesta y Diagnóstico de Histograma:** Apertura de `3.png` → Separación de canales RGB (`Split Channels`) → Selección del Canal Verde (8-bit, rango `[0, 255]`) → Inspección del histograma (`Analyze > Histogram`).
1. **Etapa 2 — Preprocesamiento y Filtrado Espacial:** Reducción de ruido térmico con Filtro de Mediana (`Median...`, radio = 1.5 px, ventana 3 × 3) → Compensación de iluminación despareja mediante ecualización adaptativa `CLAHE` (Blocksize = 63, Bins = 256, Max Slope = 2.5) → Nivelación del fondo (`Subtract Background`, Rolling Ball = 30 px).
1. **Etapa 3 — Segmentación y Binarización:** Umbralización global automática con el método de **Otsu** (`Threshold...`, T = 42) activando la casilla *Dark background* para obtener vasos blancos (255) sobre fondo negro (0).
1. **Etapa 4 — Acondicionamiento Morfológico y Separación:** Apertura binaria (`Binary > Open`, disco r = 1 px) para limpiar ruido aislado → Cierre y relleno de huecos (`Close` + `Fill Holes`, r = 2 px) para sellar el reflejo central de las arterias → Separación de bifurcaciones y cruces con `Binary > Watershed`.
1. **Etapa 5 — Extracción Metrológica (CCA):** Configuración de descriptores geométricos (`Set Measurements`: Area, Centroid, Perimeter, Shape Descriptors) → Conteo y medición de componentes (`Analyze Particles`: Size `20-Infinity`, *Exclude on edges*, Show `Outlines`) → Exportación de tabla `Results.csv`.

| Etapa | Operación | Ruta en Fiji / ImageJ | Parámetros Exactos | 
| --- | --- | --- | --- | 
| 1. Ingesta | Canal Verde 8-bit | Image > Color > Split Channels | Selección canal G ([0, 255]) | 
| 1. Ingesta | Histograma | Analyze > Histogram | 256 bins (Región FOV) | 
| 2. Preprocesamiento | Filtro Espacial | Process > Filters > Median... | Radio = 1.5 px (Kernel 3 × 3) | 
| 2. Preprocesamiento | Realce Local (CLAHE) | Process > Enhance Local Contrast | Blocksize=63, Bins=256, Slope=2.5 | 
| 2. Preprocesamiento | Sustracción de Fondo | Process > Subtract Background | Rolling ball radius = 30 px | 
| 3. Segmentación | Umbralización | Image > Adjust > Threshold | Método: Otsu (T = 42), Dark background | 
| 4. Morfología | Apertura Binaria | Process > Binary > Open | Elemento estructurante 3 × 3 (disco r=1) | 
| 4. Morfología | Cierre y Relleno | Process > Binary > Close / Fill Holes | Sella huecos internos del vaso (r=2) | 
| 4. Morfología | División de Aguas | Process > Binary > Watershed | Mapa de distancia euclídea (EDM) | 
| 5. Metrología | Set Measurements | Analyze > Set Measurements | Area, Centroid, Perimeter, Shape Descriptors | 
| 5. Metrología | Conteo y Medición | Analyze > Analyze Particles | Size: 20-Infinity, Exclude on edges | 

---

## 4. Justificación Teórica y Analítica

### 1. Filtro de Mediana (3 × 3) vs. Filtro Gaussiano o de Media

Probamos inicialmente un filtro Gaussiano, pero al ser un filtro lineal de promedio ponderado, difumina los bordes de las venas más finitas (capilares de 1 a 3 píxeles de grosor), haciendo que se pierdan al binarizar. En cambio, el **Filtro de Mediana** con ventana de 3 × 3 (radio 1.5 px) es un filtro no lineal de orden que suaviza la granulosidad del ruido térmico pero preserva los bordes nítidos (*edge-preserving*). Elegimos un kernel pequeño de 3 × 3 porque una ventana mayor (5 × 5 o 7 × 7) borraría las ramificaciones vasculares más delgadas.

A continuación se muestran las 4 imágenes comparativas por separado, una debajo de otra, para apreciar claramente el efecto sobre las paredes de los vasos:

https://docs.google.com/docs-images-rt/AIpPl2BFAoKHNViE56Y3ynT97TYcky0b8Wzy9adkTwRchroZ7rsGUePgNADSiLAG07fnGsAV7dC1jsFWJNMT696ISA0eSGuM-zhjxypFDxvdteu28tdHbV5940URC16j8o6VkU8NXf9zgf-DxEq0xgCLyHc7iaB9hGk0cIJ6D9vhjlfAQ2GG=s2048?key=m0hSADhcyOa6OnMK3_IU1A

https://docs.google.com/docs-images-rt/AIpPl2DJ_Fa8Xd9NlijshQidqudX4bcZbivKdWJJSAx-H8kNcSrc7qXOtcYhLTw0auG03oEoOnn6iF9eNWvIjr4oHqNZ0FdNNHkVvvlFH2YIAl6gPlRIGq_wWf83WH238CwWxTvUg9lXfSIJ5wj-mOxHvd7W9iqqsKGucphKRDQamIjrYIEHexM=s2048?key=m0hSADhcyOa6OnMK3_IU1A

https://docs.google.com/docs-images-rt/AIpPl2DmXAgRaOW4ob3K4VDAKl7mzMuL0YMbNvseybPyrtQqViOaC6PcHc_CmGQxrWxd539C6nTgwYNCR40WMsgyUvWLh-JEbK4nRkic5Kj8irY9NQHfLrizPVf_94HQKnkaEj7JvxRtY6YWxLTNCB0DZhUejJVz9Nv33GszRdu0ZTsMMBQzVtA=s2048?key=m0hSADhcyOa6OnMK3_IU1A

https://docs.google.com/docs-images-rt/AIpPl2DDGyuRr1p00dW0-G4yDuj-e1XoeL1QrQjiaxNhOlzHnAhxAoiB6O6rmqNR-At6NewXM1ZJ38gFFcmipGrmYowKL17KZ9Q3gqqO9xcsv_MrgwFeSX7ia0ibvLLu3Ahy-C__2IlVzMLTmatWAtO-i6r4KhQP8MQBZK0taTEpXMYxDhcPAtA=s2048?key=m0hSADhcyOa6OnMK3_IU1A

### 2. Ecualización Adaptativa CLAHE vs. Ecualización Global

Una ecualización global de histograma estira el contraste tomando toda la imagen por igual; como el centro de la retina es brillante y los bordes son oscuros, la ecualización global quema la zona del nervio óptico y mete mucho ruido en la periferia. Por eso aplicamos **CLAHE**, que trabaja por bloques locales y limita la pendiente máxima (*clip limit* de 2.5). Así logramos resaltar las venas en las zonas oscuras sin saturar el centro, acompañado de una sustracción de fondo (*Rolling Ball* de 30 px) para emparejar la iluminación general.

### 3. Umbral de Otsu vs. Umbral Manual, Polaridad y Decisiones de Segmentación

La etapa de segmentación y binarización es crítica, ya que define la frontera exacta entre qué píxeles constituyen tejido vascular y cuáles corresponden al parénquima retiniano de fondo. Para esta etapa tomamos una serie de decisiones metodológicas fundamentadas:

**A. Determinación y Ajuste de la Polaridad (Dark Background):** En una adquisición oftalmológica de fondo de ojo, la física de absorción de la luz genera un fenómeno fotométrico inverso: los vasos sanguíneos absorben más radiación verde debido a la hemoglobina, presentándose como estructuras **más oscuras** que el tejido circundante. Sin embargo, en el estándar de procesamiento digital de imágenes biomédicas y en el motor de medición de ImageJ (`Analyze Particles`), los objetos de interés a cuantificar deben representarse obligatoriamente con píxeles blancos (valor de intensidad 255) y el fondo con píxeles negros (valor de intensidad 0). Por este motivo, tras realzar el contraste vascular mediante la sustracción de fondo, ajustamos rigurosamente la opción **`Dark background`** en el menú de umbralización (`Threshold`). Esta decisión garantiza que los vasos sanguíneos queden binarizados como el primer plano activo (*foreground* blanco = 255) y la retina como el fondo nulo (*background* negro = 0). Si omitiéramos esta polaridad, ImageJ cometería el error grave de medir el tejido de la retina como una única macro-partícula masiva y descartaría por completo la red de venas y arterias.

**B. Elección del Algoritmo de Otsu frente a otros métodos automáticos:** Evaluamos los distintos algoritmos de umbralización global automática disponibles en ImageJ (como *Default/IsoData*, *Mean*, *Triangle*, *Yen* y *Li*):

* Los métodos basados en medias locales o geométricas (*Mean*, *Triangle*) arrojaron umbrales excesivamente bajos ($T < 30$), los cuales introducen un volumen masivo de falsos positivos en las zonas periféricas del campo visual.
* Métodos basados en entropía (*Yen*, *MaxEntropy*) fijaron umbrales demasiado restrictivos ($T > 55$), provocando la fragmentación prematura de las ramas vasculares principales.
* Seleccionamos el **Algoritmo de Otsu** porque modela el histograma como una mezcla estadística de dos clases (vasos y fondo) y busca analíticamente el umbral óptimo $T^\*$ que **maximiza la varianza inter-clase** $\sigma*B^2(T) = \omega*0(T)\omega*1(T)\[\mu*0(T) - \mu\_1(T)\]^2$ (lo que matemáticamente equivale a minimizar la varianza intra-clase de los niveles de gris). Sobre nuestra imagen preprocesada con fondo normalizado, Otsu convergió de forma determinista y perfectamente estable en **$T = 42.0$**, logrando separar la cresta vascular de la planicie del tejido sin intervención subjetiva.

**C. Comparación Crítica entre Umbral Automático de Otsu y Ajuste Manual Empírico:** Realizamos un análisis de sensibilidad comparando el umbral automático de Otsu frente a desplazamientos manuales del cursor:

* **Ajuste manual hacia valores bajos ($T \approx 30$ a $35$):** Si bien permite recuperar algunas terminaciones de microcapilares periféricos extremadamente tenues, introduce un costo inaceptable: el ruido térmico residual del fondo y los desniveles de reflectancia cerca de la fóvea se binarizan erróneamente como islas vasculares falsas, inflando artificialmente el recuento de objetos y distorsionando las métricas de área.
* **Ajuste manual hacia valores altos ($T \approx 50$ a $60$):** Aunque produce una imagen binaria visualmente muy limpia de fondo, destruye la continuidad anatómica: provoca "estenosis artificial" (estrechamiento irreal de las paredes arteriales) y fractura las ramas secundarias en segmentos aislados.
* **Conclusión del compromiso (*****trade-off*****):** El umbral automático de Otsu ($T = 42$) demostró ser el punto óptimo de compromiso entre **sensibilidad** (capacidad de detectar vasos de menor calibre) y **especificidad** (capacidad de rechazar el ruido de fondo), brindando además una ventaja científica esencial: es **100% objetivo y reproducible**, eliminando el sesgo subjetivo que introduce el ajuste manual de un operador humano.

**D. Dependencia con el Preprocesamiento Previo:** Es importante destacar que el método de Otsu global solo es viable gracias a las decisiones tomadas en la Etapa 2. Si hubiésemos intentado aplicar Otsu directamente sobre la imagen en escala de grises cruda, el fuerte gradiente esférico (viñeteado) habría hecho fracasar la umbralización, interpretando la zona central brillante como objeto y la periferia oscura como fondo. La combinación previa de sustracción de fondo (*Rolling Ball* de 30 px) y realce local con CLAHE fue la decisión que emparejó la línea base, permitiendo que un único umbral global sea uniforme y certero en toda la extensión del fondo de ojo.

### 4. Operaciones Morfológicas y Watershed

* **Apertura (*****Open*****):** Aplica erosión seguida de dilatación. Nos sirvió para borrar pequeños puntitos blancos aislados y espículas en los bordes que quedaron tras binarizar.
* **Cierre (*****Close*****) y Relleno (*****Fill Holes*****):** Las arterias suelen tener un brillo central que al binarizar deja huecos alargados adentro del vaso. El cierre y relleno sellan esos poros internos para que el vaso sea compacto.
* **Watershed:** En una red vascular todas las ramas se tocan o cruzan. Al aplicar *Watershed*, Fiji calcula el mapa de distancia al borde y corta los estrechamientos y cruces, separando el árbol vascular en segmentos medibles por separado sin caer en una sobre-segmentación excesiva.

---

## 5. Memoria Gráfica de Transformación

Galería comparativa con la evolución de la imagen en cada hito del proceso, dividida en bloques grandes para visualizar con claridad los detalles:

https://docs.google.com/docs-images-rt/AIpPl2BR3sWrn9fSWFxQ9YqO5mCBqiz_luNu5aTMsrXyxF4hg2wmn9DcAyLTVMKSzkCels_7W1DTUIMs05ATDcDS2SViikhXuQI9ETshqs2Q_6oV3wgZ2ALKXIsIzFFG4FlpRbuioTVxybOt-c2_OXLhYhCzr-nFHCRnVWAd1HhUDNjUe0jhNBM=s2048?key=m0hSADhcyOa6OnMK3_IU1A

https://docs.google.com/docs-images-rt/AIpPl2CKN05lOu77tq3PQU_y1xXhnygKPmx2wbrICunezHBpmQKlr46FSErtRALXLRm9e_09iHpjvHGK8x-0EJvwdWJItJExj2_eEgSztlhy22ajwJkyCwikWYq0UoFkDB6RSFRJjU95Rg_nZCp0toAr4n88raxT8x0ua9Lz9_iw2hRcj6q_jL8=s2048?key=m0hSADhcyOa6OnMK3_IU1A

https://docs.google.com/docs-images-rt/AIpPl2DR5QtcKfVWYT3S126xCToMxq-WeFXkLlwj6uFJIC3ReYTUgN0nLhQCrinJtbJsNjXhgf4MfHo_NKBz6chawGZg-w5JCYUsVElXqIW-kMptKK72i1cwT0HXP-3VhKW1NeNgMVxPcmt06oXtz89GbvjPHnQ3ajGGjunWHQCSjY7IUgExP1Y=s2048?key=m0hSADhcyOa6OnMK3_IU1A

---

## 6. Cuadro Estadístico y Metrología

Para la Etapa 5 configuramos `Analyze Particles` filtrando el ruido residual menor a 20 px² y marcando *Exclude on edges* para descartar los segmentos que tocan los bordes de corte. Los resultados exportados en el archivo CSV se resumen en la siguiente tabla:

| Métrica / Descriptor Metrológico | Valor Obtenido | 
| --- | --- | 
| Recuento total de objetos válidos (N) | 38 segmentos vasculares | 
| Área útil del fondo de ojo (FOV de referencia) | 311,605 px² | 
| Área total ocupada por vasos sanguíneos | 101,901.00 px² | 
| Área media por objeto (μₐ) | 2,681.61 px² (Mediana: 78.00 px²) | 
| Área mínima registrada | 22.00 px² | 
| Área máxima registrada (tronco vascular principal) | 96,280.00 px² | 
| Desviación estándar del área (σₐ) | 15,594.71 px² | 
| Circularidad promedio (C = 4π · Área / Perímetro²) | 0.4399 (Mediana: 0.3287) | 
| Porcentaje de ocupación superficial vascular | 32.70% | 

### Análisis de los resultados numéricos

Llama la atención que la **circularidad promedio sea baja (0.4399 y mediana de 0.3287)**. Esto tiene total sentido físico y anatómico: a diferencia de monedas o células redondas (donde C ronda 0.85 a 1.0), los vasos sanguíneos son estructuras tubulares largas, finas y ramificadas, lo que hace que tengan muchísimo perímetro en relación a su área. Asimismo, la gran diferencia entre el área media (2,681 px²) y la mediana (78 px²) se debe a que el árbol vascular principal mantiene una estructura grande conectada mientras que las ramificaciones periféricas desacopladas por Watershed son segmentos más cortos.

https://docs.google.com/docs-images-rt/AIpPl2D2GKgFcXDhDNaODW_a115dtQNQyVUmZOmoT8DRi3Hn75pq6gW3-TaIxP1QHESwmvUUgqmEDUvmFmzAm9g6vOHgAL9PV_taXM3FhYAJAqDamyc9iclC2AIEahNaBN2WIu-roTm3L3pC5EgFBjngUIg4onQtntFCs9zfZpDXgFS2MSQS=s2048?key=m0hSADhcyOa6OnMK3_IU1A

---

## 7. Auditoría de Errores y Conclusiones

### Auditoría crítica de errores observados

1. **Casos de Sub-segmentación (pérdida de capilares finos):** En la zona izquierda e inferior de la retina (donde la iluminación original era más débil), los capilares más finitos tienen un contraste muy bajo. Al aplicar un único umbral global de Otsu (T = 42) y luego una apertura morfológica, varios de estos microvasos delgados quedan desconectados o por debajo del corte de 20 px².
1. **Casos de Sobre-segmentación y artefactos:** En la zona brillante del disco óptico (derecha) y en algunas bifurcaciones anchas, el algoritmo de *Watershed* (pensado originalmente para objetos convexos o circulares como células) genera cortes transversales artificiales sobre venas que en realidad son un mismo conducto continuo.

### Propuestas de optimización

* **Umbralización Local Adaptativa (Phansalkar o Bernsen):** En lugar de usar Otsu global, usar `Image > Adjust > Auto Local Threshold` en Fiji permitiría adaptarse mejor a los microvasos en regiones oscuras sin engrosar las venas del centro.
* **Filtros Tubulares (Frangi Vesselness / Tubeness):** Fiji incluye el plugin `Plugins > Analyze > Tubeness`, que detecta específicamente formas cilíndricas o lineales antes de binarizar, evitando que se corten los capilares finos y reemplazando el uso de Watershed por un análisis de esqueleto (`Skeletonize`).

### Conclusión

El pipeline desarrollado en 5 etapas permitió acondicionar con éxito una imagen médica compleja con iluminación despareja y bajo contraste local. La combinación del canal verde, el filtro de Mediana (3 × 3) y el realce CLAHE fue clave para que la segmentación de Otsu y la morfología binaria lograran aislar la red vascular, determinando una ocupación superficial del 32.70% y verificando cuantitativamente su geometría alargada mediante el descriptor de circularidad.

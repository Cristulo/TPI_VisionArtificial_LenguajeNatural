# Trabajo Práctico Integrador: Visión Artificial (Ciclo 2026)

**Carrera:** Licenciatura en IA  
**Materia:** 2026-1IA1(1) Visión Artificial y Lenguaje Natural  
**Documento:** Enunciado Oficial, Pautas Metodológicas y Guía de Ejecución  

- **Modalidad:** Grupal (hasta 3 integrantes)
- **Régimen:** Sin código (No-Code GUI)
- **Plazo:** 14 días corridos (2 semanas)
- **Plataforma:** Campus Virtual Moodle

---

## 1. Fundamentación y Propósito Formativo

El procesamiento digital de imágenes y la visión artificial clásica constituyen el cimiento operativo sobre el cual se construyen los sistemas contemporáneos de percepción inteligente. En el ámbito profesional e industrial, la formulación de una solución no comienza con el entrenamiento ciego de modelos profundos, sino con el diagnóstico riguroso de las condiciones de adquisición, el acondicionamiento fotométrico de las señales visuales y la selección fundamentada de técnicas de segmentación y metrología morfológica.

Este Trabajo Práctico Integrador tiene como propósito evaluar la destreza analítica, el criterio ingenieril y la capacidad técnica de los estudiantes para concebir, ejecutar y auditar un pipeline completo de procesamiento digital de imágenes. Se evalúa la toma de decisiones basada en evidencia:

- Justificar la elección de cada filtro espacial frente al tipo de ruido observado en la imagen.
- Determinar el método de umbralización óptimo según la naturaleza del histograma de niveles de gris.
- Aplicar operaciones morfológicas y algoritmos de división de aguas (*Watershed*) para aislar y desacoplar estructuras adosadas.
- Extraer métricas geométricas cuantitativas (área, perímetro, centroide, circularidad) para clasificar o inspeccionar elementos del mundo real.

---

## 2. Banco de Imágenes de Prueba

Cada equipo de trabajo deberá seleccionar **una (1)** de las siguientes 5 imágenes públicas para desarrollar la totalidad de su pipeline. Todas las imágenes representan escenarios reales abordados a lo largo del cursado:

| ID | Denominación del Caso | Dominio de Aplicación | Desafíos Técnicos Principales | Recurso en Moodle |
| :--- | :--- | :--- | :--- | :--- |
| **Img 1** | **Inspección Metrológica de Monedas** | Metrología e Inspección Industrial | Gradiente de iluminación lateral, contraste bimodal, análisis de circularidad y conteo exacto de piezas metálicas. | `Monedas` |
| **Img 2** | **Citología Médica y Recuento Celular** | Biomedicina y Diagnóstico Clínico | Ruido térmico de sensor, solapamiento de membranas celulares y separación de núcleos adosados mediante *Watershed*. | `Células` |
| **Img 3** | **Retinografía Vascular Digital** | Oftalmología y Diagnóstico por Imágenes | Estructuras vasculares de bajo contraste local, iluminación heterogénea en fondo de ojo y realce adaptativo CLAHE. | `Retina` |
| **Img 4** | **Inspección de Circuitos Impresos (PCB)** | Industria Electrónica y Control de Calidad | Detección de pistas, soldaduras, discontinuidades de bordes y filtrado selectivo con preservación de aristas vivas. | `Circuito` |
| **Img 5** | **Granulometría y Análisis de Partículas** | Minería, Geología y Ciencia de Materiales | Distribución heterogénea de partículas minerales, porosidad interna, rugosidad superficial y filtrado morfológico de área. | `Piedras` |

---

## 3. Ecosistema de Herramientas de Uso Libre Permitidas

Para garantizar la equidad pedagógica y permitir que todos los estudiantes demuestren su solvencia conceptual con independencia de su nivel previo en programación, el trabajo se resolverá íntegramente mediante software libre de interfaz gráfica:

1. **Fiji / ImageJ (Desktop - Recomendada):** Paquete open-source de referencia científica internacional. Portable para Windows, macOS y Linux. Incluye de forma nativa todos los algoritmos requeridos.
2. **ImageJ.js (Web / Cloud - Recomendada para trabajo sin instalación):** Versión oficial ejecutable en cualquier navegador web moderno (`ij.imjoy.io`) con soporte WebAssembly. No requiere instalación ni privilegios de administrador.
3. **Herramientas complementarias opcionales:**
   - **CellProfiler** (`cellprofiler.org`): Especializada en análisis cuantitativo celular y flujos de trabajo biológicos automatizados.
   - **Icy** (`icy.bioimageanalysis.org`): Plataforma comunitaria de análisis y procesamiento avanzado de bioimagen.
   - **Orange Data Mining** (`orangedatamining.com`): Entorno visual no-code con módulo *Image Analytics*, apto para etapas exploratorias y agrupamiento visual sobre descriptores.

> **Material de Consulta y Descarga en Moodle:**
> Los estudiantes disponen en la sección del aula virtual de dos manuales de referencia rápida en formato PDF, listos para descargar e imprimir (tener en cuenta que las aplicaciones están en inglés):
> - `guia-rapida-fiji-desktop.pdf`: Catálogo conceptual de operaciones para la versión de escritorio de Fiji / ImageJ.
> - `guia-rapida-imagej-online.pdf`: Catálogo conceptual de operaciones optimizado para la versión web de ImageJ.js en el navegador.

---

## 4. Estructura y Etapas del Pipeline de Procesamiento

El equipo debe diseñar, justificar y aplicar una secuencia analítica compuesta por 5 etapas canónicas:

`[Etapa 1: Ingesta e Histograma]` → `[Etapa 2: Preprocesamiento]` → `[Etapa 3: Segmentación]` → `[Etapa 4: Morfología]` → `[Etapa 5: Extracción Metrológica]`

### Etapa 1: Ingesta, Espacio de Intensidad y Diagnóstico de Histograma
- Conversión de la imagen al espacio de intensidad monocromático de 8 bits (matriz de intensidad con valores discretos en `[0, 255]`).
- Extracción e interpretación del histograma global de frecuencias de niveles de gris.
- **Diagnóstico explícito:** Evaluar si el histograma presenta distribución unimodal, bimodal o multimodal; diagnosticar problemas de exposición fotométrica (subexposición, sobreexposición o rango dinámico comprimido) e identificar la tipología de ruido presente (Gaussiano vs. impulsivo Sal y Pimienta).

### Etapa 2: Preprocesamiento y Filtrado Espacial
- Selección y aplicación justificada de un filtro espacial lineal o no lineal (Media, Gaussiano, Mediana o Bilateral) acorde al tipo de ruido diagnosticado en la Etapa 1.
- Justificación matemática y cualitativa del tamaño del kernel (ventana deslizante) utilizado, evaluando el balance entre reducción de perturbaciones y preservación de bordes estructurales.
- Compensación de iluminación heterogénea o bajo contraste local mediante Ecualización Adaptativa de Histograma Limitada por Contraste (**CLAHE**).

### Etapa 3: Segmentación y Binarización
- Aplicación de umbralización global automática basada en la maximización de la varianza inter-clase (**Algoritmo de Otsu**).
- Determinación y ajuste de la polaridad de la máscara binaria (*Dark background* activo o inactivo) para garantizar que los objetos de interés correspondan a píxeles blancos (valor 255) y el fondo a píxeles negros (valor 0).
- Comparación crítica entre el umbral automático calculado por Otsu frente a un ajuste manual empírico.

### Etapa 4: Acondicionamiento Morfológico Binario y Separación de Estructuras
- Aplicación de operaciones morfológicas basadas en elementos estructurantes:
  - **Apertura Morfológica (Erosión seguida de Dilatación):** Supresión de espículas, pequeños falsos positivos y ruido binario residual.
  - **Cierre Morfológico (Dilatación seguida de Erosión) o Relleno de Huecos:** Reconstitución de poros internos y sellado de discontinuidades en el interior de los objetos.
  - Desacople de partículas adosadas o agrupadas mediante la **Transformada de Divisoria de Aguas (*Watershed*)** basada en el mapa de distancia euclídea, evitando sobre-segmentación artificial.

### Etapa 5: Análisis de Componentes Conectados (CCA) y Extracción Metrológica
- Configuración previa de los descriptores geométricos a medir en la herramienta (`Area`, `Centroid`, `Perimeter`, `Shape Descriptors - Circularity`).
- Ejecución del motor de análisis de partículas (`Analyze Particles` o equivalente), configurando rangos de exclusión por área mínima (filtrado de ruido microscópico) y por circularidad.
- Habilitación de la exclusión en bordes de cuadro (`Exclude on edges`) para evitar distorsiones estadísticas con objetos truncados.
- Generación del mapa visual de contornos identificados y exportación de la tabla de resultados métricos en formato numérico (`.csv`).

---

## 5. Modalidad de Trabajo, Conformación de Grupos y Entregables en Moodle

> **Requisito Obligatorio: Conformación de Grupos en Moodle**  
> En el aula virtual de Moodle se encuentra habilitada la actividad interactiva **"Selector de Grupos"** (*Selección de grupos*). Cada estudiante debe ingresar y registrarse por sí mismo en el grupo correspondiente junto a sus compañeros de equipo (con un **máximo de hasta 3 miembros**).  
> **Condición excluyente:** Todos los estudiantes que presenten el trabajo deben tener obligatoriamente un grupo asignado en Moodle. Si un alumno no figura registrado en el selector de grupos, el sistema no podrá asentar su entrega ni asignar la calificación correspondiente.

### Entregable A: Tarea en Moodle – Informe Técnico Grupal (PDF)
Un integrante por grupo deberá subir un archivo único en formato PDF (denominado `TP_Integrador_VA_Grupo_XX.pdf`), con una **extensión máxima de 6 páginas**, estructurado obligatoriamente bajo los siguientes apartados:

1. **Carátula y Datos Institucionales:** Título del trabajo, imagen seleccionada, nombres completos y correos de los integrantes.
2. **Diagnóstico Fotométrico y de Adquisición:** Captura del histograma inicial, análisis del rango dinámico e identificación justificada del ruido.
3. **Diagrama de Flujo del Pipeline:** Esquema en bloques de las operaciones realizadas, consignando para cada una la herramienta empleada y los parámetros exactos (tipo de filtro, radio de kernel, umbral de Otsu, elemento estructurante).
4. **Justificación Teórica y Analítica:** Discusión sobre por qué se seleccionaron determinados algoritmos en desmedro de otros (ej. Mediana vs. Gaussiano, CLAHE vs. Ecualización Global).
5. **Memoria Gráfica de Transformación:** Galería comparativa con capturas de pantalla de la imagen en cada hito del proceso (`Original` → `Filtrada` → `Binarizada` → `Morfológica` → `Contornos numerados`).
6. **Cuadro Estadístico y Metrología:** Tabla resumen con: recuento total de objetos válidos, área media, mínima y máxima (en $\text{px}^2$), circularidad promedio ($C = \frac{4\pi \cdot \text{Área}}{\text{Perímetro}^2}$) y porcentaje de ocupación superficial.
7. **Auditoría de Errores y Conclusiones:** Análisis crítico de posibles casos de sub-segmentación o sobre-segmentación y propuestas de optimización.

### Entregable B: Cuestionario en Moodle – Validación Técnica y Numérica
Todos los estudiantes deberán responder un cuestionario interactivo en Moodle (máximo 10 preguntas) que valida la coherencia entre las mediciones obtenidas y los fundamentos conceptuales (preguntas numéricas con margen de tolerancia $\pm 2$, emparejamiento de conceptos morfológicos, completamiento de frases y opciones múltiples de diagnóstico).

> **Nota sobre el Cuestionario:** El cuestionario se hará disponible 2 días antes del cierre de la fecha de entrega.

---

## 6. Cronograma y Condiciones de Entrega

- **Fecha de Inicio / Apertura:** Lunes de la Semana 1.
- **Plazo de Realización:** 14 días corridos (2 semanas).
- **Fecha Límite de Entrega:** Domingo de la Semana 2, 23:59 hs (vía Campus Virtual Moodle).
- **Canales de Asesoramiento:** Foro de Consultas Técnicas en Moodle y sesiones de consulta síncrona en los horarios de práctica.

#!/usr/bin/env python3
"""
Pipeline de Procesamiento Digital de Imágenes para Retinografía Vascular Digital
TPI Visión Artificial - Licenciatura en Inteligencia Artificial (2026)
Autores:
  - Bringas, Mateo Lautaro (Legajo: 435719)
  - Castro, Cristian Leonel (Legajo: 435837)
  - Garcia Pintos, Valentin (Legajo: 435804)
"""

import os
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import ndimage as ndi
from skimage.segmentation import watershed
from skimage.feature import peak_local_max
from skimage.morphology import disk, opening, closing, remove_small_objects

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    img_path = os.path.join(base_dir, 'data', 'images', '3.png')
    output_fig_dir = os.path.join(base_dir, 'docs', 'informe_latex', 'figuras')
    output_csv_path = os.path.join(base_dir, 'data', 'results_metrologia_retina.csv')
    os.makedirs(output_fig_dir, exist_ok=True)
    os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)

    print(f"Cargando imagen desde: {img_path}")
    img_bgr = cv2.imread(img_path)
    if img_bgr is None:
        raise FileNotFoundError(f"No se pudo cargar la imagen: {img_path}")
    
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    h, w, c = img_rgb.shape
    print(f"Dimensiones de la imagen: {w}x{h} píxeles, canales: {c}")

    # ==========================================
    # ETAPA 1: Ingesta, Espacio de Intensidad y Diagnóstico de Histograma
    # ==========================================
    ch_r = img_rgb[:, :, 0]
    ch_g = img_rgb[:, :, 1] # CANAL VERDE: Mayor contraste espectral
    ch_b = img_rgb[:, :, 2]
    gray_img = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)

    # Máscara del campo visual retiniano (FOV - Field of View)
    _, fov_mask = cv2.threshold(gray_img, 15, 255, cv2.THRESH_BINARY)
    fov_mask = cv2.morphologyEx(fov_mask, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15)))
    fov_pixels = ch_g[fov_mask > 0]
    total_retina_area_px = int(np.count_nonzero(fov_mask))
    print(f"Área útil del fondo de ojo (FOV): {total_retina_area_px} px^2")

    # Gráfico Figura 1: Diagnóstico de Histograma y Canales
    fig, axs = plt.subplots(2, 3, figsize=(14, 8))
    fig.patch.set_facecolor('#ffffff')

    axs[0, 0].imshow(img_rgb)
    axs[0, 0].set_title("(a) Retinografía Original RGB", fontsize=11, fontweight='bold')
    axs[0, 0].axis('off')

    axs[0, 1].imshow(ch_g, cmap='gray')
    axs[0, 1].set_title("(b) Canal Verde (G) - Alto Contraste", fontsize=11, fontweight='bold')
    axs[0, 1].axis('off')

    axs[0, 2].imshow(gray_img, cmap='gray')
    axs[0, 2].set_title("(c) Escala de Grises Estándar (8-bit)", fontsize=11, fontweight='bold')
    axs[0, 2].axis('off')

    # Histograma comparativo de canales R, G, B en FOV
    axs[1, 0].hist(ch_r[fov_mask > 0], bins=256, range=(0, 256), color='red', alpha=0.5, label='Canal R (Saturado)')
    axs[1, 0].hist(ch_g[fov_mask > 0], bins=256, range=(0, 256), color='green', alpha=0.6, label='Canal G (Óptimo)')
    axs[1, 0].hist(ch_b[fov_mask > 0], bins=256, range=(0, 256), color='blue', alpha=0.5, label='Canal B (Subexpuesto)')
    axs[1, 0].set_title("(d) Descomposición Espectral en FOV", fontsize=11, fontweight='bold')
    axs[1, 0].set_xlabel("Nivel de Gris [0 - 255]")
    axs[1, 0].set_ylabel("Frecuencia (Píxeles)")
    axs[1, 0].legend(loc='upper right', fontsize=8)
    axs[1, 0].grid(True, alpha=0.3)

    # Histograma del Canal Verde en FOV con diagnóstico estadístico
    mean_val = float(np.mean(fov_pixels))
    std_val = float(np.std(fov_pixels))
    p5, p95 = np.percentile(fov_pixels, [5, 95])
    axs[1, 1].hist(fov_pixels, bins=256, range=(0, 256), color='#2e7d32', edgecolor='#1b5e20', alpha=0.7)
    axs[1, 1].axvline(mean_val, color='darkorange', linestyle='--', linewidth=2, label=f'Media: {mean_val:.1f} (std={std_val:.1f})')
    axs[1, 1].axvline(p5, color='gray', linestyle=':', label=f'P5: {p5:.0f}')
    axs[1, 1].axvline(p95, color='gray', linestyle=':', label=f'P95: {p95:.0f}')
    axs[1, 1].set_title("(e) Histograma Canal G (Diagnóstico)", fontsize=11, fontweight='bold')
    axs[1, 1].set_xlabel("Nivel de Gris [0 - 255]")
    axs[1, 1].set_ylabel("Frecuencia")
    axs[1, 1].legend(loc='upper right', fontsize=8)
    axs[1, 1].grid(True, alpha=0.3)

    # Gráfico de perfil transversal de intensidad (efecto viñeteado / iluminación esférica)
    center_y = h // 2
    profile_g = ch_g[center_y, :]
    axs[1, 2].plot(profile_g, color='teal', linewidth=1.5, label='Intensidad Canal G')
    axs[1, 2].set_title(f"(f) Perfil Transversal (Línea Y={center_y})", fontsize=11, fontweight='bold')
    axs[1, 2].set_xlabel("Posición X (Píxeles)")
    axs[1, 2].set_ylabel("Intensidad")
    axs[1, 2].grid(True, alpha=0.3)
    axs[1, 2].legend(loc='upper left', fontsize=8)

    plt.tight_layout()
    fig1_path = os.path.join(output_fig_dir, 'fig1_diagnostico_histograma.png')
    plt.savefig(fig1_path, dpi=300)
    plt.close()
    print(f"Figura 1 guardada en: {fig1_path}")

    # ==========================================
    # ETAPA 2: Preprocesamiento y Filtrado Espacial
    # ==========================================
    # Filtro Mediana 3x3: atenuación de ruido térmico/gaussiano con preservación de aristas vivas
    denoised_g = cv2.medianBlur(ch_g, 3)

    # Compensación de iluminación no uniforme mediante CLAHE
    clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
    enhanced_g = clahe.apply(denoised_g)

    # Gráfico comparativo de filtros
    fig, axs = plt.subplots(1, 4, figsize=(16, 4))
    axs[0].imshow(ch_g, cmap='gray')
    axs[0].set_title("(a) Canal Verde Original", fontsize=10, fontweight='bold')
    axs[0].axis('off')

    gauss_blur = cv2.GaussianBlur(ch_g, (5, 5), 1.2)
    axs[1].imshow(gauss_blur, cmap='gray')
    axs[1].set_title("(b) Gaussiano (Bordes suavizados)", fontsize=10, fontweight='bold')
    axs[1].axis('off')

    axs[2].imshow(denoised_g, cmap='gray')
    axs[2].set_title("(c) Mediana 3x3 (Preserva aristas)", fontsize=10, fontweight='bold')
    axs[2].axis('off')

    axs[3].imshow(enhanced_g, cmap='gray')
    axs[3].set_title("(d) CLAHE (Compensación Local)", fontsize=10, fontweight='bold')
    axs[3].axis('off')

    plt.tight_layout()
    fig4_path = os.path.join(output_fig_dir, 'fig4_comparativa_filtros_clahe.png')
    plt.savefig(fig4_path, dpi=300)
    plt.close()
    print(f"Figura 4 (Comparativa filtros) guardada en: {fig4_path}")

    # ==========================================
    # ETAPA 3: Segmentación y Binarización
    # ==========================================
    # Sustracción de fondo morfológica (Rolling Ball equivalente) para normalizar gradientes esféricos
    kernel_bg = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (31, 31))
    background_estimate = cv2.morphologyEx(enhanced_g, cv2.MORPH_DILATE, kernel_bg)
    vessel_enhanced = cv2.subtract(background_estimate, enhanced_g)
    vessel_enhanced[fov_mask == 0] = 0

    # Umbral de Otsu (Dark background: Vasos en 255 blanco, Fondo en 0 negro)
    otsu_thresh_val, binary_otsu = cv2.threshold(vessel_enhanced, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    print(f"Umbral de Otsu calculado: {otsu_thresh_val:.2f}")

    # ==========================================
    # ETAPA 4: Acondicionamiento Morfológico Binario y Separación
    # ==========================================
    # Apertura morfológica con disco r=1 para suprimir ruido granular residual y espículas
    opened = opening(binary_otsu > 0, disk(1))

    # Cierre morfológico y relleno para sellar el reflejo central del lumen vascular
    closed = closing(opened, disk(2))
    filled = ndi.binary_fill_holes(closed)

    # Filtrado de objetos espurios microscópicos (< 20 px)
    cleaned = remove_small_objects(filled, min_size=20)

    # Transformada de Distancia y Watershed con líneas divisorias
    distance = ndi.distance_transform_edt(cleaned)
    coords = peak_local_max(distance, min_distance=8, labels=cleaned)
    mask = np.zeros(distance.shape, dtype=bool)
    mask[tuple(coords.T)] = True
    markers, _ = ndi.label(mask)
    labels_ws = watershed(-distance, markers, mask=cleaned, watershed_line=True)
    num_ws_markers = np.max(markers)
    print(f"Marcadores identificados por picos de distancia: {num_ws_markers}")

    # ==========================================
    # ETAPA 5: Análisis de Componentes Conectados (CCA) y Extracción Metrológica
    # ==========================================
    # Cada región aislada por las líneas divisorias de watershed tiene una etiqueta distinta de 0
    bin_ws = (labels_ws > 0).astype(np.uint8) * 255
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(bin_ws, connectivity=8)

    records = []
    outlines_img = img_rgb.copy()
    valid_count = 0
    margin = 8 # Margen perimetral para "Exclude on edges"

    for i in range(1, num_labels):
        area = float(stats[i, cv2.CC_STAT_AREA])
        x = stats[i, cv2.CC_STAT_LEFT]
        y = stats[i, cv2.CC_STAT_TOP]
        w_box = stats[i, cv2.CC_STAT_WIDTH]
        h_box = stats[i, cv2.CC_STAT_HEIGHT]
        cx, cy = centroids[i]

        # Filtro de área mínima
        if area < 20:
            continue
        # Excluir objetos que toquen el borde de cuadro
        if x <= margin or y <= margin or (x + w_box) >= (w - margin) or (y + h_box) >= (h - margin):
            continue
        # Excluir objetos en el contorno exterior del FOV
        if fov_mask[int(np.clip(cy, 0, h-1)), int(np.clip(cx, 0, w-1))] == 0:
            continue

        component_mask = (labels == i).astype(np.uint8)
        cnts, _ = cv2.findContours(component_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        if not cnts:
            continue
        perimeter = float(cv2.arcLength(cnts[0], True))
        if perimeter == 0:
            continue

        # Circularidad C = 4 * pi * Area / Perimeter^2
        circularity = (4.0 * np.pi * area) / (perimeter ** 2)

        valid_count += 1
        records.append({
            'ID': valid_count,
            'Area_px2': area,
            'Perimeter_px': round(perimeter, 2),
            'Circularity': round(circularity, 4),
            'Centroid_X': round(cx, 2),
            'Centroid_Y': round(cy, 2),
            'Bounding_Width': w_box,
            'Bounding_Height': h_box
        })

        # Dibujar contorno en la imagen
        cv2.drawContours(outlines_img, cnts, -1, (0, 255, 255), 1)
        if area > 100 or valid_count <= 25:
            cv2.putText(outlines_img, str(valid_count), (int(cx), int(cy)), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (255, 30, 30), 1)

    df_metrics = pd.DataFrame(records)
    df_metrics.to_csv(output_csv_path, index=False)
    print(f"Métricas exportadas a: {output_csv_path}")

    # Estadísticas globales
    total_valid_objects = len(df_metrics)
    area_total_vascular = float(df_metrics['Area_px2'].sum())
    area_mean = float(df_metrics['Area_px2'].mean())
    area_median = float(df_metrics['Area_px2'].median())
    area_std = float(df_metrics['Area_px2'].std())
    area_min = float(df_metrics['Area_px2'].min())
    area_max = float(df_metrics['Area_px2'].max())
    circ_mean = float(df_metrics['Circularity'].mean())
    circ_median = float(df_metrics['Circularity'].median())
    vascular_occupancy_pct = (area_total_vascular / total_retina_area_px) * 100.0

    print("\n" + "="*55)
    print("RESUMEN METROLÓGICO CUANTITATIVO OFICIAL")
    print("="*55)
    print(f"Objetos válidos medidos (CCA): {total_valid_objects}")
    print(f"Área vascular total segmentada: {area_total_vascular:.2f} px^2")
    print(f"Área media: {area_mean:.2f} px^2 (Mediana: {area_median:.2f} px^2)")
    print(f"Área mínima: {area_min:.2f} px^2 | Área máxima: {area_max:.2f} px^2")
    print(f"Desviación estándar de área: {area_std:.2f} px^2")
    print(f"Circularidad promedio: {circ_mean:.4f} (Mediana: {circ_median:.4f})")
    print(f"Porcentaje de ocupación superficial vascular: {vascular_occupancy_pct:.2f}%")
    print("="*55 + "\n")

    # Guardar resumen en texto
    summary_path = os.path.join(base_dir, 'data', 'resumen_estadistico.txt')
    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write(f"TPI Visión Artificial - Retinografía Vascular Digital (3.png)\n")
        f.write(f"Autores: Bringas, Mateo Lautaro (435719) | Castro, Cristian Leonel (435837) | Garcia Pintos, Valentin (435804)\n\n")
        f.write(f"Área FOV Fondo de Ojo: {total_retina_area_px} px^2\n")
        f.write(f"Recuento Componentes Válidos: {total_valid_objects}\n")
        f.write(f"Umbral de Otsu Calculado: {otsu_thresh_val:.2f}\n")
        f.write(f"Área Vascular Total: {area_total_vascular:.2f} px^2\n")
        f.write(f"Área Media: {area_mean:.2f} px^2\n")
        f.write(f"Área Mediana: {area_median:.2f} px^2\n")
        f.write(f"Área Mínima: {area_min:.2f} px^2\n")
        f.write(f"Área Máxima: {area_max:.2f} px^2\n")
        f.write(f"Desviación Estándar Área: {area_std:.2f} px^2\n")
        f.write(f"Circularidad Promedio: {circ_mean:.4f}\n")
        f.write(f"Circularidad Mediana: {circ_median:.4f}\n")
        f.write(f"Porcentaje Ocupación Superficial: {vascular_occupancy_pct:.2f}%\n")

    # ==========================================
    # GENERACIÓN DE FIGURAS PARA EL INFORME LATEX
    # ==========================================
    # Figura 3: Memoria Gráfica de Transformación (6 paneles comparativos)
    fig, axs = plt.subplots(2, 3, figsize=(15, 10))
    axs[0, 0].imshow(img_rgb)
    axs[0, 0].set_title("(a) Imagen Original RGB", fontsize=11, fontweight='bold')
    axs[0, 0].axis('off')

    axs[0, 1].imshow(enhanced_g, cmap='gray')
    axs[0, 1].set_title("(b) Canal Verde Filtrado (Mediana 3x3 + CLAHE)", fontsize=11, fontweight='bold')
    axs[0, 1].axis('off')

    axs[0, 2].imshow(binary_otsu, cmap='gray')
    axs[0, 2].set_title(f"(c) Binarización Otsu Invertida (T={otsu_thresh_val:.1f})", fontsize=11, fontweight='bold')
    axs[0, 2].axis('off')

    axs[1, 0].imshow(cleaned, cmap='gray')
    axs[1, 0].set_title("(d) Acondicionamiento Morfológico (Apertura + Cierre)", fontsize=11, fontweight='bold')
    axs[1, 0].axis('off')

    axs[1, 1].imshow(labels_ws, cmap='nipy_spectral')
    axs[1, 1].set_title(f"(e) Desacople Watershed (Líneas Divisorias)", fontsize=11, fontweight='bold')
    axs[1, 1].axis('off')

    axs[1, 2].imshow(outlines_img)
    axs[1, 2].set_title(f"(f) Contornos Numerados (N={total_valid_objects})", fontsize=11, fontweight='bold')
    axs[1, 2].axis('off')

    plt.tight_layout()
    fig3_path = os.path.join(output_fig_dir, 'fig3_memoria_grafica_etapas.png')
    plt.savefig(fig3_path, dpi=300)
    plt.close()
    print(f"Figura 3 (Memoria gráfica) guardada en: {fig3_path}")

    # Figura 5: Outlines de Alta Resolución
    plt.figure(figsize=(10, 7))
    plt.imshow(outlines_img)
    plt.title(f"Extracción Metrológica: Contornos y Detección Vascular (N={total_valid_objects})", fontsize=12, fontweight='bold')
    plt.axis('off')
    plt.tight_layout()
    fig5_path = os.path.join(output_fig_dir, 'fig5_outlines_etiquetadas.png')
    plt.savefig(fig5_path, dpi=300)
    plt.close()
    print(f"Figura 5 (Outlines etiquetadas) guardada en: {fig5_path}")

    # Figura 6: Distribución Metrológica (Histogramas y Boxplots de Área y Circularidad)
    fig, axs = plt.subplots(1, 2, figsize=(12, 4.5))
    axs[0].hist(df_metrics['Area_px2'], bins=20, color='#1976d2', edgecolor='#0d47a1', alpha=0.7)
    axs[0].set_title("Distribución de Áreas de Segmentos Vasculares", fontsize=11, fontweight='bold')
    axs[0].set_xlabel("Área (px²)")
    axs[0].set_ylabel("Frecuencia (Segmentos)")
    axs[0].set_yscale('log')
    axs[0].grid(True, alpha=0.3)

    axs[1].hist(df_metrics['Circularity'], bins=15, range=(0, 1.0), color='#388e3c', edgecolor='#1b5e20', alpha=0.7)
    axs[1].axvline(circ_mean, color='red', linestyle='--', linewidth=1.5, label=f'Media: {circ_mean:.3f}')
    axs[1].set_title("Distribución del Factor de Circularidad", fontsize=11, fontweight='bold')
    axs[1].set_xlabel("Circularidad (4π·Área / Perímetro²)")
    axs[1].set_ylabel("Frecuencia")
    axs[1].legend(loc='upper right')
    axs[1].grid(True, alpha=0.3)

    plt.tight_layout()
    fig6_path = os.path.join(output_fig_dir, 'fig6_distribucion_metrologica.png')
    plt.savefig(fig6_path, dpi=300)
    plt.close()
    print(f"Figura 6 (Distribución metrológica) guardada en: {fig6_path}")

    # Figura 2: Diagrama de Flujo del Pipeline
    fig, ax = plt.subplots(figsize=(12, 3.2))
    ax.axis('off')
    steps = [
        "1. Ingesta\nCanal Verde (G)\n(8-bit [0,255])",
        "2. Preprocesado\nFiltro Mediana 3x3\n+ CLAHE Local",
        "3. Segmentación\nUmbral Otsu\nDark Background",
        "4. Morfología\nApertura + Cierre\n+ Watershed",
        "5. Metrología\nCCA + Filtro Área\nOutlines + CSV"
    ]
    colors = ['#e1f5fe', '#e8f5e9', '#fff3e0', '#f3e5f5', '#fbe9e7']
    border_colors = ['#0288d1', '#388e3c', '#f57c00', '#7b1fa2', '#d84315']

    for i, (text, col, bcol) in enumerate(zip(steps, colors, border_colors)):
        box = dict(boxstyle='round,pad=0.7', facecolor=col, edgecolor=bcol, linewidth=2)
        ax.text(i * 2.3 + 1.0, 1.0, text, ha='center', va='center', fontsize=9.5, fontweight='bold', bbox=box)
        if i < len(steps) - 1:
            ax.annotate('', xy=(i * 2.3 + 2.05, 1.0), xytext=(i * 2.3 + 1.85, 1.0),
                        arrowprops=dict(facecolor='#424242', edgecolor='#424242', arrowstyle='->', lw=2.2))

    ax.set_xlim(-0.2, 10.5)
    ax.set_ylim(0.2, 1.8)
    plt.tight_layout()
    fig2_path = os.path.join(output_fig_dir, 'fig2_flujograma_pipeline.png')
    plt.savefig(fig2_path, dpi=300)
    plt.close()
    print(f"Figura 2 (Flujograma) guardada en: {fig2_path}")

    print("\n¡Pipeline ejecutado con éxito total!")

if __name__ == '__main__':
    main()

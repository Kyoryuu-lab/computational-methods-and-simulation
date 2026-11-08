"""
==============================================================================
Module:      monte_carlo_area.py
Description: Monte Carlo integration for geometric area estimation.
             Extracts boundary contours and applies spatial point-in-polygon tests.
==============================================================================
"""

import os
import random
import cv2
import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Polygon, Point
from typing import Optional, Tuple


def generate_synthetic_map_mask(width: int = 600, height: int = 600) -> np.ndarray:
    """Erzeugt eine synthetische Testgeometrie, falls kein externes Bild vorhanden ist."""
    img = np.zeros((height, width, 3), dtype=np.uint8)
    points = np.array([
        [150, 100], [450, 120], [520, 300], [420, 500],
        [220, 480], [100, 350], [120, 200]
    ], dtype=np.int32)
    cv2.fillPoly(img, [points], (255, 255, 255))
    return img


def estimate_area_monte_carlo(image_path: Optional[str] = None, n_iters: int = 40000,
                              scale_factor: float = 0.15, real_area: float = 6890.0,
                              save_plot: Optional[str] = None) -> Tuple[float, float]:
    """
    Extrahiert den Umriss eines geografischen Gebiets und schätzt dessen Fläche via Monte-Carlo-Integration.
    """
    image = None
    if image_path and os.path.exists(image_path):
        image = cv2.imread(image_path)

    if image is None:
        print("[!] Externes Bild nicht gefunden. Verwende prozedurales Test-Polygon.")
        image = generate_synthetic_map_mask()

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        raise RuntimeError("Keine geschlossenen Konturen im Bild erkannt.")

    main_contour = max(contours, key=cv2.contourArea)
    contour_coords = main_contour.reshape(-1, 2)
    polygon = Polygon(contour_coords)

    xmin, ymin, xmax, ymax = polygon.bounds
    bounding_box_area = scale_factor * (xmax - xmin) * scale_factor * (ymax - ymin)

    inside_count = 0
    xi, yi, xo, yo = [], [], [], []

    for _ in range(n_iters):
        rx = random.uniform(xmin, xmax)
        ry = random.uniform(ymin, ymax)

        if polygon.contains(Point(rx, ry)):
            xi.append(rx)
            yi.append(ry)
            inside_count += 1
        else:
            xo.append(rx)
            yo.append(ry)

    estimated_area = bounding_box_area * (inside_count / n_iters)
    error_percent = abs((estimated_area - real_area) / real_area) * 100.0

    print(f"[*] Monte-Carlo-Integration ({n_iters:,} Punkte):")
    print(f"    Punkte innerhalb : {inside_count:,} / {n_iters:,}")
    print(f"    Geschätzte Fläche: {estimated_area:.4f} km² (Referenz: {real_area:.1f} km²)")
    print(f"    Abweichung       : {error_percent:.3f} %")

    plt.figure(figsize=(9, 9))
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.scatter(xi, yi, color='blue', s=1, alpha=0.4, label='Inkludierte Punkte')
    plt.scatter(xo, yo, color='red', s=1, alpha=0.4, label='Exkludierte Punkte')
    plt.plot(contour_coords[:, 0], contour_coords[:, 1], color="yellow", linewidth=2, label="Bereichsgrenze")

    plt.legend()
    plt.title(f"Monte-Carlo-Flächenbestimmung (Fläche: {estimated_area:.1f} km²)")

    if save_plot:
        plt.savefig(save_plot, dpi=300, bbox_inches='tight')
        print(f"[+] Diagramm gespeichert: {save_plot}")
        plt.close()
    else:
        plt.show()

    return estimated_area, error_percent


if __name__ == "__main__":
    estimate_area_monte_carlo()

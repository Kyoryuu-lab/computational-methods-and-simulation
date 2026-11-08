"""
==============================================================================
Module:      interpolation.py
Description: Numerical interpolation algorithms: Newton's divided difference
             polynomial interpolation and linear interpolation.
==============================================================================
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple, Optional


def linear_interpolation(x: List[float], y: List[float], x_eval: List[float]) -> np.ndarray:
    """Berechnet die stueckweise lineare Interpolation."""
    return np.interp(x_eval, x, y)


def compute_divided_differences(x: List[float], y: List[float]) -> np.ndarray:
    """
    Berechnet die Tabelle der dividierten Differenzen fuer das Newton-Polynom.
    Gibt die oberste Zeile der Differenzentabelle zurueck.
    """
    n = len(x)
    coef = np.zeros([n, n])
    coef[:, 0] = y

    for j in range(1, n):
        for i in range(n - j):
            coef[i][j] = (coef[i + 1][j - 1] - coef[i][j - 1]) / (x[i + j] - x[i])

    return coef[0, :]


def evaluate_newton_polynomial(coef: np.ndarray, x_data: List[float], x_val: float) -> float:
    """Wertet das Newton-Polynom an einer Stelle x_val nach dem Horner-Schema aus."""
    n = len(x_data) - 1
    p = coef[n]
    for k in range(1, n + 1):
        p = coef[n - k] + (x_val - x_data[n - k]) * p
    return float(p)


def newton_interpolation(x: List[float], y: List[float], x_eval: List[float]) -> np.ndarray:
    """Interpoliert Stützstellen mittels des Newtonschen Interpolationspolynoms."""
    coef = compute_divided_differences(x, y)
    return np.array([evaluate_newton_polynomial(coef, x, xi) for xi in x_eval])


def run_interpolation_analysis(save_plot: Optional[str] = None):
    """Fuehrt die Vergleichsberechnung und Visualisierung durch."""
    x = [0.101, 0.106, 0.111, 0.116, 0.121, 0.126, 0.131, 0.136, 0.141, 0.146, 0.151]
    y = [1.26183, 1.27644, 1.29122, 1.30617, 1.32130, 1.33660, 1.35207, 1.36773, 1.38357, 1.39959, 1.41579]
    eval_points = [0.1035, 0.1492, 0.1324, 0.159]

    y_linear = linear_interpolation(x, y, eval_points)
    y_newton = newton_interpolation(x, y, eval_points)

    print("[*] Stützstellen x:", x)
    print("[*] Evaluierungspunkte X:", eval_points)
    for pt, y_lin, y_new in zip(eval_points, y_linear, y_newton):
        print(f"    x = {pt:<6} | Linear: {y_lin:.6f} | Newton: {y_new:.6f}")

    plt.figure(figsize=(10, 6))
    plt.plot(x, y, 'bo-', label="Originale Stützstellen (Daten)")
    plt.plot(eval_points, y_linear, 'rs', label="Lineare Interpolation", linestyle='None')
    plt.plot(eval_points, y_newton, 'g^', label="Newton-Interpolation", linestyle='None')

    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("Numerische Interpolation: Newton vs. Linear")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)

    if save_plot:
        plt.savefig(save_plot, dpi=300, bbox_inches='tight')
        print(f"[+] Diagramm gespeichert: {save_plot}")
        plt.close()
    else:
        plt.show()


if __name__ == "__main__":
    run_interpolation_analysis()

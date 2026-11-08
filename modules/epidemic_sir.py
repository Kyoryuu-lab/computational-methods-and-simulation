"""
==============================================================================
Module:      epidemic_sir.py
Description: Epidemiological SIR dynamics with time-dependent lockdown
             interventions solved via Ordinary Differential Equations (ODE).
==============================================================================
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from typing import List, Tuple, Optional


def sir_derivatives(y: Tuple[float, float, float], t: float, n: float, beta: float,
                    gamma: float, lockdown_day: int, lockdown_effect: float) -> Tuple[float, float, float]:
    """Berechnet die rechten Seiten des SIR-Differentialgleichungssystems."""
    s, i, r = y
    beta_eff = beta * (1.0 - lockdown_effect) if t >= lockdown_day else beta

    ds_dt = -beta_eff * s * i / n
    di_dt = (beta_eff * s * i / n) - (gamma * i)
    dr_dt = gamma * i
    return ds_dt, di_dt, dr_dt


def simulate_sir_scenarios(days: int = 180, save_plot: Optional[str] = None):
    """Simuliert und vergleicht mehrere Lockdown-Szenarien."""
    n = 1.0
    i0 = 1.0 / 60000.0
    r0 = 0.0
    s0 = n - i0 - r0
    y0 = (s0, i0, r0)

    reproduction_rate = 1.76
    gamma = 1.0 / 30.0
    beta = reproduction_rate * gamma
    t = np.linspace(0, days, days)

    scenarios = [
        (30, 0.5),   # Lockdown an Tag 30, 50 % Transmission-Senkung
        (50, 0.7),   # Lockdown an Tag 50, 70 % Transmission-Senkung
        (70, 0.9),   # Lockdown an Tag 70, 90 % Transmission-Senkung
    ]

    plt.figure(figsize=(12, 7))
    print("[*] Starte SIR-Differentialgleichungsintegration...")

    for day, effect in scenarios:
        solution = odeint(sir_derivatives, y0, t, args=(n, beta, gamma, day, effect))
        _, i_series, _ = solution.T

        mortality_rate = 0.1
        daily_deaths = mortality_rate * gamma * i_series * n
        peak_day = int(t[np.argmax(daily_deaths)])
        peak_val = float(np.max(daily_deaths))

        print(f"    - Szenario (Tag {day:2d}, -{int(effect*100)}%): Peak an Tag {peak_day:3d} | Max. tägliche Mortalität: {peak_val:.2e}")
        plt.plot(t, daily_deaths, label=f"Lockdown: Tag {day}, Reduktion {int(effect * 100)} %")

    plt.xlabel("Tage seit Ausbruch")
    plt.ylabel("Tägliche Todesfälle (normalisiert)")
    plt.title("SIR-Epidemiemodell: Einfluss von Lockdown-Zeitpunkt und -Stärke")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)

    if save_plot:
        plt.savefig(save_plot, dpi=300, bbox_inches='tight')
        print(f"[+] Diagramm gespeichert: {save_plot}")
        plt.close()
    else:
        plt.show()


if __name__ == "__main__":
    simulate_sir_scenarios()

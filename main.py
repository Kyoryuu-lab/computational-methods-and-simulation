"""
==============================================================================
Project:     Computational Methods and Simulation Suite
File:        main.py
Author:      Yevhen Biezhyn
Description: Unified CLI orchestrator executing numerical polynomial interpolation,
             epidemiological ODE simulation, and Monte Carlo area estimation.
==============================================================================
"""

import argparse
from modules.interpolation import run_interpolation_analysis
from modules.epidemic_sir import simulate_sir_scenarios
from modules.monte_carlo_area import estimate_area_monte_carlo


def print_banner(title: str):
    print("\n" + "=" * 78)
    print(f"  {title.upper()}")
    print("=" * 78)


def main():
    parser = argparse.ArgumentParser(
        description="Computational Methods & Numerical Simulation Suite",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "--module",
        choices=["all", "interpolation", "epidemic", "montecarlo"],
        default="all",
        help=(
            "all           : Führt alle 3 Methoden nacheinander aus (Standard)\n"
            "interpolation : Newton- & Lineare Polynominterpolation\n"
            "epidemic      : SIR-Differentialgleichungsmodell & Lockdowns\n"
            "montecarlo    : Stochastische Monte-Carlo-Flächenintegration"
        )
    )
    parser.add_argument("--save-plots", action="store_true", help="Speichert generierte Diagramme als PNG-Dateien")
    parser.add_argument("--image", type=str, default=None, help="Pfad zu einem Bild für die Monte-Carlo-Integration")
    parser.add_argument("--iterations", type=int, default=40000, help="Anzahl der Monte-Carlo-Stichproben (Standard: 40000)")
    args = parser.parse_args()

    print("=" * 78)
    print("  COMPUTATIONAL METHODS & NUMERICAL SIMULATION SUITE")
    print("=" * 78)

    if args.module in ["all", "interpolation"]:
        print_banner("1. Modul: Numerische Polynominterpolation")
        plot_file = "interpolation_comparison.png" if args.save_plots else None
        run_interpolation_analysis(save_plot=plot_file)

    if args.module in ["all", "epidemic"]:
        print_banner("2. Modul: SIR-Epidemiedynamik (ODE-Integration)")
        plot_file = "sir_epidemic_scenarios.png" if args.save_plots else None
        simulate_sir_scenarios(days=180, save_plot=plot_file)

    if args.module in ["all", "montecarlo"]:
        print_banner("3. Modul: Monte-Carlo-Flächenintegration")
        plot_file = "monte_carlo_area.png" if args.save_plots else None
        estimate_area_monte_carlo(
            image_path=args.image,
            n_iters=args.iterations,
            save_plot=plot_file
        )

    print("\n" + "=" * 78)
    print("  ALLE NUMERISCHEN BERECHNUNGEN ERFOLGREICH ABGESCHLOSSEN.")
    print("=" * 78 + "\n")


if __name__ == "__main__":
    main()

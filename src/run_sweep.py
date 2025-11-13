import csv
import os
from typing import List

from .nozzle import NozzleInputs, performance

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_CSV = os.path.join(PROJECT_ROOT, "nozzle_sweep_results.csv")

def main() -> None:
    # Example sweep: Pc in [30..90] bar, ε in [5, 10, 20], Pa = 101325 Pa
    Pcs = [30e5, 60e5, 90e5]
    eps_list = [5.0, 10.0, 20.0]
    Pa = 101325.0
    # Example hot gas: gamma=1.22, Mw=0.022 kg/mol, Tc=3500 K (условно)
    gamma, Mw, Tc = 1.22, 0.022, 3500.0

    rows: List[dict] = []
    for Pc in Pcs:
        for eps in eps_list:
            out = performance(NozzleInputs(Pc=Pc, Tc=Tc, Pa=Pa, gamma=gamma, Mw=Mw, epsilon=eps))
            rows.append({
                "Pc_bar": Pc/1e5,
                "epsilon": eps,
                "Me": round(out.Me, 4),
                "Pe_kPa": round(out.Pe/1e3, 2),
                "Ve_mps": round(out.Ve, 1),
                "CF": round(out.CF, 4),
                "Isp_s": round(out.Isp, 2),
                "F_per_At_MPa": round(out.F_per_At/1e6, 3),
            })

    with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    print("=== Nozzle sweep done ===")
    print(f"Saved: {OUT_CSV}")

if __name__ == "__main__":
    main()

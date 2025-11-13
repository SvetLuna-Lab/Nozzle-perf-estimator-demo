import csv
import os
from src.nozzle import NozzleInputs, performance

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IN_CSV  = os.path.join(PROJECT_ROOT, "data", "sample_cases.csv")
OUT_CSV = os.path.join(PROJECT_ROOT, "data", "sample_cases_results.csv")

def main() -> None:
    rows_in = []
    with open(IN_CSV, "r", encoding="utf-8") as f:
        r = csv.DictReader(f)
        for row in r:
            rows_in.append(row)

    rows_out = []
    for row in rows_in:
        Pc = float(row["Pc_bar"]) * 1e5
        eps = float(row["epsilon"])
        Tc = float(row["Tc_K"])
        Pa = float(row["Pa_Pa"])
        gamma = float(row["gamma"])
        Mw = float(row["Mw_kg_per_mol"])
        out = performance(NozzleInputs(Pc=Pc, Tc=Tc, Pa=Pa, gamma=gamma, Mw=Mw, epsilon=eps))
        rows_out.append({
            "Pc_bar": float(row["Pc_bar"]),
            "epsilon": eps,
            "Me": round(out.Me, 4),
            "Pe_kPa": round(out.Pe/1e3, 2),
            "Ve_mps": round(out.Ve, 1),
            "CF": round(out.CF, 4),
            "Isp_s": round(out.Isp, 2),
            "F_per_At_MPa": round(out.F_per_At/1e6, 3),
        })

    with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows_out[0].keys()))
        w.writeheader()
        w.writerows(rows_out)

    print(f"Saved: {OUT_CSV}")

if __name__ == "__main__":
    main()

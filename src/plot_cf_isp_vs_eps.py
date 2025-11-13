# file: src/plot_cf_isp_vs_eps.py
# One-figure Matplotlib plot (no seaborn, no custom colors)
import os
import numpy as np
import matplotlib.pyplot as plt

from nozzle import NozzleInputs, performance

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIG_DIR = os.path.join(PROJECT_ROOT, "figures")
os.makedirs(FIG_DIR, exist_ok=True)

# Example conditions (illustrative, idealized)
Pc = 60e5       # Pa
Tc = 3500.0     # K
Pa = 101325.0   # Pa
gamma = 1.22
Mw = 0.022      # kg/mol

eps_values = np.linspace(5.0, 40.0, 60)  # area ratio from 5 to 40
cf_vals = []
isp_vals = []

for eps in eps_values:
    out = performance(NozzleInputs(Pc=Pc, Tc=Tc, Pa=Pa, gamma=gamma, Mw=Mw, epsilon=eps))
    cf_vals.append(out.CF)
    isp_vals.append(out.Isp)

plt.figure()  # single figure
plt.title("Ideal nozzle performance vs area ratio ε (Pc=60 bar, Tc=3500 K, Pa=1 atm)")
plt.plot(eps_values, cf_vals, label="CF")
plt.plot(eps_values, isp_vals, label="Isp (s)")
plt.xlabel("ε = Ae/At")
plt.ylabel("Value")
plt.grid(True, which="both", linestyle="--", alpha=0.4)
plt.legend()
out_path = os.path.join(FIG_DIR, "cf_isp_vs_eps.png")
plt.savefig(out_path, dpi=160, bbox_inches="tight")
print(f"Saved: {out_path}")

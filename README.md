# Nozzle-perf-estimator-demo

> Requires **Python 3.10+**. Pure-Python demo (no external runtime deps).

Minimal estimator of ideal (isentropic) rocket nozzle performance:
- exit state: **Me, Pe, Te**, exit velocity **Ve**
- thrust coefficient **CF**, specific impulse **Isp**, thrust per throat area **F/At**
- sweep script over chamber pressure **Pc** and area ratio **ε**

---

## Repository structure

```text
nozzle-perf-estimator-demo/
├─ src/
│  ├─ __init__.py
│  ├─ thermo.py
│  ├─ nozzle.py
│  └─ run_sweep.py
├─ data/
│  └─ sample_cases.csv
├─ tests/
│  ├─ __init__.py
│  ├─ test_thermo.py
│  └─ test_nozzle.py
├─ docs/
│  └─ ENGINEERING_NOTE.md
├─ CHANGELOG.md
├─ README.md
├─ requirements.txt
└─ .gitignore



Quick start

pip install -r requirements.txt   # installs pytest / pytest-cov if you keep them here
python src/run_sweep.py           # writes nozzle_sweep_results.csv


Optional one-liner check:

python -c "from src.nozzle import NozzleInputs,performance; print(performance(NozzleInputs(60e5,3500,101325,1.22,0.022,10.0)))"


Console output example (from sweep):

=== Nozzle sweep done ===
Saved: /path/to/nozzle_sweep_results.csv


Tests

python -m unittest discover -s tests


test_thermo.py — area–Mach monotonicity and Pe/Pc bounds

test_nozzle.py — plausible ranges and ε–effect on Me and CF


Engineering note

See docs/ENGINEERING_NOTE.md for assumptions, equations, sanity checks, and limitations.


## Changelog
See [CHANGELOG.md](./CHANGELOG.md) for release notes.


## Extending

- Add an over/under-expansion check (compare **Pe** to **Pa**) and a separation warning flag.
- Support CEA-based property tables so **gamma** and **molar mass** vary with temperature (γ(T), Mw(T)).
- Introduce simple loss models / nozzle efficiency factors.
- Generate plots of **CF** and **Isp** versus **ε** (area ratio) and **Pc** (chamber pressure).


License

MIT/Apache-2.0

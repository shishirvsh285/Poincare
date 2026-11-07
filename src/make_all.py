"""Run every simulation and rebuild every figure.  Usage:  python src/make_all.py"""
import importlib
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

SCRIPTS = [
    "01_proof_pigeonhole",
    "02_liouville_blob",
    "03_torus_oscillators",
    "04_cat_map",
    "05_gas_in_box",
    "06_gas_torus",
    "07_torus_figures",
]

if __name__ == "__main__":
    for name in SCRIPTS:
        t0 = time.time()
        print(f"\n=== {name} ===")
        importlib.import_module(name).main()
        print(f"--- done in {time.time() - t0:.0f} s")

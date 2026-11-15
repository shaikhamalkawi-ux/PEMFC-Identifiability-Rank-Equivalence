"""Run all Project 53 v13 reproducibility checks in sequence."""
from __future__ import annotations
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = [
    "reproduce_v7.py",
    "possibilistic_temperature_levels.py",
    "symmetry_nullspace_geometry.py",
    "information_geometry_oed.py",
    "symmetry_breaking_order.py",
    "gauge_fixing_prior_dependence.py",
]

lines = ["PROJECT53 V13 UNIFIED REPRODUCTION"]
for name in SCRIPTS:
    print(f"\n=== {name} ===", flush=True)
    proc = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / name)],
        cwd=ROOT,
        check=False,
        text=True,
    )
    if proc.returncode != 0:
        raise SystemExit(f"{name} failed with exit code {proc.returncode}")
    lines.append(name + ": PASS")

lines.append("PROJECT53 V13 UNIFIED REPRODUCTION: PASS")
out = ROOT / "outputs" / "REPRODUCTION_V13_ALL.txt"
out.parent.mkdir(exist_ok=True)
out.write_text("\n".join(lines) + "\n", encoding="utf-8")
print("\nPROJECT53 V13 UNIFIED REPRODUCTION: PASS")

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
    proc = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / name)],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    lines.append(f"\n=== {name} ===")
    lines.append(proc.stdout.rstrip())

lines.append("\nPROJECT53 V13 UNIFIED REPRODUCTION: PASS")
out = ROOT / "outputs" / "REPRODUCTION_V13_ALL.txt"
out.parent.mkdir(exist_ok=True)
out.write_text("\n".join(lines) + "\n", encoding="utf-8")
print("\n".join(lines[-3:]))

#!/usr/bin/env python3
"""Run the numerical certificates, then the finite identity diagnostics.

The individual programs contain their numerical gates. This runner preserves
their complete output under verification/output and propagates any failure.
It does not interpret a successful finite check as a proof of a general claim.
"""

from pathlib import Path
import subprocess
import sys


def main() -> int:
    directory = Path(__file__).resolve().parent
    output = directory / "output"
    output.mkdir(exist_ok=True)
    programs = (
        ("norm_circle_interval.py", "rigorous norm-tail certificate"),
        ("core_transfer_bounds.py", "rigorous security-transfer arithmetic"),
        ("norm_circle_identity_checks.py", "floating-point identity diagnostics"),
    )
    for filename, description in programs:
        result = subprocess.run(
            [sys.executable, str(directory / filename)],
            cwd=directory.parent,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        destination = output / (Path(filename).stem + ".txt")
        destination.write_text(result.stdout, encoding="utf-8")
        if result.returncode:
            sys.stderr.write(result.stderr)
            sys.stderr.write(result.stdout)
            print(f"FAIL: {description}", file=sys.stderr)
            return result.returncode
        if result.stderr:
            sys.stderr.write(result.stderr)
        print(f"PASS: {description}", flush=True)
    print("Complete outputs: verification/output/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

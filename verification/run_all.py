#!/usr/bin/env python3
"""Check repository integrity, numerical certificates, diagnostics, and plot assets.

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
        (("check_repository.py",), "report, learning map, and navigation integrity"),
        (("norm_circle_interval.py",), "rigorous norm-tail certificate"),
        (("core_transfer_bounds.py",), "rigorous security-transfer arithmetic"),
        (("norm_circle_identity_checks.py",), "floating-point identity diagnostics"),
        (("Graph/generate_plots.py", "--check"), "analytic plot regeneration and asset identity"),
    )
    for arguments, description in programs:
        filename = arguments[0]
        result = subprocess.run(
            [sys.executable, str(directory / filename), *arguments[1:]],
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

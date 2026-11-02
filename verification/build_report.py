#!/usr/bin/env python3
"""Rebuild the explanatory report without replacing its reviewed PDF."""

import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--engine", default="pdflatex")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    manifest = json.loads((root / "verification/report_manifest.json").read_text())
    source = root / manifest["source"]
    stored = root / manifest["pdf"]
    if sha256(source) != manifest["source_sha256"]:
        raise SystemExit("Report source differs from the reviewed manifest; inspect the change first.")
    engine = shutil.which(args.engine)
    if engine is None:
        raise SystemExit("pdfLaTeX not found; install TeX Live 2025 or supply --engine.")
    version = subprocess.run([engine, "--version"], check=True, text=True,
                             stdout=subprocess.PIPE).stdout.splitlines()[0]
    if "TeX Live 2025" not in version:
        raise SystemExit(f"TeX Live 2025 is required; found: {version}")
    output = root / "verification/output/report"
    output.mkdir(parents=True, exist_ok=True)
    for attempt in range(1, 4):
        result = subprocess.run(
            [engine, "-interaction=nonstopmode", "-halt-on-error", "-recorder",
             f"-output-directory={output}", str(source)],
            cwd=root, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        )
        (output / f"pass-{attempt}.txt").write_text(result.stdout, encoding="utf-8")
        if result.returncode:
            raise SystemExit(f"Report compilation failed; inspect {output / f'pass-{attempt}.txt'}")
    pdf = output / stored.name
    log = output / f"{source.stem}.log"
    if not pdf.is_file() or not log.is_file():
        raise SystemExit("Compilation did not produce both the fresh PDF and final log.")
    problems = re.findall(r"^.*(?:Overfull|Underfull|Warning:|Undefined control sequence|Missing character).*$",
                          log.read_text(encoding="utf-8", errors="replace"), re.MULTILINE)
    if problems:
        raise SystemExit("Final report log needs review:\n" + "\n".join(problems))
    print(version)
    print(f"Fresh PDF: {pdf.relative_to(root)}")
    print(f"Final log: {log.relative_to(root)}")
    print(f"Fresh PDF SHA256: {sha256(pdf)}")
    print(f"Byte-identical to stored report: {sha256(pdf) == sha256(stored)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

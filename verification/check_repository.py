#!/usr/bin/env python3
"""Check local navigation, the shared learning map, and the reviewed report pair."""

import hashlib
import json
from pathlib import Path
import re
import subprocess
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def slug(text: str) -> str:
    text = re.sub(r"\[([^]]+)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"<[^>]+>", "", text).lower()
    return re.sub(r"[^\w\- ]", "", text).replace(" ", "-")


def anchors(path: Path) -> set[str]:
    found: set[str] = set()
    counts: dict[str, int] = {}
    for heading in re.findall(r"^#{1,6}\s+(.+?)\s*#*\s*$", path.read_text(), re.MULTILINE):
        base = slug(heading)
        count = counts.get(base, 0)
        counts[base] = count + 1
        found.add(base if count == 0 else f"{base}-{count}")
    return found


def main() -> int:
    paths = subprocess.run(["git", "ls-files", "-z"], cwd=ROOT, check=True,
                           stdout=subprocess.PIPE).stdout.decode().split("\0")
    pages = [ROOT / p for p in paths if p.endswith(".md")]
    links = 0
    for page in pages:
        text = re.sub(r"```.*?```", "", page.read_text(encoding="utf-8"), flags=re.DOTALL)
        for target in re.findall(r"\[[^\]]*\]\(([^\s)]+)(?:\s+[^)]*)?\)", text):
            parsed = urlsplit(target.strip("<>"))
            if parsed.scheme or parsed.netloc:
                continue
            destination = (page.parent / unquote(parsed.path)).resolve() if parsed.path else page
            require(destination.is_relative_to(ROOT), f"Link escapes repository: {page}: {target}")
            require(destination.exists(), f"Missing link target: {page.relative_to(ROOT)}: {target}")
            if parsed.fragment and destination.suffix == ".md":
                require(unquote(parsed.fragment) in anchors(destination),
                        f"Missing heading target: {page.relative_to(ROOT)}: {target}")
            links += 1
    milestones = (ROOT / "learning/MILESTONES.md").read_text()
    ids = re.findall(r"^### M(\d{2})\s", milestones, re.MULTILINE)
    require(ids == [f"{i:02d}" for i in range(1, 31)], "Milestones must be exactly M01–M30, in order.")
    for match in re.finditer(r"^### M(\d{2})\s.*?(?=^### M|\Z)", milestones, re.MULTILINE | re.DOTALL):
        current = int(match.group(1))
        dependency = re.search(r"\*\*Dependencies and story role:\*\*(.*)", match.group(0))
        require(dependency is not None, f"Missing dependencies in M{current:02d}")
        for earlier in re.findall(r"M(\d{2})", dependency.group(1)):
            require(int(earlier) < current, f"Forward dependency in M{current:02d}: M{earlier}")
    manifest = json.loads((ROOT / "verification/report_manifest.json").read_text())
    for kind in ("source", "pdf"):
        path = ROOT / manifest[kind]
        require(path.is_file(), f"Missing report {kind}")
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        require(actual == manifest[f"{kind}_sha256"], f"Report {kind} hash differs from reviewed manifest.")
    source = (ROOT / manifest["source"]).read_text()
    require("\\input{" not in source and "\\include{" not in source,
            "Report source must remain self-contained.")
    require("\\cite{" not in source and "\\bibliography" not in source,
            "The explanatory report must remain reference-free.")
    require((ROOT / manifest["pdf"]).read_bytes().startswith(b"%PDF-"), "Report is not a PDF.")
    print(f"PASS: {len(pages)} Markdown pages, {links} local links, M01–M30 and backward dependencies")
    print("PASS: reviewed explanatory report PDF/source hashes and self-contained source")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

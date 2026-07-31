from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def extract(pattern: str, text: str, label: str) -> str:
    match = re.search(pattern, text, re.MULTILINE)
    if not match:
        raise RuntimeError(f"Version introuvable dans {label}")
    return match.group(1)


version = read("VERSION").strip()
checks = {
    "app.py": extract(r'^APP_VERSION\s*=\s*["\']([^"\']+)["\']', read("app.py"), "app.py"),
    "pyproject.toml": extract(r'^version\s*=\s*"([^"]+)"', read("pyproject.toml"), "pyproject.toml"),
    "installer/2Webp.iss": extract(r'^\s*#define MyAppVersion "([^"]+)"', read("installer/2Webp.iss"), "installer/2Webp.iss"),
}

errors = [
    f"{path}: {value} != {version}"
    for path, value in checks.items()
    if value != version
]

if errors:
    print("ERREUR: versions incohérentes", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    raise SystemExit(1)

print(f"OK: version {version} cohérente dans {len(checks) + 1} sources")

#!/usr/bin/env python3
"""Build a decision-oriented repository packet without reading source contents."""
from __future__ import annotations

import argparse
import fnmatch
import re
import subprocess
from pathlib import Path

EXCLUDED_DIRS = {".git", "node_modules", "dist", "build", ".next", "coverage", "vendor", "__pycache__"}
MANIFESTS = {
    "package.json", "pnpm-workspace.yaml", "turbo.json", "pyproject.toml",
    "requirements.txt", "go.mod", "Cargo.toml", "composer.json", "Gemfile",
    "Dockerfile", "docker-compose.yml", "docker-compose.yaml", ".env.example",
    "README.md", "openapi.yaml", "openapi.yml", "schema.prisma",
}
SOURCE_EXTS = {".ts", ".tsx", ".js", ".jsx", ".py", ".go", ".rs", ".java", ".rb", ".php", ".sql", ".graphql"}
TEST_MARKERS = ("test", "spec", "__tests__", "e2e", "integration")


def git_files(root: Path) -> list[Path] | None:
    try:
        result = subprocess.run(
            ["git", "-C", str(root), "ls-files", "-co", "--exclude-standard"],
            text=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, check=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return None
    return [root / line for line in result.stdout.splitlines() if line]


def fallback_files(root: Path) -> list[Path]:
    return [p for p in root.rglob("*") if p.is_file() and not any(part in EXCLUDED_DIRS for part in p.relative_to(root).parts)]


def ignored(path: Path, root: Path) -> bool:
    rel = path.relative_to(root)
    return any(part in EXCLUDED_DIRS or fnmatch.fnmatch(part, "*.min.js") or fnmatch.fnmatch(part, "*.map") for part in rel.parts)


def query_terms(query: str) -> set[str]:
    return {x for x in re.findall(r"[a-zA-Z0-9_/-]{2,}", query.lower()) if x not in {"para", "desde", "con", "the", "and"}}


def category(path: Path) -> str:
    name = path.name.lower()
    rel = str(path).lower()
    if path.name in MANIFESTS:
        return "manifiesto"
    if any(marker in rel for marker in TEST_MARKERS):
        return "prueba"
    if path.suffix.lower() in SOURCE_EXTS:
        return "código"
    if path.suffix.lower() in {".yml", ".yaml", ".json", ".toml", ".env"}:
        return "configuración"
    return "otro"


def score(path: Path, root: Path, terms: set[str]) -> int:
    rel = str(path.relative_to(root)).lower()
    value = {"manifiesto": 50, "prueba": 24, "configuración": 18, "código": 12, "otro": 0}[category(path)]
    value += sum(20 for term in terms if term in rel)
    value -= min(len(path.relative_to(root).parts), 8)
    return value


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    parser.add_argument("--query", required=True, help="Resultado o decisión que se necesita resolver")
    parser.add_argument("--limit", type=int, default=24)
    args = parser.parse_args()

    root = Path(args.root).resolve()
    paths = git_files(root) or fallback_files(root)
    paths = [p for p in paths if p.is_file() and not ignored(p, root)]
    terms = query_terms(args.query)
    ranked = sorted(paths, key=lambda p: (-score(p, root, terms), str(p)))[: max(args.limit, 1)]

    print(f"RESULTADO: {args.query}")
    print(f"RAÍZ: {root}")
    print(f"ARCHIVOS_ELEGIBLES: {len(paths)}")
    print(f"TÉRMINOS: {', '.join(sorted(terms)) or 'ninguno'}")
    print("EVIDENCIA_CANDIDATA:")
    for path in ranked:
        rel = path.relative_to(root)
        print(f"- [{category(path)}] {rel}")
    print("SIGUIENTE_DECISIÓN: elige solo los candidatos que puedan cambiar la decisión actual; abre símbolos o rangos antes que archivos completos.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

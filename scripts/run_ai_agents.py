from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
APP_DIR = ROOT_DIR / "5-Search-AI-Workloads-Agents-and-RAG" / "mobile-agents"
ENV_FILE = ROOT_DIR / ".env"


def main() -> None:
    if not APP_DIR.exists():
        raise SystemExit(f"AI agents app folder not found: {APP_DIR}")
    if not ENV_FILE.exists():
        raise SystemExit(f"Environment file not found: {ENV_FILE}")

    print(f"Starting AI agents app from: {APP_DIR}")
    print(f"Using environment file: {ENV_FILE}")

    completed = subprocess.run([sys.executable, "app.py"], cwd=APP_DIR, check=False)
    if completed.returncode:
        raise SystemExit(completed.returncode)


if __name__ == "__main__":
    main()

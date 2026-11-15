#!/usr/bin/env python3

import shutil
import subprocess
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent / "unrwalkingmapWebsite"

DIST_DIR = PROJECT_DIR / "dist"
NGINX_ROOT = Path("/var/www/html")


def run(cmd):
    print("\nCommand:")
    print(" ".join(map(str, cmd)))
    subprocess.run(cmd, check=True)


def main():
    if not DIST_DIR.exists():
        raise FileNotFoundError(
            f"Missing build output: {DIST_DIR}"
        )

    for item in NGINX_ROOT.iterdir():
        if item.is_dir():
            shutil.rmtree(item)
        else:
            item.unlink()

    shutil.copytree(
        DIST_DIR,
        NGINX_ROOT,
        dirs_exist_ok=True
    )

    run([
        "systemctl",
        "restart",
        "nginx"
    ])

    

    print("\nDeployment complete.")


if __name__ == "__main__":
    main()
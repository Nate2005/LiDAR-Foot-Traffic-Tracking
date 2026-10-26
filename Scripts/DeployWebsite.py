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
    print(f"Project Directory: {PROJECT_DIR}")

    # Build website
    run(["npm", "install"], cwd=PROJECT_DIR)
    run(["npm", "run", "build"], cwd=PROJECT_DIR)

    if not DIST_DIR.exists():
        raise FileNotFoundError(
            f"Build succeeded but {DIST_DIR} does not exist."
        )

    # Clear nginx folder
    for item in NGINX_ROOT.iterdir():
        if item.is_dir():
            shutil.rmtree(item)
        else:
            item.unlink()

    # Copy website
    shutil.copytree(
        DIST_DIR,
        NGINX_ROOT,
        dirs_exist_ok=True
    )

    # Copy MapLibre worker
    worker_source = (
        PROJECT_DIR /
        "public" /
        "maplibre-gl-worker.mjs"
    )

    worker_dest = (
        NGINX_ROOT /
        "maplibre-gl-worker.js"
    )

    if not worker_source.exists():
        raise FileNotFoundError(
            f"Missing worker file: {worker_source}"
        )

    shutil.copy2(
        worker_source,
        worker_dest
    )

    # Reload nginx
    run([
        "sudo",
        "systemctl",
        "reload",
        "nginx"
    ])

    # Reload nginx
    run([
        "sudo",
        "systemctl",
        "reload",
        "nginx"
    ])

    print("\nDeployment complete.")


def run(cmd, cwd=None):
    print("\nCommand:")
    print(" ".join(map(str, cmd)))
    subprocess.run(cmd, check=True, cwd=cwd)


if __name__ == "__main__":
    main()
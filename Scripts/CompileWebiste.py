#!/usr/bin/env python3

import shutil
import subprocess
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent / "unrwalkingmapWebsite"

DIST_DIR = PROJECT_DIR / "dist"
NGINX_ROOT = Path("/var/www/capstone")


def run(cmd, cwd=None):
    print("\nCommand:")
    print(" ".join(map(str, cmd)))
    subprocess.run(cmd, check=True, cwd=cwd)


def main():
    print(f"Project Directory: {PROJECT_DIR}")

    # Clean build
    if DIST_DIR.exists():
        shutil.rmtree(DIST_DIR)

    # Build as normal user
    run(["npm", "install"], cwd=PROJECT_DIR)
    run(["npm", "run", "build"], cwd=PROJECT_DIR)

    if not DIST_DIR.exists():
        raise FileNotFoundError(
            f"Build succeeded but {DIST_DIR} does not exist."
        )

    print("\nBuild complete.")

    print("\nNow deploy with:")
    print(
        "sudo python3 DeployBuiltWebsite.py"
    )


if __name__ == "__main__":
    main()
import shutil
import subprocess
import sys
from pathlib import Path


# Paths
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent
CONFIG_DIR = PROJECT_DIR / "Configs"
OUT_DIR = PROJECT_DIR / "Out"
OUT_DIR.mkdir(exist_ok=True)


# Constants
NEVADA_PBF_URL = (
    "https://download.geofabrik.de/"
    "north-america/us/nevada-latest.osm.pbf"
)

APT_PACKAGES = {
    "wget": "wget",
    "osmium": "osmium-tool",
    "tilemaker": "tilemaker"
}

PMTILES_VERSION = "1.31.2"

# Helpers


def Run(cmd):
    """Execute a command and stop if it fails."""

    print("\nCommand:")
    print(" ".join(map(str, cmd)))

    subprocess.run(cmd, check=True)


# Nevada Extract



def DownloadNevadaExtract():
    """Download the Nevada extract if not already present."""


    output_file = OUT_DIR / "nevada-latest.osm.pbf"

    if output_file.exists():
        print("Nevada extract already present.")
        return

    Run([
        "wget",
        "-O",
        str(output_file),
        NEVADA_PBF_URL
    ])

    print(f"Downloaded {output_file}")


# Apt Packages


def InstallAptPackages():
    """Install missing apt packages."""

    missing_packages = []

    for command, package in APT_PACKAGES.items():
        if shutil.which(command) is None:
            missing_packages.append(package)

    if not missing_packages:
        print("All apt packages already installed.")
        return

    Run([
        "sudo",
        "apt-get",
        "update"
    ])

    Run([
        "sudo",
        "apt-get",
        "install",
        "-y",
        *missing_packages
    ])


# PMTiles


def InstallPMTiles():
    """Install PMTiles CLI."""

    pmtiles_path = Path("/usr/local/bin/pmtiles")

    if pmtiles_path.exists():
        print("PMTiles already installed.")
        return

    archive = (
        f"go-pmtiles_{PMTILES_VERSION}_Linux_x86_64.tar.gz"
    )

    url = (
        f"https://github.com/protomaps/go-pmtiles/"
        f"releases/download/v{PMTILES_VERSION}/"
        f"{archive}"
    )

    archive_path = SCRIPT_DIR / archive

    Run([
        "wget",
        "-O",
        str(archive_path),
        url
    ])

    Run([
        "tar",
        "-xzf",
        str(archive_path)
    ])

    binary = SCRIPT_DIR / "pmtiles"

    if not binary.exists():
        binary = SCRIPT_DIR / "go-pmtiles"

    if not binary.exists():
        print("Unable to locate extracted PMTiles binary.")
        sys.exit(1)

    Run([
        "sudo",
        "mv",
        str(binary),
        str(pmtiles_path)
    ])

    Run([
        "sudo",
        "chmod",
        "+x",
        str(pmtiles_path)
    ])

    Run([
        str(pmtiles_path),
        "version"
    ])

    archive_path.unlink(missing_ok=True)

    for file in [
        SCRIPT_DIR / "LICENSE",
        SCRIPT_DIR / "README.md",
    ]:
        file.unlink(missing_ok=True)
    
    for file in SCRIPT_DIR.glob(
        "go-pmtiles*.tar.gz"
        ):
        file.unlink(missing_ok=True)
    
    print("PMTiles installed successfully.")

# Verification



def VerifyInstall():
    """Verify commands and required files."""

    required_commands = [
        "wget",
        "osmium",
        "tilemaker",
    ]

    required_files = [
        CONFIG_DIR / "config-unr.json",
        CONFIG_DIR / "process.lua"
    ]

    missing = []

    for command in required_commands:
        if shutil.which(command) is None:
            missing.append(command)

    for file_path in required_files:
        if not file_path.exists():
            missing.append(str(file_path))

    if missing:
        print("\nMissing items:")

        for item in missing:
            print(f"  - {item}")

        return False

    print("\nAll dependencies installed successfully.")

    return True



# Main


def main():
    """Install dependencies and verify setup."""

    print(f"Project Directory: {PROJECT_DIR}")

    if shutil.which("apt-get") is None:
        print("Error: apt-get not found.")
        sys.exit(1)

    if shutil.which("sudo") is None:
        print("Error: sudo not found.")
        sys.exit(1)

    try:
        InstallAptPackages()

        InstallPMTiles()

        DownloadNevadaExtract()

        if not VerifyInstall():
            sys.exit(1)

        print("\nSetup complete.")

    except subprocess.CalledProcessError as e:
        print(
            f"\nCommand failed with exit code "
            f"{e.returncode}"
        )
        sys.exit(e.returncode)


if __name__ == "__main__":
    main()
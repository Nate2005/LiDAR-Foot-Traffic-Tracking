import shutil
import subprocess
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent

CONFIG_DIR = PROJECT_DIR / "Configs"
OUT_DIR = PROJECT_DIR / "Out"

OUT_DIR.mkdir(exist_ok=True)

def FindNevadaPBF():
    """Finds the current Nevada State map file"""
    matches = list(
        OUT_DIR.glob("nevada-*.osm.pbf")
    )

    if not matches:
        return None

    return str(max(matches, key=lambda p: p.stat().st_mtime))


def CheckPMTiles():
    """ checks to see what pmtiles gets installed"""
    return (
        shutil.which("pmtiles") is not None or
        shutil.which("go-pmtiles") is not None
    )


def CheckPackages():
    """Checks what packages are installed on the system and marks what missing packages are there
    Note that it also checks to see if the config files are there"""
    required_commands = [
        "wget",
        "osmium",
        "tilemaker"
    ]

    missing = []

    for command in required_commands:
        if shutil.which(command) is None:
            missing.append(command)

    if not CheckPMTiles():
        missing.append("pmtiles")

    CONFIG_DIR = Path("../Configs")
    
    if not (CONFIG_DIR / "config-unr.json").exists():
     missing.append("Configs/config-unr.json")
    
    if not (CONFIG_DIR / "process.lua").exists():
     missing.append("Configs/process.lua")

    if not missing:
        return True

    print("Missing prerequisites:")

    for item in missing:
        print(f"  - {item}")

    return False

def RunAndShowCommand(cmd):
    
    """Runs a command and also displays it"""
    
    print("\nCommand:")
    print(" ".join(cmd))
    subprocess.run(cmd, check=True)


def ConvertNevadaStateFiletoUNRFile(input_pbf):
    output_pbf = OUT_DIR / "unr.osm.pbf"

    bbox = "-119.83,39.53,-119.80,39.56"

    cmd = [
        "osmium",
        "extract",
        "-b",
        bbox,
        "-o",
        str(output_pbf),
        input_pbf
    ]

    RunAndShowCommand(cmd)

    return str(output_pbf)



def GenerateMBTiles(input_pbf):

    mbtiles_file = OUT_DIR / "unr.mbtiles"

    config_file = CONFIG_DIR / "config-unr.json"
    process_file = CONFIG_DIR / "process.lua"

    cmd = [
        "tilemaker",
        "--input",
        input_pbf,
        "--output",
        str(mbtiles_file),
        "--config",
        str(config_file),
        "--process",
        str(process_file),
        "--bbox",
        "-119.83,39.53,-119.80,39.56"
    ]

    RunAndShowCommand(cmd)

    return str(mbtiles_file)

def ConvertMBToPMTiles(mbtiles_file):

    pmtiles_file = OUT_DIR / "unr.pmtiles"

    pmtiles_cmd = (
        "pmtiles"
        if shutil.which("pmtiles")
        else "go-pmtiles"
    )

    cmd = [
        pmtiles_cmd,
        "convert",
        mbtiles_file,
        str(pmtiles_file)
    ]

    RunAndShowCommand(cmd)

    print(f"\nCreated {pmtiles_file}")

    return str(pmtiles_file)

def MovePMTilesToSitePublicDir(pmtiles_file):

    """ Move the pmtiles to the public dir folder of the site"""

    destination = (
        PROJECT_DIR /
        "unrwalkingmapWebsite" /
        "public" /
        "unr.pmtiles"
    )

    shutil.copy2(
        pmtiles_file,
        destination
    )

    print(
        f"Copied {pmtiles_file} "
        f"to {destination}"
    )


def main():
    """Main Method where it first deletes existing files,
    
    Check to see any packages are there, 
    
    and then find the nevada state file, 
    
    If found, it converts the nevada state map into a map of unr
    
    Then Generates the MBtiles of unr
    
    Then converts the mbtiles of unr into pmtiles
    
    """

    for file in [
         OUT_DIR / "unr.osm.pbf",
         OUT_DIR / "unr.mbtiles",
         OUT_DIR / "unr.pmtiles"
     ]:  
         path = Path(file)

         if path.exists():
             print(f"Removing {path}")
             path.unlink()

    if not CheckPackages():
        print(
            "\nPlease install depenencies from the readme with sudo/root privileges "
            "and then rerun this script.\n"
        )
        return

    input_pbf = FindNevadaPBF()

    if input_pbf is None:
        print(
            "\nNo file matching nevada-*.osm.pbf was found.\n"
        )
        return

    print(f"Using Nevada extract: {Path(input_pbf).name}")

    unr_pbf = ConvertNevadaStateFiletoUNRFile(input_pbf)
    mbtiles = GenerateMBTiles(unr_pbf)
    pmtiles_file = ConvertMBToPMTiles(mbtiles)

    MovePMTilesToSitePublicDir(pmtiles_file)

    print(f"\nFinal output: {pmtiles_file} and moved to website folder")


    


if __name__ == "__main__":
    main()
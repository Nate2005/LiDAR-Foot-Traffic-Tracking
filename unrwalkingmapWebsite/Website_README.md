
# UNR Walking Map Website

## Repository Layout

- unrwalkingmapWebsite/
    - Configs/
    - Scripts/
    - Out/ 

## Software Requirements

### System Requirements

Install the following packages from the Linux distribution's repositories:

```text
Python >= 3.12
wget >= 1.25
osmium-tool >= 1.19.1
tilemaker >= 3.2
pmtiles >= 1.31
nginx >= 1.30

npm >= 11.x
Node.js >= 24.x

systemd/systemctl
```

### Website Dependencies

All website dependencies are defined in:
- package.json
- package-lock.json


Install them with:
```text
cd unrwalkingmapWebsite
npm install
```

### Note

The website public directory is intentionally kept empty in the repository.

Required runtime assets, including:
 
- unr.pmtiles
- fonts/
- maplibre-gl-worker.mjs
- favicon.svg

must be generated or downloaded separately and placed in:

```text 
unrwalkingmapWebsite/public/
```

before building the website.



## Required Map Data

The map-generation scripts require a Nevada OpenStreetMap extract from Geofabrik:

https://download.geofabrik.de/north-america/us/nevada.html

Download the Nevada .osm.pbf file and place it inside the project's Out directory.

The scripts expect a file matching:

- nevada-*.osm.pbf

Put into Out folder

### Font Assets

The website requires glyph assets in:

```text
unrwalkingmapWebsite/public/fonts/
```

These assets are based on the OpenMapTiles Open Font Glyphs project:

https://github.com/openmaptiles/fonts

The map style uses:

```text
Open Sans Regular
```
Required files include:

- OpenSans-Regular.ttf
- Generated glyph PBF files in:

```text
public/fonts/_output/
```

If the glyphs are not already present, generate them with:

```text
cd unrwalkingmapWebsite/public/fonts
npm install
node generate.js
```

The generated glyphs  files will be written to:

```text
public/fonts/_output/
```

These files are copied automatically into the final website build by Vite.


### Additional Runtime Assets

Download the MapLibre GL JS worker file:

- maplibre-gl-worker.mjs

from the MapLibre GL JS project:

https://github.com/maplibre/maplibre-gl-js

and place it in:

```text
unrwalkingmapWebsite/public/
```

Ensure that .mjs files are served with the MIME type:

application/javascript


## Generate Map Tiles

Run:

```text
python3 Scripts/CreateMapTiles.py
```

This generates:
```text
Out/unr.osm.pbf
Out/unr.mbtiles
Out/unr.pmtiles
```

and copies:

```text
unr.pmtiles
```

to:
```text
unrwalkingmapWebsite/public/
```
## Build Site

Run:
```text
cd unrwalkingmapWebsite
npm install
npm run build
```

This creates:
```text
unrwalkingmapWebsite/dist
```


## Deploy Site
DeployWebsite.py requires sudo to:

- Write to /var/www/html
- Reload the nginx service


Run:
```text
sudo python3 Scripts/DeployWebsite.py
```

This:
- Copies the contents of unrwalkingmapWebsite/dist
- Deploys the site to /var/www/html
- Reloads Nginx
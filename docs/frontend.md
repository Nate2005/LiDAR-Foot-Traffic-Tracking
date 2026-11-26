
# UNR Walking Map Website

## Repository Layout

- frontend/                    Vue + Vite site
- map/
    - config/                    tilemaker config
    - scripts/create_map_tiles.py
    - out/                       generated tiles
- deploy/scripts/                build_frontend.py, deploy_frontend.py

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
cd frontend
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
frontend/public/
```

before building the website.



## Required Map Data

The map-generation scripts require a Nevada OpenStreetMap extract from Geofabrik:

https://download.geofabrik.de/north-america/us/nevada.html

Download the Nevada .osm.pbf file and place it inside the map/out/ directory.

The scripts expect a file matching:

- nevada-*.osm.pbf

Put into map/out/

### Font Assets

The website requires glyph assets in:

```text
frontend/public/fonts/
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
cd frontend/public/fonts
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
frontend/public/
```

Ensure that .mjs files are served with the MIME type:

application/javascript


## Generate Map Tiles

Run:

```text
python3 map/scripts/create_map_tiles.py
```

This generates:
```text
map/out/unr.osm.pbf
map/out/unr.mbtiles
map/out/unr.pmtiles
```

and copies:

```text
unr.pmtiles
```

to:
```text
frontend/public/
```
## Build Site

Run:
```text
cd frontend
npm install
npm run build
```

This creates:
```text
frontend/dist
```


## Deploy Site
deploy_frontend.py requires sudo to:

- Write to /var/www/html
- Reload the nginx service


Run:
```text
sudo python3 deploy/scripts/deploy_frontend.py
```

This:
- Copies the contents of frontend/dist
- Deploys the site to /var/www/html
- Reloads Nginx
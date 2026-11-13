// style-unr.ts

import type { StyleSpecification } from 'maplibre-gl'

const style: StyleSpecification = {
  version: 8,
  name: 'UNR MapLibre',
  metadata: {
    'maputnik:renderer': 'mlgljs',
    description: 'MapLibre style for the Tilemaker/OpenMapTiles layers'
  },
  center: [-119.815, 39.545],
  zoom: 13,
  "glyphs": "/fonts/_output/{fontstack}/{range}.pbf",

  sources: {
    unr: {
      type: 'vector',
      url: 'pmtiles://unr.pmtiles',
      minzoom: 0,
      maxzoom: 14
    }
  },

  layers: [
    // paste all layers here
    /////



    {
      "id": "background",
      "type": "background",
      "paint": {
        "background-color": "#f4f1ea"
      }
    },
    {
      "id": "landcover-wood",
      "type": "fill",
      "source": "unr",
      "source-layer": "landcover",
      "filter": [
        "==",
        [
          "get",
          "class"
        ],
        "wood"
      ],
      "paint": {
        "fill-color": "#b8d3aa",
        "fill-opacity": 0.72
      }
    },
    {
      "id": "landcover-grass",
      "type": "fill",
      "source": "unr",
      "source-layer": "landcover",
      "filter": [
        "==",
        [
          "get",
          "class"
        ],
        "grass"
      ],
      "paint": {
        "fill-color": "#cfe3b4",
        "fill-opacity": 0.72
      }
    },
    {
      "id": "landcover-farmland",
      "type": "fill",
      "source": "unr",
      "source-layer": "landcover",
      "filter": [
        "==",
        [
          "get",
          "class"
        ],
        "farmland"
      ],
      "paint": {
        "fill-color": "#e7dfb2",
        "fill-opacity": 0.72
      }
    },
    {
      "id": "landcover-sand",
      "type": "fill",
      "source": "unr",
      "source-layer": "landcover",
      "filter": [
        "==",
        [
          "get",
          "class"
        ],
        "sand"
      ],
      "paint": {
        "fill-color": "#f2e2b8",
        "fill-opacity": 0.72
      }
    },
    {
      "id": "landcover-wetland",
      "type": "fill",
      "source": "unr",
      "source-layer": "landcover",
      "filter": [
        "==",
        [
          "get",
          "class"
        ],
        "wetland"
      ],
      "paint": {
        "fill-color": "#b9d8c5",
        "fill-opacity": 0.72
      }
    },
    {
      "id": "landcover-ice",
      "type": "fill",
      "source": "unr",
      "source-layer": "landcover",
      "filter": [
        "==",
        [
          "get",
          "class"
        ],
        "ice"
      ],
      "paint": {
        "fill-color": "#e8f5fa",
        "fill-opacity": 0.72
      }
    },
    {
      "id": "landuse-residential",
      "type": "fill",
      "source": "unr",
      "source-layer": "landuse",
      "minzoom": 4,
      "filter": [
        "==",
        [
          "get",
          "class"
        ],
        "residential"
      ],
      "paint": {
        "fill-color": "#ddd9d2",
        "fill-opacity": 0.65
      }
    },
    {
      "id": "landuse-commercial",
      "type": "fill",
      "source": "unr",
      "source-layer": "landuse",
      "minzoom": 4,
      "filter": [
        "==",
        [
          "get",
          "class"
        ],
        "commercial"
      ],
      "paint": {
        "fill-color": "#ead6d0",
        "fill-opacity": 0.65
      }
    },
    {
      "id": "landuse-retail",
      "type": "fill",
      "source": "unr",
      "source-layer": "landuse",
      "minzoom": 4,
      "filter": [
        "==",
        [
          "get",
          "class"
        ],
        "retail"
      ],
      "paint": {
        "fill-color": "#ead5cc",
        "fill-opacity": 0.65
      }
    },
    {
      "id": "landuse-industrial",
      "type": "fill",
      "source": "unr",
      "source-layer": "landuse",
      "minzoom": 4,
      "filter": [
        "==",
        [
          "get",
          "class"
        ],
        "industrial"
      ],
      "paint": {
        "fill-color": "#d8d3cf",
        "fill-opacity": 0.65
      }
    },
    {
      "id": "landuse-school",
      "type": "fill",
      "source": "unr",
      "source-layer": "landuse",
      "minzoom": 4,
      "filter": [
        "==",
        [
          "get",
          "class"
        ],
        "school"
      ],
      "paint": {
        "fill-color": "#e7dfbf",
        "fill-opacity": 0.65
      }
    },
    {
      "id": "landuse-university",
      "type": "fill",
      "source": "unr",
      "source-layer": "landuse",
      "minzoom": 4,
      "filter": [
        "==",
        [
          "get",
          "class"
        ],
        "university"
      ],
      "paint": {
        "fill-color": "#dfddba",
        "fill-opacity": 0.65
      }
    },
    {
      "id": "landuse-stadium",
      "type": "fill",
      "source": "unr",
      "source-layer": "landuse",
      "minzoom": 4,
      "filter": [
        "==",
        ["get", "class"],
        "stadium"
      ],
      "paint": {
        "fill-color": "#d8ccb3",
        "fill-opacity": 0.75
      }
    },

    {
      "id": "landuse-pitch",
      "type": "fill",
      "source": "unr",
      "source-layer": "landuse",
      "minzoom": 4,
      "filter": [
        "==",
        ["get", "class"],
        "pitch"
      ],
      "paint": {
        "fill-color": "#b9d8aa",
        "fill-opacity": 0.75
      }
    }

    ,
    {
      "id": "landuse-hospital",
      "type": "fill",
      "source": "unr",
      "source-layer": "landuse",
      "minzoom": 4,
      "filter": [
        "==",
        [
          "get",
          "class"
        ],
        "hospital"
      ],
      "paint": {
        "fill-color": "#ead0d0",
        "fill-opacity": 0.65
      }
    },
    {
      "id": "landuse-cemetery",
      "type": "fill",
      "source": "unr",
      "source-layer": "landuse",
      "minzoom": 4,
      "filter": [
        "==",
        [
          "get",
          "class"
        ],
        "cemetery"
      ],
      "paint": {
        "fill-color": "#c8dbc2",
        "fill-opacity": 0.65
      }
    },
    {
      "id": "landuse-military",
      "type": "fill",
      "source": "unr",
      "source-layer": "landuse",
      "minzoom": 4,
      "filter": [
        "==",
        [
          "get",
          "class"
        ],
        "military"
      ],
      "paint": {
        "fill-color": "#e4c7c0",
        "fill-opacity": 0.65
      }
    },
    {
      "id": "park",
      "type": "fill",
      "source": "unr",
      "source-layer": "park",
      "minzoom": 11,
      "paint": {
        "fill-color": "#b9d8aa",
        "fill-opacity": 0.78
      }
    },
    {
      "id": "water",
      "type": "fill",
      "source": "unr",
      "source-layer": "water",
      "minzoom": 6,
      "paint": {
        "fill-color": "#9dcde3"
      }
    },
    {
      "id": "waterway",
      "type": "line",
      "source": "unr",
      "source-layer": "waterway",
      "minzoom": 8,
      "paint": {
        "line-color": "#71b4d2",
        "line-width": [
          "interpolate",
          [
            "linear"
          ],
          [
            "zoom"
          ],
          8,
          0.6,
          14,
          2.2
        ]
      }
    },
    {
      "id": "boundary",
      "type": "line",
      "source": "unr",
      "source-layer": "boundary",
      "minzoom": 0,
      "paint": {
        "line-color": "#9b8f86",
        "line-width": [
          "interpolate",
          [
            "linear"
          ],
          [
            "zoom"
          ],
          4,
          0.5,
          14,
          1.5
        ],
        "line-dasharray": [
          3,
          2
        ],
        "line-opacity": 0.7
      }
    },
    {
      "id": "aeroway-area",
      "type": "fill",
      "source": "unr",
      "source-layer": "aeroway",
      "minzoom": 11,
      "filter": [
        "==",
        [
          "geometry-type"
        ],
        "Polygon"
      ],
      "paint": {
        "fill-color": "#d9d9dc",
        "fill-opacity": 0.8
      }
    },
    {
      "id": "aeroway-line",
      "type": "line",
      "source": "unr",
      "source-layer": "aeroway",
      "minzoom": 11,
      "filter": [
        "==",
        [
          "geometry-type"
        ],
        "LineString"
      ],
      "paint": {
        "line-color": "#b8b8bd",
        "line-width": [
          "interpolate",
          [
            "linear"
          ],
          [
            "zoom"
          ],
          11,
          2,
          14,
          8
        ]
      }
    },
    {
      "id": "road-motorway-casing",
      "type": "line",
      "source": "unr",
      "source-layer": "transportation",
      "minzoom": 4,
      "filter": [
        "==",
        [
          "get",
          "class"
        ],
        "motorway"
      ],
      "layout": {
        "line-cap": "round",
        "line-join": "round"
      },
      "paint": {
        "line-color": "#c5bdb3",
        "line-width": [
          "interpolate",
          [
            "linear"
          ],
          [
            "zoom"
          ],
          4,
          3.5,
          16,
          7.5
        ]
      }
    },
    {
      "id": "road-motorway",
      "type": "line",
      "source": "unr",
      "source-layer": "transportation",
      "minzoom": 4,
      "filter": [
        "==",
        [
          "get",
          "class"
        ],
        "motorway"
      ],
      "layout": {
        "line-cap": "round",
        "line-join": "round"
      },
      "paint": {
        "line-color": "#e89273",
        "line-width": [
          "interpolate",
          [
            "linear"
          ],
          [
            "zoom"
          ],
          4,
          3.0,
          16,
          5.5
        ]
      }
    },
    {
      "id": "road-trunk-casing",
      "type": "line",
      "source": "unr",
      "source-layer": "transportation",
      "minzoom": 5,
      "filter": [
        "==",
        [
          "get",
          "class"
        ],
        "trunk"
      ],
      "layout": {
        "line-cap": "round",
        "line-join": "round"
      },
      "paint": {
        "line-color": "#c5bdb3",
        "line-width": [
          "interpolate",
          [
            "linear"
          ],
          [
            "zoom"
          ],
          5,
          3,
          16,
          7
        ]
      }
    },
    {
      "id": "road-trunk",
      "type": "line",
      "source": "unr",
      "source-layer": "transportation",
      "minzoom": 5,
      "filter": [
        "==",
        [
          "get",
          "class"
        ],
        "trunk"
      ],
      "layout": {
        "line-cap": "round",
        "line-join": "round"
      },
      "paint": {
        "line-color": "#e9a979",
        "line-width": [
          "interpolate",
          [
            "linear"
          ],
          [
            "zoom"
          ],
          5,
          2.5,
          16,
          5
        ]
      }
    },
    {
      "id": "road-primary-casing",
      "type": "line",
      "source": "unr",
      "source-layer": "transportation",
      "minzoom": 7,
      "filter": [
        "==",
        [
          "get",
          "class"
        ],
        "primary"
      ],
      "layout": {
        "line-cap": "round",
        "line-join": "round"
      },
      "paint": {
        "line-color": "#c5bdb3",
        "line-width": [
          "interpolate",
          [
            "linear"
          ],
          [
            "zoom"
          ],
          7,
          2.3,
          16,
          6.3
        ]
      }
    },
    {
      "id": "road-primary",
      "type": "line",
      "source": "unr",
      "source-layer": "transportation",
      "minzoom": 7,
      "filter": [
        "==",
        [
          "get",
          "class"
        ],
        "primary"
      ],
      "layout": {
        "line-cap": "round",
        "line-join": "round"
      },
      "paint": {
        "line-color": "#efc078",
        "line-width": [
          "interpolate",
          [
            "linear"
          ],
          [
            "zoom"
          ],
          7,
          1.7999999999999998,
          16,
          4.3
        ]
      }
    },
    {
      "id": "road-secondary-casing",
      "type": "line",
      "source": "unr",
      "source-layer": "transportation",
      "minzoom": 9,
      "filter": [
        "==",
        [
          "get",
          "class"
        ],
        "secondary"
      ],
      "layout": {
        "line-cap": "round",
        "line-join": "round"
      },
      "paint": {
        "line-color": "#c5bdb3",
        "line-width": [
          "interpolate",
          [
            "linear"
          ],
          [
            "zoom"
          ],
          9,
          1.7999999999999998,
          16,
          5.8
        ]
      }
    },
    {
      "id": "road-secondary",
      "type": "line",
      "source": "unr",
      "source-layer": "transportation",
      "minzoom": 9,
      "filter": [
        "==",
        [
          "get",
          "class"
        ],
        "secondary"
      ],
      "layout": {
        "line-cap": "round",
        "line-join": "round"
      },
      "paint": {
        "line-color": "#f3d69a",
        "line-width": [
          "interpolate",
          [
            "linear"
          ],
          [
            "zoom"
          ],
          9,
          1.2999999999999998,
          16,
          3.8
        ]
      }
    },
    {
      "id": "road-tertiary-casing",
      "type": "line",
      "source": "unr",
      "source-layer": "transportation",
      "minzoom": 11,
      "filter": [
        "==",
        [
          "get",
          "class"
        ],
        "tertiary"
      ],
      "layout": {
        "line-cap": "round",
        "line-join": "round"
      },
      "paint": {
        "line-color": "#c5bdb3",
        "line-width": [
          "interpolate",
          [
            "linear"
          ],
          [
            "zoom"
          ],
          11,
          1.2000000000000002,
          16,
          5.2
        ]
      }
    },
    {
      "id": "road-tertiary",
      "type": "line",
      "source": "unr",
      "source-layer": "transportation",
      "minzoom": 11,
      "filter": [
        "==",
        [
          "get",
          "class"
        ],
        "tertiary"
      ],
      "layout": {
        "line-cap": "round",
        "line-join": "round"
      },
      "paint": {
        "line-color": "#f8e7bd",
        "line-width": [
          "interpolate",
          [
            "linear"
          ],
          [
            "zoom"
          ],
          11,
          0.7000000000000002,
          16,
          3.2
        ]
      }
    },
    {
      "id": "road-minor-casing",
      "type": "line",
      "source": "unr",
      "source-layer": "transportation",
      "minzoom": 12,
      "filter": [
        "==",
        [
          "get",
          "class"
        ],
        "minor"
      ],
      "layout": {
        "line-cap": "round",
        "line-join": "round"
      },
      "paint": {
        "line-color": "#c5bdb3",
        "line-width": [
          "interpolate",
          [
            "linear"
          ],
          [
            "zoom"
          ],
          12,
          0.6000000000000001,
          16,
          4.6
        ]
      }
    },
    {
      "id": "road-minor",
      "type": "line",
      "source": "unr",
      "source-layer": "transportation",
      "minzoom": 12,
      "filter": [
        "==",
        [
          "get",
          "class"
        ],
        "minor"
      ],
      "layout": {
        "line-cap": "round",
        "line-join": "round"
      },
      "paint": {
        "line-color": "#ffffff",
        "line-width": [
          "interpolate",
          [
            "linear"
          ],
          [
            "zoom"
          ],
          12,
          0.4,
          16,
          2.6
        ]
      }
    },
    {
      "id": "road-service-casing",
      "type": "line",
      "source": "unr",
      "source-layer": "transportation",
      "minzoom": 12,
      "filter": [
        "==",
        [
          "get",
          "class"
        ],
        "service"
      ],
      "layout": {
        "line-cap": "round",
        "line-join": "round"
      },
      "paint": {
        "line-color": "#c5bdb3",
        "line-width": [
          "interpolate",
          [
            "linear"
          ],
          [
            "zoom"
          ],
          12,
          0.5,
          16,
          3.8
        ]
      }
    },
    {
      "id": "road-service",
      "type": "line",
      "source": "unr",
      "source-layer": "transportation",
      "minzoom": 12,
      "filter": [
        "==",
        [
          "get",
          "class"
        ],
        "service"
      ],
      "layout": {
        "line-cap": "round",
        "line-join": "round"
      },
      "paint": {
        "line-color": "#ffffff",
        "line-width": [
          "interpolate",
          [
            "linear"
          ],
          [
            "zoom"
          ],
          12,
          0.4,
          16,
          1.8
        ]
      }
    },
    {
      "id": "road-track-casing",
      "type": "line",
      "source": "unr",
      "source-layer": "transportation",
      "minzoom": 14,
      "filter": [
        "==",
        [
          "get",
          "class"
        ],
        "track"
      ],
      "layout": {
        "line-cap": "round",
        "line-join": "round"
      },
      "paint": {
        "line-color": "#c5bdb3",
        "line-width": [
          "interpolate",
          [
            "linear"
          ],
          [
            "zoom"
          ],
          14,
          0.5,
          16,
          3.5
        ]
      }
    },
    {
      "id": "road-track",
      "type": "line",
      "source": "unr",
      "source-layer": "transportation",
      "minzoom": 14,
      "filter": [
        "==",
        [
          "get",
          "class"
        ],
        "track"
      ],
      "layout": {
        "line-cap": "round",
        "line-join": "round"
      },
      "paint": {
        "line-color": "#d8c7a6",
        "line-width": [
          "interpolate",
          [
            "linear"
          ],
          [
            "zoom"
          ],
          14,
          0.4,
          16,
          1.5
        ]
      }
    },
    {
      "id": "road-path-casing",
      "type": "line",
      "source": "unr",
      "source-layer": "transportation",
      "minzoom": 14,
      "filter": [
        "==",
        [
          "get",
          "class"
        ],
        "path"
      ],
      "layout": {
        "line-cap": "round",
        "line-join": "round"
      },
      "paint": {
        "line-color": "#c5bdb3",
        "line-width": [
          "interpolate",
          [
            "linear"
          ],
          [
            "zoom"
          ],
          14,
          0.5,
          16,
          3.2
        ]
      }
    },
    {
      "id": "road-path",
      "type": "line",
      "source": "unr",
      "source-layer": "transportation",
      "minzoom": 14,
      "filter": [
        "==",
        [
          "get",
          "class"
        ],
        "path"
      ],
      "layout": {
        "line-cap": "round",
        "line-join": "round"
      },
      "paint": {
        "line-color": "#c2a983",
        "line-width": [
          "interpolate",
          [
            "linear"
          ],
          [
            "zoom"
          ],
          14,
          0.4,
          16,
          1.2
        ]
      }
    },
    {
      "id": "road-rail-casing",
      "type": "line",
      "source": "unr",
      "source-layer": "transportation",
      "minzoom": 9,
      "filter": [
        "==",
        [
          "get",
          "class"
        ],
        "rail"
      ],
      "layout": {
        "line-cap": "round",
        "line-join": "round"
      },
      "paint": {
        "line-color": "#c5bdb3",
        "line-width": [
          "interpolate",
          [
            "linear"
          ],
          [
            "zoom"
          ],
          9,
          0.5,
          16,
          3.3
        ]
      }
    },
    {
      "id": "road-rail",
      "type": "line",
      "source": "unr",
      "source-layer": "transportation",
      "minzoom": 9,
      "filter": [
        "==",
        [
          "get",
          "class"
        ],
        "rail"
      ],
      "layout": {
        "line-cap": "round",
        "line-join": "round"
      },
      "paint": {
        "line-color": "#909090",
        "line-width": [
          "interpolate",
          [
            "linear"
          ],
          [
            "zoom"
          ],
          9,
          0.4,
          16,
          1.3
        ]
      }
    },
    {
      "id": "ferry",
      "type": "line",
      "source": "unr",
      "source-layer": "transportation",
      "minzoom": 9,
      "filter": [
        "==",
        [
          "get",
          "class"
        ],
        "ferry"
      ],
      "paint": {
        "line-color": "#5b9dbc",
        "line-width": 1.2,
        "line-dasharray": [
          2,
          2
        ]
      }
    },
    {
      "id": "building",
      "type": "fill",
      "source": "unr",
      "source-layer": "building",
      "minzoom": 13,
      "paint": {
        "fill-color": "#d2c4b7",
        "fill-outline-color": "#b7a99d",
        "fill-opacity": 0.88
      }
    },
    {
      "id": "road-label",
      "type": "symbol",
      "source": "unr",
      "source-layer": "transportation_name",
      "minzoom": 8,
      "filter": [
        "has",
        "name:latin"
      ],
      "layout": {
        "symbol-placement": "line",
        "text-field": [
          "coalesce",
          [
            "get",
            "name:latin"
          ],
          [
            "get",
            "name_int"
          ],
          [
            "get",
            "name"
          ]
        ],
        "text-font": [
          "Open Sans Regular"
        ],
        "text-size": [
          "interpolate",
          [
            "linear"
          ],
          [
            "zoom"
          ],
          8,
          10,
          14,
          13
        ],
        "text-rotation-alignment": "map",
        "text-letter-spacing": 0.02
      },
      "paint": {
        "text-color": "#5b5149",
        "text-halo-color": "#ffffff",
        "text-halo-width": 1.4
      }
    },
    {
      "id": "waterway-label",
      "type": "symbol",
      "source": "unr",
      "source-layer": "waterway",
      "minzoom": 10,
      "filter": [
        "has",
        "name:latin"
      ],
      "layout": {
        "symbol-placement": "line",
        "text-field": [
          "coalesce",
          [
            "get",
            "name:latin"
          ],
          [
            "get",
            "name_int"
          ],
          [
            "get",
            "name"
          ]
        ],
        "text-font": [
          "Open Sans Regular"
        ],
        "text-size": 11
      },
      "paint": {
        "text-color": "#397d9d",
        "text-halo-color": "#eef8fc",
        "text-halo-width": 1.2
      }
    },
    {
      "id": "water-label",
      "type": "symbol",
      "source": "unr",
      "source-layer": "water_name",
      "minzoom": 10,
      "filter": [
        "has",
        "name:latin"
      ],
      "layout": {
        "text-field": [
          "coalesce",
          [
            "get",
            "name:latin"
          ],
          [
            "get",
            "name_int"
          ],
          [
            "get",
            "name"
          ]
        ],
        "text-font": [
          "Open Sans Regular"
        ],
        "text-size": 12
      },
      "paint": {
        "text-color": "#397d9d",
        "text-halo-color": "#eef8fc",
        "text-halo-width": 1.2
      }
    },
    {
      "id": "poi-dot",
      "type": "circle",
      "source": "unr",
      "source-layer": "poi",
      "minzoom": 12,
      "paint": {
        "circle-radius": [
          "interpolate",
          [
            "linear"
          ],
          [
            "zoom"
          ],
          12,
          2.5,
          16,
          4.5
        ],
        "circle-color": "#a35c54",
        "circle-stroke-color": "#ffffff",
        "circle-stroke-width": 1
      }
    },
    {
      "id": "poi-label",
      "type": "symbol",
      "source": "unr",
      "source-layer": "poi",
      "minzoom": 12,
      "filter": [
        "has",
        "name:latin"
      ],
      "layout": {
        "text-field": [
          "coalesce",
          [
            "get",
            "name:latin"
          ],
          [
            "get",
            "name_int"
          ],
          [
            "get",
            "name"
          ]
        ],
        "text-font": [
          "Open Sans Regular"
        ],
        "text-size": [
          "interpolate",
          [
            "linear"
          ],
          [
            "zoom"
          ],
          12,
          10,
          16,
          12
        ],
        "text-offset": [
          0,
          0.9
        ],
        "text-anchor": "top",
        "text-optional": true
      },
      "paint": {
        "text-color": "#4a3e38",
        "text-halo-color": "#ffffff",
        "text-halo-width": 1.3
      }
    },
    {
      "id": "aerodrome-label",
      "type": "symbol",
      "source": "unr",
      "source-layer": "aerodrome_label",
      "minzoom": 10,
      "filter": [
        "has",
        "name:latin"
      ],
      "layout": {
        "text-field": [
          "coalesce",
          [
            "get",
            "name:latin"
          ],
          [
            "get",
            "name_int"
          ],
          [
            "get",
            "name"
          ]
        ],
        "text-font": [
          "Open Sans Regular"
        ],
        "text-size": 12
      },
      "paint": {
        "text-color": "#4e5963",
        "text-halo-color": "#ffffff",
        "text-halo-width": 1.2
      }
    },
    {
      "id": "mountain-label",
      "type": "symbol",
      "source": "unr",
      "source-layer": "mountain_peak",
      "minzoom": 11,
      "filter": [
        "has",
        "name:latin"
      ],
      "layout": {
        "text-field": [
          "concat",
          "\u25b2 ",
          [
            "coalesce",
            [
              "get",
              "name:latin"
            ],
            [
              "get",
              "name_int"
            ],
            [
              "get",
              "name"
            ]
          ]
        ],
        "text-font": [
          "Open Sans Regular"
        ],
        "text-size": 11
      },
      "paint": {
        "text-color": "#6c5848",
        "text-halo-color": "#ffffff",
        "text-halo-width": 1.2
      }
    },
    {
      "id": "housenumber",
      "type": "symbol",
      "source": "unr",
      "source-layer": "housenumber",
      "minzoom": 14,
      "filter": [
        "has",
        "housenumber"
      ],
      "layout": {
        "text-field": [
          "get",
          "housenumber"
        ],
        "text-font": [
          "Open Sans Regular"
        ],
        "text-size": 9
      },
      "paint": {
        "text-color": "#766a61",
        "text-halo-color": "#ffffff",
        "text-halo-width": 1
      }
    },
    {
      "id": "place-neighborhood",
      "type": "symbol",
      "source": "unr",
      "source-layer": "place",
      "minzoom": 11,
      "filter": [
        "in",
        [
          "get",
          "class"
        ],
        [
          "literal",
          [
            "neighbourhood",
            "suburb",
            "hamlet",
            "locality"
          ]
        ]
      ],
      "layout": {
        "text-field": [
          "coalesce",
          [
            "get",
            "name:latin"
          ],
          [
            "get",
            "name_int"
          ],
          [
            "get",
            "name"
          ]
        ],
        "text-font": [
          "Open Sans Regular"
        ],
        "text-size": [
          "interpolate",
          [
            "linear"
          ],
          [
            "zoom"
          ],
          11,
          10,
          14,
          12
        ],
        "text-max-width": 9,
        "text-padding": 3
      },
      "paint": {
        "text-color": "#34302d",
        "text-halo-color": "#ffffff",
        "text-halo-width": 1.6
      }
    },
    {
      "id": "place-town",
      "type": "symbol",
      "source": "unr",
      "source-layer": "place",
      "minzoom": 7,
      "filter": [
        "in",
        [
          "get",
          "class"
        ],
        [
          "literal",
          [
            "town",
            "village"
          ]
        ]
      ],
      "layout": {
        "text-field": [
          "coalesce",
          [
            "get",
            "name:latin"
          ],
          [
            "get",
            "name_int"
          ],
          [
            "get",
            "name"
          ]
        ],
        "text-font": [
          "Open Sans Regular"
        ],
        "text-size": [
          "interpolate",
          [
            "linear"
          ],
          [
            "zoom"
          ],
          7,
          11,
          14,
          15
        ],
        "text-max-width": 9,
        "text-padding": 3
      },
      "paint": {
        "text-color": "#34302d",
        "text-halo-color": "#ffffff",
        "text-halo-width": 1.6
      }
    },
    {
      "id": "place-city",
      "type": "symbol",
      "source": "unr",
      "source-layer": "place",
      "minzoom": 5,
      "filter": [
        "in",
        [
          "get",
          "class"
        ],
        [
          "literal",
          [
            "city"
          ]
        ]
      ],
      "layout": {
        "text-field": [
          "coalesce",
          [
            "get",
            "name:latin"
          ],
          [
            "get",
            "name_int"
          ],
          [
            "get",
            "name"
          ]
        ],
        "text-font": [
          "Open Sans Regular"
        ],
        "text-size": [
          "interpolate",
          [
            "linear"
          ],
          [
            "zoom"
          ],
          5,
          16,
          14,
          20
        ],
        "text-max-width": 9,
        "text-padding": 3
      },
      "paint": {
        "text-color": "#34302d",
        "text-halo-color": "#ffffff",
        "text-halo-width": 1.6
      }
    },
    {
      "id": "place-state",
      "type": "symbol",
      "source": "unr",
      "source-layer": "place",
      "minzoom": 4,
      "filter": [
        "in",
        [
          "get",
          "class"
        ],
        [
          "literal",
          [
            "state"
          ]
        ]
      ],
      "layout": {
        "text-field": [
          "coalesce",
          [
            "get",
            "name:latin"
          ],
          [
            "get",
            "name_int"
          ],
          [
            "get",
            "name"
          ]
        ],
        "text-font": [
          "Open Sans Regular"
        ],
        "text-size": [
          "interpolate",
          [
            "linear"
          ],
          [
            "zoom"
          ],
          4,
          14,
          14,
          18
        ],
        "text-max-width": 9,
        "text-padding": 3
      },
      "paint": {
        "text-color": "#34302d",
        "text-halo-color": "#ffffff",
        "text-halo-width": 1.6
      }
    },
    {
      "id": "place-country",
      "type": "symbol",
      "source": "unr",
      "source-layer": "place",
      "minzoom": 1,
      "filter": [
        "in",
        [
          "get",
          "class"
        ],
        [
          "literal",
          [
            "country"
          ]
        ]
      ],
      "layout": {
        "text-field": [
          "coalesce",
          [
            "get",
            "name:latin"
          ],
          [
            "get",
            "name_int"
          ],
          [
            "get",
            "name"
          ]
        ],
        "text-font": [
          "Open Sans Regular"
        ],
        "text-size": [
          "interpolate",
          [
            "linear"
          ],
          [
            "zoom"
          ],
          1,
          16,
          14,
          20
        ],
        "text-max-width": 9,
        "text-padding": 3
      },
      "paint": {
        "text-color": "#34302d",
        "text-halo-color": "#ffffff",
        "text-halo-width": 1.6
      }
    }




    /////
  ]
}

export default style
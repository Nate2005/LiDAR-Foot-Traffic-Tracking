import { PMTiles, Protocol } from 'pmtiles'
import * as maplibregl from 'maplibre-gl'
import type { StyleSpecification } from 'maplibre-gl'
import 'maplibre-gl/dist/maplibre-gl.css'

export async function createMap(
  container: string,
  style: StyleSpecification
) {
  const archiveUrl = '/unr.pmtiles'

  const protocol = new Protocol({ metadata: true })
  const archive = new PMTiles(archiveUrl)

  protocol.add(archive)
  maplibregl.addProtocol('pmtiles', protocol.tile)

  const header = await archive.getHeader()

  style.sources.unr = {
    type: 'vector',
    url: `pmtiles://${archiveUrl}`
  }

  maplibregl.setWorkerUrl('/maplibre-gl-worker.mjs')


  //bounries so that the user cant see the map
  //also includes the starting point be the quad
  const map = new maplibregl.Map({
    container,
    style,
    //center: [header.centerLon, header.centerLat],
    center: [-119.81452, 39.53860 ],
    zoom: 16,
    minZoom: 15,
    maxZoom: 19,
    attributionControl: false
  })

  map.setMaxBounds([
    [-119.83, 39.53],
    [-119.80, 39.56]
  ])

  map.addControl(
    new maplibregl.NavigationControl(),
     'top-right'
  )


    //Debug Tool for lat and long///////////////////////////////////////////////////////////////////  
  const coordsDiv = document.createElement('div')
coordsDiv.style.position = 'absolute'
coordsDiv.style.bottom = '10px'
coordsDiv.style.left = '10px'
coordsDiv.style.background = 'white'
coordsDiv.style.padding = '4px 8px'
coordsDiv.style.zIndex = '1000'
map.getContainer().appendChild(coordsDiv)

map.on('move', () => { const center = map.getCenter()
 const zoom = map.getZoom()
// const z = Math.floor(zoom)
 //const scale = Math.pow(2, z)
 //const x = Math.floor(  ((center.lng + 180) / 360) * scale )
 //const y = Math.floor(  (   (1 -    Math.log(     Math.tan(center.lat * Math.PI / 180) +     1 / Math.cos(center.lat * Math.PI / 180)    ) / Math.PI   ) / 2  ) * scale )
 coordsDiv.textContent =  `${center.lat.toFixed(5)}, ${center.lng.toFixed(5)},z${zoom.toFixed(2)}`}) //${z}/${x}/${y}
//  ////////////////////////////

  return map
}



<script setup lang="ts">
import { onMounted } from 'vue'
import rawStyle from '../styles/style-unr'

import { createMap } from '../services/map'
import type { RouteRequest } from '../types/route'

import SearchPanel from '../components/SearchPanel.vue'


// Placeholder until ApiController.getRoute and MapView.drawRoutes exist.
function onRoute(request: RouteRequest) {
  console.log('Route requested', request)
}

onMounted(async () => {
  const style = structuredClone(rawStyle)

  const map = await createMap(
    'map',
    style
  )

  map.on('load', () => {
    console.log('Map loaded')
  })
})
</script>

<template>
  <div class="map-container">

    <SearchPanel @route="onRoute" />
    <div id="map"></div>

    <div class="attribution">
      © OpenStreetMap contributors
    </div>

  </div>
</template>




<style scoped>

.map-container {
  position: relative;
  height: 100vh;
}

#map {
  width: 100%;
  height: 100vh;
}

.attribution {
  position: absolute;
  bottom: 0px;
  right: 10px;

  background: rgba(255,255,255,.9);
  padding: 0px 0px;

  font-size: 12px;

  border-radius: 4px;
}

</style>
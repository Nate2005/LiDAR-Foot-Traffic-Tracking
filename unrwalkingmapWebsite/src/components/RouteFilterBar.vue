<template>
  <div class="filter-bar" role="group" aria-label="Route filters">
    <button
      v-for="option in modes"
      :key="option.value"
      type="button"
      class="pill"
      :class="{ active: mode === option.value }"
      :aria-pressed="mode === option.value"
      @click="setMode(option.value)"
    >
      {{ option.label }}
    </button>
    <button
      type="button"
      class="pill"
      :class="{ active: ada }"
      :aria-pressed="ada"
      @click="toggleAda"
    >
      ADA
    </button>
  </div>
</template>

<script setup lang="ts">
import type { TravelMode } from '../types/route'

// Props map to the class diagram: activeMode and adaEnabled.
const mode = defineModel<TravelMode>('mode', { default: 'walking' })
const ada = defineModel<boolean>('ada', { default: false })

const modes: { value: TravelMode; label: string }[] = [
  { value: 'walking', label: 'Walking' },
  { value: 'bike', label: 'Bike/Scooter' },
]

function setMode(next: TravelMode) {
  mode.value = next
}

function toggleAda() {
  ada.value = !ada.value
}
</script>

<style scoped>
.filter-bar {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  padding-top: 8px;
}

.pill {
  border: 1px solid #ccc;
  background: white;
  color: #222;
  border-radius: 999px;
  padding: 6px 14px;
  font-size: 14px;
  cursor: pointer;
}

.pill.active {
  background: #239eed;
  border-color: #239eed;
  color: white;
}

.pill:focus-visible {
  outline: 2px solid #003366;
  outline-offset: 2px;
}
</style>

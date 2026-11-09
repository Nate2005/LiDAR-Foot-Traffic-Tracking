<template>
  <div class="search-overlay">
    <label class="field">
      <span class="label">From</span>
      <input class="search-input" :value="fromLabel" readonly aria-label="From" />
    </label>

    <label class="field">
      <span class="label">To</span>
      <input
        ref="toInput"
        class="search-input"
        v-model="toText"
        placeholder="Search buildings..."
        aria-label="To"
        autocomplete="off"
        @focus="open = true"
        @input="onInput"
      />
    </label>

    <ul v-if="open && suggestions.length" class="dropdown" role="listbox">
      <li
        v-for="building in suggestions"
        :key="building.id"
        role="option"
        class="item"
        @mousedown.prevent="selectBuilding(building)"
      >
        {{ building.name }}
      </li>
    </ul>

    <RouteFilterBar v-model:mode="mode" v-model:ada="ada" />
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import RouteFilterBar from './RouteFilterBar.vue'
import { buildings } from '../data/buildings'
import type { Building, RouteRequest, TravelMode } from '../types/route'

const STORAGE_KEY = 'recentSearches'
const MAX_RECENT = 5

const emit = defineEmits<{ route: [request: RouteRequest] }>()

const fromLabel = ref('')
const toText = ref('')
const selected = ref<Building | null>(null)
const open = ref(false)
const mode = ref<TravelMode>('walking')
const ada = ref(false)
const recentSearches = ref<Building[]>([])

const suggestions = computed<Building[]>(() => {
  const query = toText.value.trim().toLowerCase()
  if (!query) return recentSearches.value
  return buildings.filter((b) => b.name.toLowerCase().includes(query))
})

function prefillCurrentLocation() {
  fromLabel.value = 'Current location'
}

function loadRecentSearches() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    const ids: string[] = raw ? JSON.parse(raw) : []
    recentSearches.value = ids
      .map((id) => buildings.find((b) => b.id === id))
      .filter((b): b is Building => Boolean(b))
      .slice(0, MAX_RECENT)
  } catch {
    recentSearches.value = []
  }
}

function saveRecentSearch(building: Building) {
  const next = [building, ...recentSearches.value.filter((b) => b.id !== building.id)].slice(
    0,
    MAX_RECENT,
  )
  recentSearches.value = next
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(next.map((b) => b.id)))
  } catch {
    // storage unavailable: recents just won't persist
  }
}

function onInput() {
  selected.value = null
  open.value = true
}

function selectBuilding(building: Building) {
  selected.value = building
  toText.value = building.name
  open.value = false
  saveRecentSearch(building)
  submitRoute()
}

function submitRoute() {
  if (!selected.value) return
  emit('route', {
    fromId: null,
    toId: selected.value.id,
    mode: mode.value,
    ada: ada.value,
  })
}

// Re-route when a filter changes after a destination was chosen.
watch([mode, ada], submitRoute)

onMounted(() => {
  prefillCurrentLocation()
  loadRecentSearches()
})

defineExpose({ prefillCurrentLocation, selectBuilding, submitRoute })
</script>

<style scoped>
.search-overlay {
  position: absolute;
  top: 10px;
  left: 12px;
  z-index: 1000;

  width: 25%;
  min-width: 260px;
  max-width: calc(100vw - 24px);

  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.15);

  padding: 8px;
}

.field {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 6px;
}

.label {
  width: 36px;
  font-size: 13px;
  color: #555;
}

.search-input {
  flex: 1;
  height: 40px;
  box-sizing: border-box;
  font-size: 16px;
  padding: 0 12px;
  border-radius: 6px;
  border: 1px solid #ccc;
}

.dropdown {
  list-style: none;
  margin: 0 0 4px;
  padding: 4px 0;
  max-height: 240px;
  overflow-y: auto;
  border: 1px solid #ddd;
  border-radius: 6px;
  background: white;
}

.item {
  padding: 10px 12px;
  cursor: pointer;
  font-size: 15px;
}

.item:hover {
  background: #eef6fd;
}
</style>

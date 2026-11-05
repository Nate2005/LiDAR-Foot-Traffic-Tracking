<template>
  <div class="search-overlay">
    <input
      class="search-input"      
      v-model="searchText"
      placeholder="Search..."
    />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const searchText = ref('')
</script>

<style scoped>
.search-overlay {
  position: absolute;
  top: 10px;
  left: 12px;
  z-index: 1000;

  width: 25%;
  max-width: calc(100vw - 24px);

  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0,0,0,.15);

  padding: 8px;
 
}

.search-input {
  width: 100%; 
  height: 40px;

  box-sizing: border-box;

  font-size: 16px;

  padding: 0 12px;

  border-radius: 6px;
  border: 1px solid #ccc;
}
</style>

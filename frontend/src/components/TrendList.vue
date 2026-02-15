<template>
  <div class="trend-list-container">
    <h2>🔥 Trending Now</h2>
    <div class="controls">
      <button 
        :class="{ active: country === 'united_states' }" 
        @click="$emit('update:country', 'united_states')"
      >
        🇺🇸 USA
      </button>
      <button 
        :class="{ active: country === 'south_korea' }" 
        @click="$emit('update:country', 'south_korea')"
      >
        🇰🇷 Korea
      </button>
    </div>
    
    <div v-if="loading" class="loading">Loading trends...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    
    <ul v-else class="trend-list">
      <li 
        v-for="(trend, index) in trends" 
        :key="index"
        @click="$emit('select-trend', trend)"
        class="trend-item"
      >
        <span class="rank">{{ index + 1 }}</span>
        <span class="keyword">{{ trend }}</span>
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  trends: string[];
  loading: boolean;
  error: string | null;
  country: string;
}>();

defineEmits<{
  (e: 'update:country', country: string): void;
  (e: 'select-trend', trend: string): void;
}>();
</script>

<style scoped>
.trend-list-container {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
  height: 100%;
  overflow-y: auto;
}

h2 {
  margin-top: 0;
  margin-bottom: 20px;
  font-size: 1.5rem;
  color: #333;
}

.controls {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

button {
  padding: 8px 16px;
  border: 1px solid #ddd;
  border-radius: 20px;
  background: #f5f5f5;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.2s;
}

button.active {
  background: #007bff;
  color: white;
  border-color: #007bff;
}

.trend-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.trend-item {
  display: flex;
  align-items: center;
  padding: 12px 16px;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.2s;
  border-bottom: 1px solid #f0f0f0;
}

.trend-item:hover {
  background-color: #f8f9fa;
  transform: translateX(2px);
}

.rank {
  font-weight: bold;
  color: #007bff;
  width: 30px;
  font-size: 1.1rem;
}

.keyword {
  font-weight: 500;
  font-size: 1.1rem;
}

.loading, .error {
  text-align: center;
  padding: 20px;
  color: #666;
}

.error {
  color: #dc3545;
}
</style>

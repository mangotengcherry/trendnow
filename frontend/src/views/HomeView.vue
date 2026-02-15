<template>
  <div class="home-container">
    <main class="main-layout">
      <div class="sidebar">
        <TrendList 
          :trends="trends" 
          :loading="loadingTrends" 
          :error="error"
          :country="country"
          @update:country="changeCountry"
          @select-trend="selectTrend"
        />
      </div>
      <div class="content">
        <TrendDetail 
          :keyword="selectedKeyword"
          :loading="loadingDetail"
          :related-data="trendDetail"
          @close="selectedKeyword = null"
        />
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import TrendList from '../components/TrendList.vue';
import TrendDetail from '../components/TrendDetail.vue';
import apiClient from '../services/api';

const trends = ref<string[]>([]);
const loadingTrends = ref(false);
const error = ref<string | null>(null);
const country = ref('united_states');

const selectedKeyword = ref<string | null>(null);
const loadingDetail = ref(false);
const trendDetail = ref(null);

const fetchTrends = async (cntry: string) => {
  loadingTrends.value = true;
  error.value = null;
  // trends.value = [];
  try {
    const response = await apiClient.get('/trends', {
      params: { country: cntry }
    });
    trends.value = response.data.trends;
  } catch (err) {
    console.error(err);
    error.value = 'Failed to load trends. Please try again.';
  } finally {
    loadingTrends.value = false;
  }
};

const changeCountry = (newCountry: string) => {
  if (country.value === newCountry) return;
  country.value = newCountry;
  fetchTrends(newCountry);
  selectedKeyword.value = null;
};

const selectTrend = async (keyword: string) => {
  selectedKeyword.value = keyword;
  loadingDetail.value = true;
  trendDetail.value = null;
  
  try {
    const response = await apiClient.get(`/related/${encodeURIComponent(keyword)}`);
    trendDetail.value = response.data;
  } catch (err) {
    console.error(err);
  } finally {
    loadingDetail.value = false;
  }
};

onMounted(() => {
  fetchTrends(country.value);
});
</script>

<style scoped>
.home-container {
  height: calc(100vh - 80px); /* Adjust for header */
  display: flex;
  flex-direction: column;
}

.main-layout {
  display: grid;
  grid-template-columns: 350px 1fr;
  gap: 24px;
  flex: 1;
  min-height: 0;
}

.sidebar, .content {
  height: 100%;
  overflow: hidden;
}

@media (max-width: 900px) {
  .main-layout {
    grid-template-columns: 1fr;
    grid-template-rows: 400px 1fr;
  }
}
</style>

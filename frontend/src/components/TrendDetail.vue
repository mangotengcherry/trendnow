<template>
  <div class="trend-detail-container" v-if="keyword">
    <div class="detail-header">
      <h2>Results for: <span class="highlight">{{ keyword }}</span></h2>
      <button class="close-btn" @click="$emit('close')">&times;</button>
    </div>

    <div v-if="loading" class="loading">Fetching related content...</div>
    
    <div v-else class="content-grid">
      <!-- News Section -->
      <div class="section news-section">
        <h3>📰 Related News</h3>
        <div v-if="relatedData?.news.length === 0" class="empty">No news found</div>
        <div v-else class="cards">
            <a 
              v-for="(item, idx) in relatedData?.news" 
              :key="idx" 
              :href="item.link" 
              target="_blank"
              class="card news-card"
            >
              <div class="card-source">{{ item.source }}</div>
              <div class="card-title">{{ item.title }}</div>
              <div class="card-date">{{ new Date(item.published).toLocaleDateString() }}</div>
            </a>
        </div>
      </div>

      <!-- Social Section -->
      <div class="section social-section">
        <h3>💬 Social Reactions (Simulated)</h3>
        <div class="cards">
            <div 
              v-for="(post, idx) in relatedData?.social_posts" 
              :key="idx" 
              class="card social-card"
            >
              <div class="card-header">
                <span class="platform-badge" :class="post.platform.toLowerCase()">{{ post.platform }}</span>
                <span class="author">@{{ post.author }}</span>
              </div>
              <div class="card-content">{{ post.content }}</div>
              <div class="card-footer">
                <span>❤️ {{ post.likes }}</span>
                <span>🔄 {{ post.shares }}</span>
              </div>
            </div>
        </div>
      </div>
    </div>
  </div>
  <div v-else class="trend-detail-container empty-state">
    <div class="placeholder">
      <span class="icon">👈</span>
      <h3>Select a trending keyword to see details</h3>
      <p>Click on any item from the list to view related news and social reactions.</p>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  keyword: string | null;
  loading: boolean;
  relatedData: {
    news: Array<{ title: string; link: string; source: string; published: string }>;
    social_posts: Array<{ platform: string; author: string; content: string; likes: number; shares: number }>;
  } | null;
}>();

defineEmits<{
  (e: 'close'): void;
}>();
</script>

<style scoped>
.trend-detail-container {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
  height: 100%;
  overflow-y: auto;
}

.empty-state {
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  color: #888;
}

.placeholder .icon {
  font-size: 3rem;
  display: block;
  margin-bottom: 20px;
}

.detail-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  border-bottom: 1px solid #eee;
  padding-bottom: 15px;
}

h2 {
  margin: 0;
  font-size: 1.8rem;
}

.highlight {
  color: #007bff;
}

.close-btn {
  background: none;
  border: none;
  font-size: 2rem;
  cursor: pointer;
  color: #999;
}

.content-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
}

@media (max-width: 768px) {
  .content-grid {
    grid-template-columns: 1fr;
  }
}

.section h3 {
  margin-top: 0;
  margin-bottom: 16px;
  font-size: 1.2rem;
  color: #444;
}

.cards {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.card {
  padding: 16px;
  border: 1px solid #eee;
  border-radius: 8px;
  transition: transform 0.2s, box-shadow 0.2s;
  text-decoration: none;
  color: inherit;
  background: #fff;
  display: block;
}

.news-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
  border-color: #007bff;
}

.card-source {
  font-size: 0.8rem;
  color: #666;
  margin-bottom: 4px;
  text-transform: uppercase;
  font-weight: 600;
}

.card-title {
  font-weight: 600;
  font-size: 1.05rem;
  margin-bottom: 8px;
  line-height: 1.4;
}

.card-date {
  font-size: 0.8rem;
  color: #999;
}

.social-card {
  background: #f9f9f9;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.platform-badge {
  font-size: 0.75rem;
  padding: 2px 8px;
  border-radius: 12px;
  color: white;
  background: #666;
}

.platform-badge.twitter { background: #1DA1F2; }
.platform-badge.threads { background: #000; }
.platform-badge.reddit { background: #FF4500; }

.author {
  font-size: 0.9rem;
  color: #555;
}

.card-content {
  margin-bottom: 12px;
  line-height: 1.5;
}

.card-footer {
  display: flex;
  gap: 15px;
  font-size: 0.85rem;
  color: #666;
}

.loading {
  text-align: center;
  padding: 40px;
  font-size: 1.2rem;
  color: #666;
}
</style>

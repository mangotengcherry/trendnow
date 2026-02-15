<template>
  <div class="app-container">
    <header class="app-header">
      <div class="branding">
        <div class="logo" @click="$router.push('/')">🚀 TrendPulse</div>
        <p class="subtitle">Real-time Insights</p>
      </div>
      
      <nav class="user-nav">
        <div v-if="authStore.isAuthenticated" class="user-menu">
           <span class="user-email">{{ authStore.user?.email }}</span>
           <router-link to="/profile" class="nav-link">Profile</router-link>
           <button @click="handleLogout" class="logout-btn">Logout</button>
        </div>
        <div v-else>
           <router-link to="/login" class="login-link">Login</router-link>
        </div>
      </nav>
    </header>

    <router-view></router-view>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from './stores/auth';
import { useRouter } from 'vue-router';

const authStore = useAuthStore();
const router = useRouter();

const handleLogout = () => {
    authStore.logout();
    router.push('/login');
};
</script>

<style>
body {
  margin: 0;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
  background-color: #f0f2f5;
  color: #333;
}

.app-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 20px;
  min-height: 100vh;
  box-sizing: border-box;
}

.app-header {
  margin-bottom: 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 15px;
  border-bottom: 1px solid #e0e0e0;
}

.branding {
    display: flex;
    align-items: baseline;
    gap: 15px;
}

.logo {
  font-size: 1.8rem;
  font-weight: 800;
  color: #007bff;
  letter-spacing: -1px;
  cursor: pointer;
}

.subtitle {
  color: #666;
  font-size: 1rem;
  margin: 0;
}

.user-nav {
    display: flex;
    gap: 15px;
    align-items: center;
}

.user-email {
    font-weight: 500;
    margin-right: 10px;
}

.nav-link {
    text-decoration: none;
    color: #333;
    font-weight: 500;
}

.nav-link:hover {
    color: #007bff;
}

.login-link {
    background: #007bff;
    color: white;
    padding: 8px 16px;
    border-radius: 20px;
    text-decoration: none;
    font-weight: 500;
}

.logout-btn {
    background: none;
    border: 1px solid #ddd;
    padding: 5px 10px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 0.9rem;
}

.logout-btn:hover {
    background: #f5f5f5;
}
</style>

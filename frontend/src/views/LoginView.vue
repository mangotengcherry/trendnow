<template>
  <div class="login-container">
    <div class="login-card">
      <h1>Welcome Back</h1>
      <p class="subtitle">Sign in to continue</p>
      
      <!-- Google Login Button -->
      <!-- In a real app, use the GoogleLogin component -->
      <!-- <GoogleLogin :callback="callback" /> -->
      
      <div class="google-btn-wrapper">
         <GoogleLogin :callback="handleGoogleCallback" />
      </div>

      <div class="divider">
        <span>OR</span>
      </div>

      <!-- Password Login Form -->
      <form @submit.prevent="handlePasswordLogin" class="login-form">
        <div class="form-group">
          <label>Email</label>
          <input v-model="email" type="email" placeholder="Enter your email" required />
        </div>
        <div class="form-group">
          <label>Password</label>
          <input v-model="password" type="password" placeholder="Enter your password" required />
        </div>
        <button type="submit" class="submit-btn" :disabled="loading">
          {{ loading ? 'Signing in...' : 'Sign In with Password' }}
        </button>
        <p v-if="error" class="error-msg">{{ error }}</p>
      </form>

      <div class="dev-tools">
        <p>Development Mode:</p>
        <button @click="mockGoogleLogin" class="mock-btn">Simulate Google Login</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/auth';
import { GoogleLogin } from 'vue3-google-login';

const email = ref('');
const password = ref('');
const error = ref('');
const loading = ref(false);

const router = useRouter();
const authStore = useAuthStore();

const handleGoogleCallback = async (response: any) => {
  // logic to send response.credential to backend
  const success = await authStore.googleLogin(response.credential);
  if (success) {
      router.push('/');
  } else {
      error.value = "Google login failed";
  }
};

const handlePasswordLogin = async () => {
    loading.value = true;
    error.value = '';
    try {
        await authStore.passwordLogin(email.value, password.value);
        router.push('/');
    } catch (err) {
        error.value = "Invalid email or password. New users must sign up with Google first.";
    } finally {
        loading.value = false;
    }
};

const mockGoogleLogin = async () => {
    const mockToken = "mock_token_devuser";
    const success = await authStore.googleLogin(mockToken);
    if (success) {
        router.push('/');
    }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 80vh;
}

.login-card {
  background: white;
  padding: 40px;
  border-radius: 16px;
  box-shadow: 0 10px 25px rgba(0,0,0,0.05);
  width: 100%;
  max-width: 400px;
  text-align: center;
}

h1 {
  margin-bottom: 10px;
  color: #333;
}

.subtitle {
  color: #666;
  margin-bottom: 30px;
}

.google-btn-wrapper {
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
}

.divider {
  display: flex;
  align-items: center;
  margin: 20px 0;
  color: #999;
  font-size: 0.9rem;
}

.divider::before, .divider::after {
  content: "";
  flex: 1;
  border-bottom: 1px solid #eee;
}

.divider span {
  padding: 0 10px;
}

.form-group {
  margin-bottom: 15px;
  text-align: left;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-size: 0.9rem;
  font-weight: 500;
}

.form-group input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 1rem;
}

.submit-btn {
  width: 100%;
  padding: 12px;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  margin-top: 10px;
}

.submit-btn:disabled {
    background: #ccc;
}

.error-msg {
    color: red;
    margin-top: 10px;
    font-size: 0.9rem;
}

.dev-tools {
    margin-top: 30px;
    padding-top: 20px;
    border-top: 1px dashed #ddd;
}

.mock-btn {
    background: #666;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 0.8rem;
}
</style>

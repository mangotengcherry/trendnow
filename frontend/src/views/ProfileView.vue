<template>
  <div class="profile-container">
    <div class="profile-card">
        <h1>User Profile</h1>
        <div class="user-info">
            <p><strong>Email:</strong> {{ authStore.user?.email }}</p>
            <p><strong>Account Type:</strong> {{ authStore.user?.has_password ? 'Google + Password' : 'Google Only' }}</p>
        </div>

        <div class="password-section">
            <h2>{{ authStore.user?.has_password ? 'Change Password' : 'Set Password' }}</h2>
            <form @submit.prevent="handleSetPassword">
                <input v-model="newPassword" type="password" placeholder="New Password" required />
                <button type="submit">{{ authStore.user?.has_password ? 'Update Password' : 'Set Password' }}</button>
            </form>
            <p v-if="message" :class="{'success': !isError, 'error': isError}">{{ message }}</p>
        </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useAuthStore } from '../stores/auth';

const authStore = useAuthStore();
const newPassword = ref('');
const message = ref('');
const isError = ref(false);

const handleSetPassword = async () => {
    message.value = '';
    isError.value = false;
    try {
        await authStore.setPassword(newPassword.value);
        message.value = "Password updated successfully!";
        newPassword.value = '';
    } catch (error) {
        isError.value = true;
        message.value = "Failed to update password.";
    }
};
</script>

<style scoped>
.profile-container {
    display: flex;
    justify-content: center;
    margin-top: 50px;
}

.profile-card {
    background: white;
    padding: 30px;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    width: 100%;
    max-width: 500px;
}

h1 { margin-top: 0; }

.user-info {
    margin-bottom: 30px;
    padding-bottom: 20px;
    border-bottom: 1px solid #eee;
}

.password-section input {
    width: 100%;
    padding: 10px;
    margin-bottom: 10px;
    border: 1px solid #ddd;
    border-radius: 4px;
    box-sizing: border-box;
}

.password-section button {
    background: #007bff;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 4px;
    cursor: pointer;
}

.success { color: green; margin-top: 10px; }
.error { color: red; margin-top: 10px; }
</style>

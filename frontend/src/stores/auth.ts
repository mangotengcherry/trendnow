import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import apiClient from '../services/api';
import { googleSdkLoaded } from 'vue3-google-login';

export const useAuthStore = defineStore('auth', () => {
    const user = ref(JSON.parse(localStorage.getItem('user') || 'null'));
    const token = ref(localStorage.getItem('token') || null);

    const isAuthenticated = computed(() => !!token.value);

    function setUser(newUser: any, newToken: string) {
        user.value = newUser;
        token.value = newToken;
        localStorage.setItem('user', JSON.stringify(newUser));
        localStorage.setItem('token', newToken);
        apiClient.defaults.headers.common['Authorization'] = `Bearer ${newToken}`;
    }

    function logout() {
        user.value = null;
        token.value = null;
        localStorage.removeItem('user');
        localStorage.removeItem('token');
        delete apiClient.defaults.headers.common['Authorization'];
    }

    async function googleLogin(credential: string) {
        try {
            const response = await apiClient.post('/auth/google', { token: credential });
            setUser({
                id: response.data.user_id,
                email: response.data.email,
                has_password: response.data.has_password
            }, response.data.access_token);
            return true;
        } catch (error) {
            console.error('Google login failed', error);
            return false;
        }
    }

    async function passwordLogin(email: string, password: string) {
        try {
            const response = await apiClient.post('/auth/login', { email, password });
            setUser({
                id: response.data.user_id,
                email: response.data.email,
                has_password: response.data.has_password
            }, response.data.access_token);
            return true;
        } catch (error) {
            console.error('Password login failed', error);
            throw error;
        }
    }

    async function setPassword(password: string) {
        try {
            await apiClient.post('/auth/password', { password });
            if (user.value) user.value.has_password = true;
            localStorage.setItem('user', JSON.stringify(user.value));
            return true;
        } catch (error) {
            console.error('Set password failed', error);
            throw error;
        }
    }

    // Initialize axios header if token exists
    if (token.value) {
        apiClient.defaults.headers.common['Authorization'] = `Bearer ${token.value}`;
    }

    return { user, token, isAuthenticated, googleLogin, passwordLogin, logout, setPassword };
});

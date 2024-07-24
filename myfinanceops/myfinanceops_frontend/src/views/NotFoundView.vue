<template>
  <div>
    <h1>404 - Page Not Found</h1>
    <p>The page you are looking for does not exist.</p>
    <div v-if="isUserLoggedIn">
      <router-link to="/home" class="go-home-button">Go Home</router-link>
    </div>
    <div v-else>
      <router-link to="/signup" class="signup-button">Go to Signup</router-link>
      <router-link to="/login" class="login-button">Go to Login</router-link>
    </div>
  </div>
</template>

<script setup>
import {computed} from 'vue';
import {useAuthStore} from '@/stores/auth';

const authStore = useAuthStore();
const isUserLoggedIn = computed(() => authStore.isAuthenticated);
</script>

<style>
.go-home-button, .signup-button, .login-button {
  display: inline-block;
  margin: 5px;
  padding: 10px 15px;
  text-decoration: none;
  color: white;
  border-radius: 5px;
  cursor: pointer;
}

.go-home-button {
  background-color: #007bff;
}

.signup-button, .login-button {
  background-color: #d9534f;
}
</style>
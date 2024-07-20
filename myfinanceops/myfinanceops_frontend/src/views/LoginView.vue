<template>
  <main class="px-8 py-6 bg-gray-100">
    <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
      <div class="main-left col-span-2 flex flex-col">
        <div class="p-20 bg-white border border-gray-200 rounded-lg flex-1">
          <h1 class="mb-6 text-2xl">Don't have an account yet?</h1>
          <p class="mb-6 text-gray-500">
            <strong>No worries. Create your account by
              <router-link to="/signup" style="color: #3498db; text-decoration: underline;">signing up here.
              </router-link>
            </strong>
            <br>
            <br>
          </p>
        </div>
      </div>
      <div class="main-center col-span-2 space-y-4 flex flex-col">
        <div class="p-20 bg-white border border-gray-200 rounded-lg flex-1">
          <form @submit.prevent="handleLogin" class="space-y-6">
            <div>
              <h1 class="mb-6 text-2xl">Log in</h1>

              <label>E-mail</label><br>
              <input v-model="email" type="email" placeholder="Your e-mail address"
                     class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg">
            </div>

            <div>
              <label>Password</label><br>
              <input v-model="password" type="password" placeholder="Your password"
                     class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg">
            </div>
            <div>
              <button class="py-4 px-6 bg-purple-600 text-white rounded-lg">Log in</button>
              <p v-if="errorMessage" class="text-red-500">{{ errorMessage }}</p>
            </div>
          </form>
          <div v-if="authStore.error" class="text-red-500">
            <span class="material-icons" style="font-size: 1rem;">Error: </span>
            {{ authStore.error }}
          </div>
        </div>
      </div>
    </div>
  </main>
</template>

<script setup lang="ts">
import {computed, ref} from 'vue';
import {useRouter} from 'vue-router';
import {useAuthStore} from '@/stores/auth';

const email = ref('');
const password = ref('');
const errorMessage = ref('');
const router = useRouter();
const authStore = useAuthStore();

const handleLogin = async (event: Event) => {
  errorMessage.value = '';
  if (!email.value.trim() || !password.value.trim()) {
    errorMessage.value = "Please fill up both email and password.";
    return; // Stop the function here
  }
  event.preventDefault(); // Prevent default form submission
  try {
    // Pass email and password as a single object
    await authStore.login(email.value, password.value);
// Assuming `isLoggedIn` is a property that gets updated to true upon successful login
  } catch (error) {
    console.error(error);
  }
  try {
    await router.push('/home/'); // Redirect to the home page on successful login{

  } catch (error) {
    console.error(error);
    errorMessage.value = "Login failed. Please check your credentials and try again.";
  }
}

</script>
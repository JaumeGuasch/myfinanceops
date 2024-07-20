<script setup lang="ts">
import {onMounted} from 'vue';
import {useAuthStore} from '@/stores/auth';
import {useRouter} from 'vue-router';

const authStore = useAuthStore();
const router = useRouter(); // Ensure router is instantiated here

onMounted(async () => {
  try {
    await authStore.logout();
    router.push({name: 'login'}); // Use router to navigate
  } catch (error) {
    console.error('Logout failed:', error);
    // Optionally, handle the error by showing a message to the user
  }
});
</script>

<template>
  <div class="main-center col-span-2 space-y-4 flex flex-col">
    <div class="p-20 bg-white border border-gray-200 rounded-lg flex-1">
      <h1 class="mb-6 text-2xl">You have been logged out!</h1>
      <p class="mb-6 text-gray-500">
        <strong>Thank you for using our application.</strong>
        <br>
        <br>
      </p>
    </div>
  </div>
</template>

<style scoped>

</style>
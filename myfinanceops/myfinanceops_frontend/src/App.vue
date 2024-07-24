<template>
  <nav class="nav py-6 px-8 border-b border-gray-200">
    <div class="max-w-7xl mx-auto">
      <div class="flex items-center justify-between">
        <div class="menu-left">
          <a href="#" class="text-xl flex">
            <img src="./assets/mainlogo.png" width="120">
          </a>
        </div>
        <template v-if="isUserLoggedIn">
          <div class="menu-center absolute left-1/2 transform -translate-x-1/2 flex space-x-20">
            <a href="/home/" class="flex flex-col items-center">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                   stroke="currentColor" class="size-8">
                <path stroke-linecap="round" stroke-linejoin="round"
                      d="m2.25 12 8.954-8.955c.44-.439 1.152-.439 1.591 0L21.75 12M4.5 9.75v10.125c0 .621.504 1.125 1.125 1.125H9.75v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21h4.125c.621 0 1.125-.504 1.125-1.125V9.75M8.25 21h8.25"/>
              </svg>
              <span>Home</span>
            </a>

            <a href="/hedging/" class="flex flex-col items-center">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                   stroke="currentColor"
                   class="w-8 h-8">
                <path stroke-linecap="round" stroke-linejoin="round"
                      d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z"/>
              </svg>
              <span>Hedging</span>
            </a>

            <a href="/operations/" class="flex flex-col items-center">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                   stroke="currentColor" class="size-8">
                <path stroke-linecap="round" stroke-linejoin="round"
                      d="M8.25 6.75h12M8.25 12h12m-12 5.25h12M3.75 6.75h.007v.008H3.75V6.75Zm.375 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0ZM3.75 12h.007v.008H3.75V12Zm.375 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Zm-.375 5.25h.007v.008H3.75v-.008Zm.375 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Z"/>
              </svg>
              <span>Trades</span>
            </a>
            <a href="#" class="flex flex-col items-center">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                   stroke="currentColor" class="size-8">
                <path stroke-linecap="round" stroke-linejoin="round" d="M10.5 6a7.5 7.5 0 1 0 7.5 7.5h-7.5V6Z"/>
                <path stroke-linecap="round" stroke-linejoin="round" d="M13.5 10.5H21A7.5 7.5 0 0 0 13.5 3v7.5Z"/>
              </svg>
              <span>Analytics</span>
            </a>
            <a href="#" class="flex flex-col items-center">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                   stroke="currentColor"
                   class="w-8 h-8">
                <path stroke-linecap="round" stroke-linejoin="round"
                      d="M14.857 17.082a23.848 23.848 0 005.454-1.31A8.967 8.967 0 0118 9.75v-.7V9A6 6 0 006 9v.75a8.967 8.967 0 01-2.312 6.022c1.733.64 3.56 1.085 5.455 1.31m5.714 0a24.255 24.255 0 01-5.714 0m5.714 0a3 3 0 11-5.714 0"/>
              </svg>
              <span>Notifications</span>
            </a>
          </div>
          <div class="menu-right">
            <a href="#" v-if="isUserLoggedIn"
               style="font-style: normal; color: #000000; font-size: large; margin-right: 20px;">
              Hi, {{ userName }}
            </a>
            <a href="/logout" v-if="isUserLoggedIn" class="logout-button"
               style="display: inline-block; text-align: center; width: 100px; padding: 8px 0; background-color: #d9534f; color: white; text-decoration: none; border-radius: 5px; cursor: pointer;">
              Logout
            </a>
          </div>
        </template>
        <template v-else>
          <div class="menu-center absolute left-1/2 transform -translate-x-1/2">
            <!-- Only the company logo is centered here -->
          </div>
        </template>
      </div>
    </div>
  </nav>
  <main class="px-8 py-6 bg-white ">
    <router-view v-slot="{ Component }">
      <transition name="slide-fade" mode="out-in">
        <component :is="Component" :key="$route.fullPath"/>
      </transition>
    </router-view>
  </main>
</template>

<script setup lang="ts">
import {computed, watch} from 'vue';
import {useAuthStore} from '@/stores/auth';

const authStore = useAuthStore();


let userName = computed(() => authStore.userName);
const isUserLoggedIn = computed(() => authStore.isAuthenticated);

watch(() => authStore.isAuthenticated, (newVal) => {
  if (newVal) {
    userName = computed(() => authStore.user.name);
    const userNameString = userName.value;
    userName = computed(() => capitalizeFirstLetter(userNameString));
  } else {
    userName = computed(() => '');
  }
});

function capitalizeFirstLetter(string: string | null): string {
  if (string === null) {
    return '';
  }
  return string.charAt(0).toUpperCase() + string.slice(1).toLowerCase();
}

</script>

<style>

.nav {
  background-color: #f9fafb;
  border-bottom: 4px solid #dddddd;
}

body {
  background-color: #ffffff;
}

</style>

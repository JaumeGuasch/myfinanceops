<template>
  <main class="px-8 py-6 bg-gray-100">
    <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
      <div class="main-left col-span-2 flex flex-col">
        <div class="p-20 bg-white border border-gray-200 rounded-lg flex-1">
          <h1 class="mb-6 text-2xl">Log in</h1>
          <p class="mb-6 text-gray-500">
            <strong>Creating accounts is not supported on this application.</strong>
            <br>
            <br>
            Contact a system administrator from your organization in order to be assigned your personal credentials.
          </p>
        </div>
      </div>
      <div class="main-center col-span-2 space-y-4 flex flex-col">
        <div class="p-20 bg-white border border-gray-200 rounded-lg flex-1">
          <form class="space-y-6">
            <div>
              <label>E-mail</label><br>
              <input type="email" placeholder="Your e-mail address"
                     class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg">
            </div>

            <div>
              <label>Password</label><br>
              <input type="password" placeholder="Your password"
                     class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg">
            </div>

            <div>
              <button class="py-4 px-6 bg-purple-600 text-white rounded-lg">Log in</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </main>
</template>

<script setup lang="ts">
// Your setup code here. For example:
import {ref} from 'vue';

const email = ref('');
const password = ref('');

// Functions and reactive data defined here are automatically exposed to the template
</script>
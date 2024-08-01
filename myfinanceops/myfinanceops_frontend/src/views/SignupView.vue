<template>
  <main class="px-8 py-6 bg-gray-100">
    <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
      <div class="main-left col-span-2 flex flex-col">
        <div class="p-20 bg-white border border-gray-200 rounded-lg flex-1">
          <h1 class="mb-6 text-2xl">Already own an account?</h1>
          <p class="mb-6 text-gray-500">
            <strong>Go to the log in page by
              <router-link to="/login" style="color: #3498db; text-decoration: underline;">clicking here.
              </router-link>
            </strong>
            <br>
            <br>
          </p>
        </div>
      </div>
      <div class="main-center col-span-2 space-y-4 flex flex-col">
        <div class="p-20 bg-white border border-gray-200 rounded-lg flex-1">
          <form @submit.prevent="handleSignup" class="space-y-6">
            <div>
              <h1 class="mb-6 text-2xl">Sign up</h1>

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
              <label>Name</label><br>
              <input v-model="name" type="text" placeholder="Your name"
                     class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg">
            </div>

            <div>
              <label>Surnames</label><br>
              <input v-model="surnames" type="text" placeholder="Your surnames"
                     class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg">
            </div>

            <div>
              <label>Organization</label><br>
              <input v-model="organization" type="text" placeholder="Your organization"
                     class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg">
            </div>

            <div>
              <button type="submit" class="py-4 px-6 bg-purple-600 text-white rounded-lg">Sign up</button>
            </div>
            <br>
            <strong>
              <div v-if="successMessage" class="p-2 bg-blue-200 border border-gray-600 rounded-lg text-gray-600">
                <p>
                  Registration successful, redirecting you to the login page...
                </p>
              </div>
            </strong>
          </form>
          <p v-if="errorMessage" class="text-red-500">{{ errorMessage }}</p>
        </div>
      </div>
    </div>
  </main>
</template>

<script setup lang="ts">
import {ref} from 'vue';
import {useRouter} from 'vue-router';
import {useAuthStore} from '@/stores/auth';

const email = ref('');
const password = ref('');
const name = ref('');
const surnames = ref('');
const organization = ref('');
const errorMessage = ref('');
const router = useRouter();
const authStore = useAuthStore();
const successMessage = ref('');
const countdown = ref(3); // Initialize countdown


// Import the signup function from authService
import authService from '@/services/authService';

const handleSignup = async (event: Event) => {
  event.preventDefault(); // Prevent default form submission

  const userData = {
    email: email.value,
    password: password.value,
    name: name.value,
    surnames: surnames.value,
    organization: organization.value
  };

  try {
    const response = await authService.signup(
        userData.email,
        userData.password,
        userData.name,
        userData.surnames,
        userData.organization
    );

    successMessage.value = "Registration successful, redirecting you to the login page...";
    setTimeout(() => {
      router.push('/login/');
    }, 3000);

  } catch (error) {
    console.error(error);
    errorMessage.value = "Signup failed. Please check your information and try again.";
  }
}
</script>
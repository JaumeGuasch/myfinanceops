import './assets/main.css'
import {createApp} from 'vue'
import {createPinia} from 'pinia'
import App from './App.vue'
import router from './router'
import axios from 'axios'

// Add CSRF token to axios if needed

axios.defaults.baseURL = 'http://127.0.0.1:8000/' // Django URL
axios.defaults.withCredentials = true;

axios.interceptors.request.use((config) => {
    // Search for the jwt cookie
    const jwtToken = document.cookie.split(';').find(c => c.trim().startsWith('jwt='));
    if (jwtToken) {
        // Extract the token value and set it in the Authorization header
        config.headers.Authorization = `Bearer ${jwtToken.split('=')[1]}`;
    }
    return config;
});

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')

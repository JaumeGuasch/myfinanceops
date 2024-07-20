import './assets/main.css'
import {createApp} from 'vue'
import {createPinia} from 'pinia'
import App from './App.vue'
import axios from 'axios'
import router from './router';
import {useAuthStore} from "@/stores/auth";


export const api = axios.create({
    baseURL: 'http://localhost:8000/',
    withCredentials: true,
});

api.interceptors.request.use((config) => {
    const token = localStorage.getItem('token');
    if (token) {
        config.headers['Authorization'] = `Token ${token}`;
    }
    return config;
}, (error) => {
    return Promise.reject(error);
});
export default api;

const app = createApp(App)
app.config.globalProperties.$api = api;
const pinia = createPinia()
app.use(pinia)

const authStore = useAuthStore();
authStore.checkAuthStatus();


app.use(router);
app.mount('#app')


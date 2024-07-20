import {createRouter, createWebHistory} from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from "../views/LoginView.vue";
import OperationsView from "@/views/OperationsView.vue";
import HedgingView from "@/views/HedgingView.vue";
import SignupVIew from '@/views/SignupVIew.vue';
import {useAuthStore} from "@/stores/auth";

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/home/',
            name: 'home',
            component: HomeView,
            meta: {requiresAuth: true}
        },
        {
            path: '/login',
            name: 'login',
            component: LoginView
        },
        {
            path: '/signup',
            name: 'signup',
            component: SignupVIew
        },
        {
            path: '/operations',
            name: 'operations',
            component: OperationsView,
            meta: {requiresAuth: true}

        },
        {
            path: '/hedging',
            name: 'hedging',
            component: HedgingView,
            meta: {requiresAuth: true}

        },
        {
            path: '/about',
            name: 'about',
            component: () => import('../views/AboutView.vue')
        },
        {
            path: '/logout',
            name: 'logout',
            component: () => import('../views/LogoutView.vue'),
        }
    ]
})

router.beforeEach((to, from, next) => {
    const authStore = useAuthStore();
    authStore.checkAuthStatus(); // Ensure the check is performed before each navigation
    if (to.matched.some(record => record.meta.requiresAuth) && !authStore.isAuthenticated) {
        next({path: '/login'});
    } else {
        next();
    }
});

export default router;
// store/auth.ts
import {defineStore} from 'pinia';
import authService from '../services/authService';

interface User {
    email: string;
    password: string;
}

interface AuthState {
    user: User | null;
}

export const useAuthStore = defineStore('auth', {
    state: (): AuthState => ({
        user: JSON.parse(localStorage.getItem('user') as string) || null,
    }),
    actions: {
        async signup(email: string, password: string, name: string, surnames: string, organization: string) {
            try {
                const response = await authService.signup(email, password, name, surnames, organization);
                // Optionally update state or perform further actions on successful signup
            } catch (error) {
                console.error("There has been a problem with the sign up.", error);
                throw error;
            }
        },
        async login(email: string, password: string) {
            try {
                const response = await authService.login(email, password);
                if (response.user) {
                    this.user = response.user;
                    localStorage.setItem('user', JSON.stringify(this.user));
                }
            } catch (error) {
                console.error("Authentication failed. Please, check your credentials and try again", error);
                throw error;
            }
        },
        logout() {
            authService.logout();
            this.user = null;
            localStorage.removeItem('user');
        }
    }
});
// store/auth.ts
import {defineStore} from 'pinia';
import authService from '../services/authService';

interface User {
    email: string;
    password?: string;
    jwt?: string;
}

interface AuthState {
    user: User | null;
    isAuthenticated: boolean; // This can be determined by checking the presence of an HTTP-only cookie on the server-side
}

export const useAuthStore = defineStore('auth', {
    state: (): AuthState => ({
        user: null,
        isAuthenticated: false, // Initially not authenticated
    }),
    actions: {
        async signup(email: string, password: string, name: string, surnames: string, organization: string) {
            try {
                const response = await authService.signup(email, password, name, surnames, organization);
                // Handle signup success, potentially updating user state or redirecting
            } catch (error) {
                console.error("There has been a problem with the sign up.", error);
                throw error;
            }
        },
        async login(email: string, password: string) {
            try {
                const response = await authService.login(email, password);
                // Directly extract email and jwt from the response
                if (response.email && response.jwt) {
                    this.user = {email: response.email, jwt: response.jwt};
                    this.isAuthenticated = true;
                } else {
                    // Handle case where email or jwt is not present in the response
                    console.error('Login failed: JWT or user information is missing in the response');
                    throw new Error('Login failed: JWT or user information is missing in the response');
                }
            } catch (error) {
                console.error("Authentication failed.", error);
                throw error;
            }
        },
        logout() {
            try {
                authService.logout();
                localStorage.removeItem('jwt')
                this.user = null;
                this.isAuthenticated = false; // Update isAuthenticated to reflect logout
            } catch (error) {
                console.error("Logout failed.", error);
                throw error;
            }
        }
    }
});



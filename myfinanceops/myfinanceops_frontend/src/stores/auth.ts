import {defineStore} from 'pinia';
import {isAxiosError} from "axios";
import authService from '@/services/authService'; // Adjust the import path as necessary

interface UserType {
    email: string;
    name: string;
    surnames: string;
    organization: string;
    token: string;
}


export const useAuthStore = defineStore('auth', {
    state: () => ({
        loggedOut: true,
        error: "" as string,
        user: {} as UserType,
        loading: false,
        authInterval: null as ReturnType<typeof setInterval> | null,
        token: "" as string,
        isAuthenticated: false,
    }),
    actions: {
        async signup(email: string, password: string, name: string, surnames: string, organization: string) {
            this.loading = true;
            try {
                const {data: {user, token}} = await authService.signup(email, password, name, surnames, organization);
                this.user = user;
                localStorage.setItem('token', token);
                this.loggedOut = false;
                this.error = "";
            } catch (error) {
                console.error("There has been a problem with the sign up.", error);
                if (isAxiosError(error) && error.response) {
                    this.error = error.response.data.error;
                } else {
                    this.error = "An unexpected error occurred";
                }
            } finally {
                this.loading = false;
            }
        },
        async login(email: string, password: string) {
            this.loading = true;
            try {
                const response = await authService.login(email, password);
                const {token, user} = response;
                localStorage.setItem('token', token);
                localStorage.setItem('user', user.name)
                this.user = {...user, token};
                this.token = token;
                this.isAuthenticated = true;
                this.loggedOut = false;
                this.error = "";
            } catch (error) {
                console.error("There has been a problem with the login.", error);
                if (isAxiosError(error) && error.response) {
                    this.error = error.response.data.error;
                } else {
                    this.error = "An unexpected error occurred";
                }
                this.isAuthenticated = false;
            } finally {
                this.loading = false;
            }
        },
        checkAuthStatus() {
            const token = localStorage.getItem('token');
            this.isAuthenticated = !!token;
            if (token) {
                this.token = token;
                // Optionally, fetch user details here if needed
            }
        },
        logout() {
            localStorage.clear();
            this.isAuthenticated = false;
            this.loggedOut = true;
        },
    },
    getters: {
        userName: (state) => {
            // Return the user's name from localStorage if available
            return localStorage.getItem('user') || '';
        }
    }

});



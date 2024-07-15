// operationsStore.ts
import {defineStore} from 'pinia'
import axios from 'axios'

export const useOperationsStore = defineStore('operations', {
    state: () => ({
        operations: [],
        loading: false,
        error: null
    }),
    actions: {
        async fetchOperations() {
            this.loading = true;
            try {
                const response = await axios.get(import.meta.env.VITE_API_URL + 'operations/', {
                    withCredentials: true // Include credentials with the request
                });
                this.operations = response.data;
                this.error = null;
            } catch (error) {
                console.error("Operations listing failed.", error);
                throw error;
            } finally {
                this.loading = false;
            }
        }
    }
})
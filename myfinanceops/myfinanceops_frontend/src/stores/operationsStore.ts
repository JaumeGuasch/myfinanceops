import {defineStore} from 'pinia';
import operationsService from '@/services/operationsService';

type Operation = any; // Replace `any` with a more specific type structure if possible

export const useOperationsStore = defineStore('operations', {
    state: (): { operations: Record<string, any>[], loading: boolean, error: string | null } => ({
        operations: [],
        loading: false,
        error: null,
    }),
    actions: {
      async getOperations() {
            this.loading = true;
            try {
                const response = await operationsService.getOperations();
                console.log(response);
                this.operations = response;
                localStorage.setItem('operations', JSON.stringify(this.operations));
                this.loading = false;
            } catch (error) {
                this.error = error instanceof Error ? error.message : 'An error occurred';
                this.loading = false;
            }
        },
    },
});
import {defineStore} from 'pinia';
import operationsService from '@/services/operationsService';

// Define a type for the operation. Adjust this type according to the actual structure of your operation objects.
type Operation = any; // Replace `any` with a more specific type structure if possible

export const useOperationsStore = defineStore('operations', {
    state: (): { operations: Record<string, string>[], loading: boolean, error: string | null } => ({
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
                this.operations = response.map((operation: Operation) => {
                    const operationAsString: Record<string, string> = {};
                    Object.entries(operation).forEach(([key, value]) => {
                        operationAsString[key] = String(value);
                    });
                    console.log(operationAsString);
                    return operationAsString;
                });
                // Save the operations to localStorage
                localStorage.setItem('operations', JSON.stringify(this.operations));
                this.loading = false;
            } catch (error) {
                this.error = error instanceof Error ? error.message : 'An error occurred';
                this.loading = false;
            }
        },
    },
});
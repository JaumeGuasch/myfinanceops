<template>
  <div>
    <div class="operations-diary-header">
      <h1 class="header-style">Operation Details for ID: {{ operationId }}</h1>
      <div class="table-switch-buttons">
        <button @click="editOperation" class="button" title="Edit">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
               stroke="currentColor" class="size-6">
            <path stroke-linecap="round" stroke-linejoin="round"
                  d="m16.862 4.487 1.687-1.688a1.875 1.875 0 1 1 2.652 2.652L6.832 19.82a4.5 4.5 0 0 1-1.897 1.13l-2.685.8.8-2.685a4.5 4.5 0 0 1 1.13-1.897L16.863 4.487Zm0 0L19.5 7.125"/>
          </svg>
        </button>
        <button @click="deleteOperation" class="button" title="Delete">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
               stroke="currentColor" class="size-6">
            <path stroke-linecap="round" stroke-linejoin="round"
                  d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0"/>
          </svg>
        </button>
      </div>
    </div>
    <div class="operation-details">
      <div v-if="operationDetails">
        <p>Type: <input v-model="operationDetails.type" disabled/></p>
        <p>Date: <input v-model="operationDetails.date" type="date"/></p>
        <p>Market: <input v-model="operationDetails.market_name"/></p>
        <p>Trader: <input v-model="operationDetails.trader"/></p>
        <p>Description: <input v-model="operationDetails.description"/></p>
        <p>Created By: {{ operationDetails.created_by.name }} {{ operationDetails.created_by.surnames }}</p>
        <p>Modified By: {{ operationDetails.modified_by.name }} {{ operationDetails.modified_by.surnames }}</p>
        <p>Operation Chain: <input v-model="operationDetails.chain_number"/></p>
        <div v-for="field in specificFields" :key="field.name">
          <p>{{ field.label }}: <input v-model="operationDetails[field.name]" :type="field.type" /></p>
        </div>
        <div class="form-buttons">
          <button @click="confirmChanges" class="button">Confirm Changes</button>
          <button @click="cancelChanges" class="button">Cancel</button>
        </div>
      </div>
      <div v-else>
        <p>No details available for this operation.</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue';
import { useRoute } from 'vue-router';
import api from "@/main";

interface SpecificField {
  name: string;
  label: string;
  type: string;
  options?: string[];
}

const route = useRoute();
const operationId = route.params.operation_id;
const operationDetails = ref<Record<string, any> | null>(null);
const originalDetails = ref<Record<string, any> | null>(null);
const specificFields = ref<SpecificField[]>([]);

const fetchSpecificFields = async (type: string) => {
  try {
    let apiType;
    switch (type) {
      case 'Stock':
        apiType = 'stockoperation';
        break;
      case 'Futures':
        apiType = 'futuresoperation';
        break;
      case 'Options':
        apiType = 'optionsoperation';
        break;
      default:
        throw new Error('Invalid operation type');
    }

    const url = `api/operation-fields?type=${apiType}`;
    const response = await api.get(url);

    // Define common fields to exclude
    const commonFields = ['date', 'trader', 'market', 'description', 'operation_chain'];

    // Filter out common fields
    specificFields.value = response.data.filter((field: SpecificField) => !commonFields.includes(field.name));
    console.log('Specific fields fetched:', specificFields.value);
  } catch (error) {
    console.error('Error fetching specific fields:', error);
  }
};

onMounted(() => {
  console.log(`Fetching details for operation ID: ${operationId}`);
  const storedOperations = localStorage.getItem('operations');
  if (storedOperations) {
    const operationsList = JSON.parse(storedOperations);
    const operation = operationsList.find((op: any) => op.id === operationId);
    if (operation) {
      console.log('Operation details found:', operation);
      operationDetails.value = { ...operation };
      originalDetails.value = { ...operation };
      fetchSpecificFields(operation.type);
    } else {
      console.log('No operation details found for this ID.');
    }
  } else {
    console.log('No operations found in localStorage.');
  }
});

const confirmChanges = async () => {
  try {
    const plainObject = JSON.parse(JSON.stringify(operationDetails.value));
    delete plainObject.created_by;
    delete plainObject.modified_by;

    console.log('Request body:', plainObject);

    const response = await api.put('/api/update-operation', plainObject);
    console.log('Operation updated successfully:', response.data);

    const storedOperations = localStorage.getItem('operations');
    if (storedOperations) {
      const operationsList = JSON.parse(storedOperations);
      const index = operationsList.findIndex((op: any) => op.id === operationId);
      if (index !== -1) {
        operationsList[index] = plainObject;
        localStorage.setItem('operations', JSON.stringify(operationsList));
      }
    }
  } catch (error) {
    console.error('Error updating operation:', error);
  }
};

const cancelChanges = () => {
  operationDetails.value = { ...originalDetails.value };
};
</script>

<style scoped>
.operations-diary-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 32px;
  border: 2px solid #a0aec0;
  border-radius: 6px;
  margin-top: 1%;
  transition: margin-right 0.3s ease;
  margin-right: var(-30%, 0%);
  background-color: #ffffff;
}

.header-style {
  text-transform: uppercase;
  font-weight: bolder;
  font-size: 24px;
  color: #374151;
  text-align: center;
  padding: 8px;
  background-color: #ffffff;
}

.table-switch-buttons {
  display: flex;
  gap: 20px;
}

.button {
  background-color: #4f46e5;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  display: flex;
  align-items: center;
  gap: 8px;
}

.button:hover {
  background-color: #4338ca;
}

.button svg.size-6 {
  width: 24px;
  height: 24px;
}

.operation-details {
  padding: 16px;
  border: 1px solid #a0aec0;
  border-radius: 8px;
  margin-top: 16px;
  background-color: #f9fafb;
}

.operation-details p {
  margin: 8px 0;
}

.form-buttons {
  display: flex;
  gap: 10px;
  margin-top: 16px;
}
</style>
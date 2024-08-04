<template>
  <div class="operations-diary">
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
        <button @click="() => deleteOperation(operationId)" class="button" title="Delete">
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
        <div class="common-fields">
          <h3 class="section-title">Common fields</h3>
          <div class="field">
            <label for="operation_chain">Operation Chain:</label>
            <select id="operation_chain" v-model="operationDetails.operation_chain" class="custom-input"
                    :disabled="!isEditable">
              <option value="" selected>Link to new chain of operations</option>
              <option v-for="chain in operationChains" :key="chain.id" :value="chain.chain_number">{{
                  chain.chain_number
                }}
              </option>
            </select>
          </div>
          <div class="fields-grid">
            <div v-for="field in commonFields" :key="field.name" class="field">
              <label :for="field.name">{{ field.label }}:</label>
              <input
                  v-if="['text', 'number', 'date', 'email', 'password', 'tel', 'url', 'datetime-local', 'month', 'week', 'time', 'color'].includes(field.type)"
                  :id="field.name" v-model="operationDetails[field.name]" :type="field.type" class="custom-input"
                  :disabled="!isEditable"/>
              <select v-if="field.type === 'select'" :id="field.name" v-model="operationDetails[field.name]"
                      class="custom-input" :disabled="!isEditable">
                <option v-for="option in field.options" :key="option" :value="option">{{ option }}</option>
              </select>
              <textarea v-if="field.type === 'textarea'" :id="field.name" v-model="operationDetails[field.name]"
                        class="custom-input" :disabled="!isEditable"></textarea>
            </div>
          </div>
        </div>
        <div class="specific-fields">
          <h3 class="section-title">Specific fields</h3>
          <div class="fields-grid">
            <div v-for="field in specificFields" :key="field.name" class="field">
              <label :for="field.name">{{ field.label }}:</label>
              <input v-if="field.type === 'text'" :id="field.name" v-model="operationDetails[field.name]"
                     :type="field.type" class="custom-input" :disabled="!isEditable"/>
              <input v-if="field.type === 'number'" :id="field.name" v-model="operationDetails[field.name]"
                     :type="field.type" class="custom-input" :disabled="!isEditable"/>
              <input v-if="field.type === 'date'" :id="field.name" v-model="operationDetails[field.name]"
                     :type="field.type" class="custom-input" :disabled="!isEditable"/>
              <select v-if="field.type === 'select'" :id="field.name" v-model="operationDetails[field.name]"
                      class="custom-input" :disabled="!isEditable">
                <option v-for="option in field.options" :key="option" :value="option">{{ option }}</option>
              </select>
            </div>
          </div>
        </div>
        <div class="form-buttons">
          <button @click="confirmChanges" class="button" :disabled="!isEditable">Confirm Changes</button>
          <button @click="cancelChanges" class="button" :disabled="!isEditable">Cancel</button>
        </div>
      </div>
      <div v-else>
        <p>No details available for this operation.</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">import {ref, onMounted} from 'vue';
import {useRoute} from 'vue-router';
import api from "@/main";
import router from "@/router";

interface SpecificField {
  name: string;
  label: string;
  type: string;
  options?: string[];
}

const route = useRoute();
let operationId = route.params.operation_id;
if (Array.isArray(operationId)) {
  operationId = operationId[0];
}
const operationDetails = ref<Record<string, any> | null>(null);
const originalDetails = ref<Record<string, any> | null>(null);
const specificFields = ref<SpecificField[]>([]);
const commonFields = ref<SpecificField[]>([]);
const isEditable = ref(false);
const operationChains = ref<any[]>([]);

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
    const commonFieldNames = ['date', 'trader', 'market', 'description', 'operation_chain'];
    specificFields.value = response.data.filter((field: SpecificField) => !commonFieldNames.includes(field.name));
    commonFields.value = response.data.filter((field: SpecificField) => commonFieldNames.includes(field.name));
    console.log('Specific fields fetched:', specificFields.value);
    console.log('Common fields fetched:', commonFields.value);
  } catch (error) {
    console.error('Error fetching specific fields:', error);
  }
};

const fetchOperationChains = async () => {
  try {
    const response = await api.get('/api/get-all-operation-chain');
    operationChains.value = response.data;
    console.log('Operation chains fetched:', operationChains.value);
  } catch (error) {
    console.error('Error fetching operation chains:', error);
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
      operationDetails.value = {...operation};
      originalDetails.value = {...operation};
      fetchSpecificFields(operation.type);
    } else {
      console.log('No operation details found for this ID.');
    }
  } else {
    console.log('No operations found in localStorage.');
  }
  fetchOperationChains().then(() => {
    if (operationDetails.value && operationDetails.value.operation_chain) {
      const existingChain = operationChains.value.find(chain => chain.id === operationDetails.value!.operation_chain);
      if (existingChain) {
        operationDetails.value.operation_chain = existingChain.chain_number;
      } else {
        operationChains.value.push({
          id: operationDetails.value.operation_chain,
          chain_number: operationDetails.value.operation_chain
        });
      }
    }
  });
});

const confirmChanges = async () => {
  try {
    const plainObject = JSON.parse(JSON.stringify(operationDetails.value));
    delete plainObject.created_by;
    delete plainObject.modified_by;

    // Ensure the operation_chain is correctly set before updating
    const existingChain = operationChains.value.find(chain => chain.chain_number === plainObject.operation_chain);
    if (existingChain) {
      plainObject.operation_chain = existingChain.id;
    } else {
      plainObject.operation_chain = operationDetails.value!.operation_chain;
    }

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

const deleteOperation = async (id: string) => {
  try {
    const response = await api.delete('/api/delete-operation', {
      data: {id}
    });
    if (response.status === 200) {
      console.log('Operation deleted successfully');
      await router.push('/operations');
    } else {
      console.error('Failed to delete operation:', response.data.error);
    }
  } catch (error) {
    console.error('Error deleting operation:', error);
  }
};

const cancelChanges = () => {
  operationDetails.value = {...originalDetails.value};
  isEditable.value = false;
};

const editOperation = () => {
  isEditable.value = true;
};

defineExpose({
  deleteOperation,
});
</script>

<style src="@/assets/button-styles.css"></style>

<style>
.operations-diary-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 32px;
  border: 2px solid #a0aec0;
  border-radius: 6px;
  margin-top: 1%;
  transition: margin-right 0.3s ease;
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

.common-fields, .specific-fields {
  padding: 16px;
  border: 1px solid #a0aec0;
  border-radius: 8px;
  margin-top: 16px;
  background-color: #ffffff;
}

.fields-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
}

.field {
  margin-bottom: 16px;
}

.field label {
  display: block;
  margin-bottom: 8px;
}

.field input, .field select, .field textarea {
  width: 100%;
  padding: 8px;
  border: 1px solid #a0aec0;
  border-radius: 4px;
  box-sizing: border-box;
}

.section-title {
  padding: 12px 0;
  font-size: 18px;
  font-weight: 500;
  border-bottom: 2px solid #a0aec0;
  margin-bottom: 16px;
}

.custom-input {
  width: 100%;
  height: 50%;
  padding: 8px;
}

.form-buttons {
  display: flex;
  justify-content: flex-end;
  gap: 16px;
  margin-top: 16px;
}
</style>
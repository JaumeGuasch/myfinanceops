<template>
  <div class="create-operation">
    <div class="operations-diary-header">
      <h1 class="header-style">Create Operation</h1>
    </div>
    <div class="dropdown-section-container">
      <div class="dropdown-section">
        <label for="operation-type" class="dropdown-label">Select Operation Type:</label>
        <select id="operation-type" v-model="selectedType" class="dropdown">
          <option v-for="type in operationTypes" :key="type.type" :value="type">{{ type.label }}</option>
        </select>
      </div>
    </div>
    <div v-if="specificFields.length > 0" class="operation-details">
      <div class="common-fields">
        <h3 class="section-title">Common fields</h3>
        <div class="field">
          <label for="operation_chain">Operation Chain:</label>
          <select id="operation_chain" v-model="formData.operation_chain" class="custom-input">
            <option value="" selected>Link to new chain of operations</option>
            <option v-for="chain in operationChains" :key="chain.id" :value="chain.chain_number">{{ chain.chain_number }}</option>
          </select>
        </div>
        <div class="fields-grid">
          <div v-for="field in commonFields" :key="field.name" class="field">
            <label :for="field.name">{{ field.label }}:</label>
            <input
                v-if="['text', 'number', 'date', 'email', 'password', 'tel', 'url', 'datetime-local', 'month', 'week', 'time', 'color'].includes(field.type)"
                :id="field.name" v-model="formData[field.name]" :type="field.type" class="custom-input"/>
            <select v-if="field.type === 'select'" :id="field.name" v-model="formData[field.name]" class="custom-input">
              <option v-for="option in field.options" :key="option" :value="option">{{ option }}</option>
            </select>
            <textarea v-if="field.type === 'textarea'" :id="field.name" v-model="formData[field.name]" class="custom-input"></textarea>
          </div>
        </div>
      </div>
      <div class="specific-fields">
        <h3 class="section-title">Specific fields</h3>
        <div class="fields-grid">
          <div v-for="field in specificFields" :key="field.name" class="field">
            <label :for="field.name">{{ field.label }}:</label>
            <input v-if="field.type === 'text'" :id="field.name" v-model="formData[field.name]" :type="field.type" class="custom-input"/>
            <input v-if="field.type === 'number'" :id="field.name" v-model="formData[field.name]" :type="field.type" class="custom-input"/>
            <input v-if="field.type === 'date'" :id="field.name" v-model="formData[field.name]" :type="field.type" class="custom-input"/>
            <select v-if="field.type === 'select'" :id="field.name" v-model="formData[field.name]" class="custom-input">
              <option v-for="option in field.options" :key="option" :value="option">{{ option }}</option>
            </select>
          </div>
        </div>
      </div>
    </div>
    <div class="table-switch-buttons">
      <button class="button" @click="handleSubmit">Create Operation</button>
    </div>
  </div>
</template>


<script setup lang="ts">
import {ref, onMounted, watch} from 'vue';
import api from "@/main";

interface SelectedType {
  type: string;
  name: string;
  label: string;
}

interface SpecificField {
  name: string;
  label: string;
  type: string;
  options?: string[];
}

interface OperationType {
  type: string;
  label: string;
}

interface OperationChain {
  id: string;
  chain_number: string;
}

const operationTypes = ref<OperationType[]>([]);
const selectedType = ref<SelectedType>({type: '', name: '', label: ''});
const specificFields = ref<SpecificField[]>([]);
const commonFields = ref<SpecificField[]>([]);
const formData = ref<Record<string, any>>({operation_chain: ''});
const operationChains = ref<OperationChain[]>([]);

const fetchOperationTypes = async () => {
  try {
    const response = await api.get('api/operation-types');
    operationTypes.value = response.data.operation_types;
  } catch (error) {
    console.error('Error fetching operation types:', error);
  }
};

const fetchSpecificFields = async (type: string) => {
  try {
    const url = `api/operation-fields?type=${type}`;
    const response = await api.get(url);
    const data = response.data;
    specificFields.value = Array.isArray(data) ? data.filter(field => !commonFieldNames.includes(field.name)) : [];
    commonFields.value = Array.isArray(data) ? data.filter(field => commonFieldNames.includes(field.name)) : [];
    initializeFormData();
  } catch (error) {
    console.error('Error fetching specific fields:', error);
  }
};

const fetchOperationChains = async (type: string) => {
  try {
    const response = await api.get(`api/get-all-operation-chain?type=${type}`);
    operationChains.value = response.data;
  } catch (error) {
    console.error('Error fetching operation chains:', error);
  }
}

watch(selectedType, (newType) => {
  if (newType.type) {
    fetchSpecificFields(newType.type);
    fetchOperationChains(newType.type);
  }
});

const commonFieldNames = ['date', 'trader', 'market'];

const initializeFormData = () => {
  if (Array.isArray(specificFields.value)) {
    specificFields.value.forEach(field => {
      formData.value[field.name] = '';
    });
  }
  if (Array.isArray(commonFields.value)) {
    commonFields.value.forEach(field => {
      formData.value[field.name] = '';
    });
  }
};

const handleSubmit = async () => {
  try {
    const payload: Record<string, any> = {
      type: selectedType.value.type,
      operation_chain: formData.value.operation_chain || null,
      date: formData.value.date,
      trader: formData.value.trader,
      market: formData.value.market,
      transaction_type: formData.value.transaction_type,
      specific_fields: {}
    };

    if (selectedType.value.type === 'stockoperation') {
      payload.specific_fields = {
        stock_code: formData.value.stock_code,
        shares_amount: formData.value.shares_amount,
        price_per_share: formData.value.price_per_share
      };
    } else if (selectedType.value.type === 'futuresoperation') {
      payload.specific_fields = {
        contract: formData.value.contract,
        price_per_contract: formData.value.price_per_contract
      };
    } else if (selectedType.value.type === 'futuresoptionsoperation') {
      payload.specific_fields = {
        strike_price: formData.value.strike_price,
        premium: formData.value.premium,
        price_per_contract: formData.value.price_per_contract
      };
    }

    console.log('Payload:', JSON.stringify(payload, null, 2));

    const response = await api.post('api/create-operation', payload, {
      headers: {
        'Content-Type': 'application/json',
      },
    });
    console.log('Operation created successfully:', response.data);
    // Handle success (e.g., show a success message, redirect, etc.)
  } catch (error) {
    console.error('Error creating operation:', error);
    // Handle error (e.g., show an error message)
  }
};

onMounted(() => {
  fetchOperationTypes();
});

watch(selectedType, (newType) => {
  if (newType.type) {
    fetchSpecificFields(newType.type);
  }
});
</script>


<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

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

.dropdown-section-container {
  max-width: 300px;
  margin-top: 16px;
  padding: 8px;
}

.dropdown-section {
  padding: 8px;
}

.dropdown-label {
  display: block;
  margin-bottom: 8px;
  font-weight: bold;
}

.dropdown {
  width: 100%;
  padding: 8px;
  border: 1px solid #a0aec0;
  border-radius: 4px;
  box-sizing: border-box;
  background-color: #ffffff;
}

.table-switch-buttons {
  display: flex;
  gap: 20px;
  margin-top: 16px;
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

.operation-details {
  padding: 16px;
  border: 1px solid #a0aec0;
  border-radius: 8px;
  margin-top: 16px;
  background-color: #f9fafb;
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
  border: 1px solid #a0aec0;
  border-radius: 4px;
  box-sizing: border-box;
  background-color: #ffffff;
  font-size: 16px;
  color: #374151;
  transition: border-color 0.3s ease, box-shadow 0.3s ease;
}

.custom-input:focus {
  border-color: #4f46e5;
  box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.3);
}
</style>
<template>
  <div>
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
              <option v-for="chain in operationChains" :key="chain.id" :value="chain.chain_number">{{
                  chain.chain_number
                }}
              </option>
            </select>
          </div>
          <div class="fields-grid">
            <div v-for="field in commonFields" :key="field.name" class="field">
              <label :for="field.name">{{ field.label }}:</label>
              <template v-if="field.name === 'market'">
                <div class="dropdown" @click="toggleDropdown">
                  <div class="dropbtn">{{ formData.market || 'Select a market...' }}</div>
                  <div v-if="dropdownOpen" class="dropdown-content" @click.stop>
                    <input type="text" v-model="searchQuery" @input="filterMarkets" placeholder="Search markets..."
                           class="custom-input"/>
                    <div v-for="market in filteredMarkets" :key="market.id" @click="selectMarket(market.name)"
                         class="dropdown-item">
                      {{ market.name }}
                    </div>
                  </div>
                </div>
              </template>
              <template v-else>
                <input
                    v-if="['text', 'number', 'date', 'email', 'password', 'tel', 'url', 'datetime-local', 'month', 'week', 'time', 'color'].includes(field.type)"
                    :id="field.name" v-model="formData[field.name]" :type="field.type" class="custom-input"/>
                <select v-if="field.type === 'select'" :id="field.name" v-model="formData[field.name]"
                        class="custom-input">
                  <option v-for="option in field.options" :key="option" :value="option">{{ option }}</option>
                </select>
                <textarea v-if="field.type === 'textarea'" :id="field.name" v-model="formData[field.name]"
                          class="custom-input"></textarea>
              </template>
            </div>
          </div>
        </div>

        <div class="specific-fields">
          <h3 class="section-title">Specific fields</h3>
          <div class="fields-grid">
            <div v-for="field in specificFields" :key="field.name" class="field">
              <label :for="field.name">{{ field.label }}:</label>
              <input v-if="field.type === 'text'" :id="field.name" v-model="formData[field.name]" :type="field.type"
                     class="custom-input"/>
              <input v-if="field.type === 'number'" :id="field.name" v-model="formData[field.name]" :type="field.type"
                     class="custom-input"/>
              <input v-if="field.type === 'date'" :id="field.name" v-model="formData[field.name]" :type="field.type"
                     class="custom-input"/>
              <select v-if="field.type === 'select'" :id="field.name" v-model="formData[field.name]"
                      class="custom-input">
                <option v-for="option in field.options" :key="option" :value="option">{{ option }}</option>
              </select>
            </div>
          </div>
        </div>

        <div class="commissions-section">
          <h3 class="section-title">Commissions</h3>
          <div class="buttons-commission">
            <button class="button" @click="addCommission">Add Commission</button>
            <button class="button" @click="deleteCommission">Delete Commission</button>
          </div>
          <table class="table-auto">
            <thead>
            <tr>
              <th>Commission Name</th>
              <th>Calcuation mode</th>
              <th>Amount</th>
              <th>Currency</th>
              <th>Actions</th>
            </tr>
            </thead>
            <tbody>
            <tr v-for="(commission, index) in formData.commissions" :key="index">
              <td>
                <select v-model="commission.name" class="custom-input">
                  <option v-for="option in commissionOptions" :key="option.id" :value="option.name">{{
                      option.name
                    }}
                  </option>
                </select>
              </td>
              <td>
                <select v-model="commission.type" class="custom-input">
                  <option v-for="option in commissionTypeOptions" :key="option" :value="option">{{ option }}</option>
                </select>
              </td>
              <td>
                <input type="number" v-model="commission.amount" class="custom-input"/>
              </td>
              <td>
                <button @click="removeCommission(index)">Delete</button>
              </td>
            </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
    <div class="table-switch-buttons">
      <button class="button" @click="handleSubmit">Create Operation</button>
    </div>
    <div v-if="showPopup" class="success-checkmark">
      <div class="checkmark-wrapper">
        <div class="check-icon">
          <span class="icon-line line-tip"></span>
          <span class="icon-line line-long"></span>
          <div class="icon-circle"></div>
          <div class="icon-fix"></div>
        </div>
      </div>
    </div>
  </div>
</template>


<script setup lang="ts">import {ref, onMounted, watch, computed} from 'vue';
import api from '@/main';
import '@/assets/success-tick.css';

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

interface Market {
  id: number;
  name: string;
}

interface Commission {
  id: number;
  name: string;
}

const operationTypes = ref<OperationType[]>([]);
const selectedType = ref<SelectedType>({type: '', name: '', label: ''});
const specificFields = ref<SpecificField[]>([]);
const commonFields = ref<SpecificField[]>([]);
const formData = ref<Record<string, any>>({market: '', operation_chain: ''});
const operationChains = ref<OperationChain[]>([]);
const markets = ref<Market[]>([]);
const searchQuery = ref('');
const dropdownOpen = ref(false);
const showPopup = ref(false);
const commissionOptions = ref<Commission[]>([]);
const commissionTypeOptions = ref(['Per share', 'Per contract', 'Total']);

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
};

const fetchMarkets = async () => {
  try {
    const response = await api.get('/api/get-markets');
    console.log('Markets:', response.data)
    markets.value = (response.data as Market[]).sort((a, b) => a.name.localeCompare(b.name));
  } catch (error) {
    console.error('Error fetching markets:', error);
  }
};

const filteredMarkets = computed<Market[]>(() => {
  return markets.value.filter(market =>
      market.name.toLowerCase().includes(searchQuery.value.toLowerCase())
  );
});


const fetchCommissionsOptions = async () => {
  try {
    const response = await api.get('api/get-commissions');
    commissionOptions.value = response.data;
  } catch (error) {
    console.error('Error fetching commissions:', error);
  }
};
const setCommissionTypeOptions = () => {
  const type = formData.value.type;
  if (type === 'stock') {
    commissionTypeOptions.value = ['Per share', 'Total'];
  } else if (type === 'futures' || type === 'options') {
    commissionTypeOptions.value = ['Per contract', 'Total'];
  }
};

const addCommission = () => {
  formData.value.commissions.push({name: '', type: '', amount: 0});
};

const removeCommission = (index: number) => {
  formData.value.commissions.splice(index, 1);
};

const toggleDropdown = () => {
  dropdownOpen.value = !dropdownOpen.value;
};

const filterMarkets = () => {
};

const selectMarket = (marketName: string) => {
  formData.value.market = marketName;
  dropdownOpen.value = false;
};

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
    const payload = {
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

    showPopup.value = true;

    setTimeout(() => {
      window.location.href = '/operations/';
    }, 1000);

  } catch (error) {
    console.error('Error creating operation:', error);
  }
};

onMounted(() => {
  fetchOperationTypes();
  fetchMarkets();
});

watch(selectedType, (newType) => {
  if (newType.type) {
    fetchSpecificFields(newType.type);
  }
});
</script>

<style src="@/assets/button-styles.css"></style>
<style src="@/assets/page-header.css"></style>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
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

.dropdown {
  position: relative;
  display: inline-block;
  cursor: pointer;
}

.dropdown-content {
  display: block;
  position: absolute;
  background-color: #f9f9f9;
  min-width: 160px;
  box-shadow: 0px 8px 16px 0px rgba(0, 0, 0, 0.2);
  z-index: 1;
  border-radius: 4px;
  padding: 2%;
  margin-top: 8px; /* Add spacing from the clickable dropdown div */
  max-height: 200px; /* Set maximum height */
  overflow-y: auto; /* Make it scrollable if content exceeds max height */
}

.custom-input {
  width: 100%;
  padding: 8px;
  margin-bottom: 8px; /* Add spacing between the search box and the dropdown items */
}

.dropdown-item {
  padding: 8px 16px;
  cursor: pointer;
}

.dropdown-item:hover {
  background-color: #ddd;
}

.buttons-commission {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.buttons-commission .button {
  background-color: #4f46e5;
  color: white;
  border: none;
  padding: 6px 12px;
  border-radius: 12px;
  cursor: pointer;
}

th, td {
  border: 2px solid #ddd;
  text-align: left;
  padding: 6px;
  color: #4b5563;
  white-space: nowrap; /* Prevents text from wrapping */
}

th {
  background-color: #4f46e5;
  color: #ffffff;
  text-align: center;
}

tr:nth-child(even) {
  background-color: #f7fafc;
}

.table-auto {
  border: 2px solid transparent;
  border-collapse: collapse;
  border-spacing: 0;
  width: 100%;
  margin-top: 1%;
  border-radius: 8px;
  overflow: hidden;
  background-color: #ffffff;
}

th:first-child {
  border-top-left-radius: 12px;
}

th:last-child {
  border-top-right-radius: 12px;
}

tr:last-child td:first-child {
  border-bottom-left-radius: 12px;
}

tr:last-child td:last-child {
  border-bottom-right-radius: 12px;
}

.table-auto th {
  font-size: 16px;
}

.table-auto td {
  font-size: 14px;
}

tbody tr:nth-child(odd) {
  background-color: #ffffff;
}

tbody tr:nth-child(even) {
  background-color: #d8e4f0;
}
</style>
<template>
  <main :style="{ 'margin-right': showPopup ? '30%' : '0' }">
    <div class="operations-diary-header">
      <h1 class="header-style">operations diary</h1>
      <div class="flex items-center">
        <div :class="{ 'showPopup': showPopup }">
          <button @click="togglePopup" class="py-2 px-4 bg-purple-600 text-white rounded-lg ml-2">
            <!-- filter icon -->
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                 stroke="currentColor" class="size-6">
              <path stroke-linecap="round" stroke-linejoin="round"
                    d="M12 3c2.755 0 5.455.232 8.083.678.533.09.917.556.917 1.096v1.044a2.25 2.25 0 0 1-.659 1.591l-5.432 5.432a2.25 2.25 0 0 0-.659 1.591v2.927a2.25 2.25 0 0 1-1.244 2.013L9.75 21v-6.568a2.25 2.25 0 0 0-.659-1.591L3.659 7.409A2.25 2.25 0 0 1 3 5.818V4.774c0-.54.384-1.006.917-1.096A48.32 48.32 0 0 1 12 3Z"/>
            </svg>
          </button>
          <div class="popup-container" v-if="showPopup">
            <div class="popup-panel">
              <div v-for="(options, columnName) in columnVisibility" :key="columnName"
                   class="checkbox-container items-center">
                <input type="checkbox" v-model="options.visible" :id="columnName">
                <label :for="columnName" class="search-label">{{ columnName }}
                  <input type="text" v-model="options.searchTerm" class="ml-2 search-input" placeholder="Search...">
                </label>
              </div>
              <div class="flex justify-end">
                <button @click="showPopup = false" class="py-2 px-4 mt-2">
                  Close
                </button>
              </div>
            </div>
          </div>
        </div>
        <button class="py-2 px-4 bg-purple-600 text-white rounded-lg ml-2">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
               stroke="currentColor" class="size-6">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15"/>
          </svg>
        </button>
      </div>
    </div>
    <!-- Separate div for the operations table -->
    <div class="table-wrapper">
      <div v-if="loading" class="text-center py-4">Loading...</div>
      <div v-if="error" class="text-red-500">Failed to load operations: {{ error }}</div>
      <table v-if="!loading && operations" class="table-auto divide-y divide-gray-200 mt-4 w-full">
        <thead class="bg-gray-50">
        <tr>
          <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
              v-if="columnVisibility.id.visible">
            ID
          </th>
          <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
              v-if="columnVisibility.type.visible">
            Type
          </th>
          <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
              v-if="columnVisibility.date.visible">
            Date
          </th>
          <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
              v-if="columnVisibility.market.visible">
            Market
          </th>
          <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
              v-if="columnVisibility.trader.visible">
            Trader
          </th>
          <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
              v-if="columnVisibility.description.visible">
            Description
          </th>
        </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
        <tr v-for="operation in filteredOperations" :key="operation.id">
          <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500" v-if="columnVisibility.id.visible">{{
              operation.id
            }}
          </td>
          <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500" v-if="columnVisibility.type.visible">{{
              operation.type
            }}
          </td>
          <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500" v-if="columnVisibility.date.visible">{{
              operation.date
            }}
          </td>
          <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500" v-if="columnVisibility.market.visible">{{
              operation.market_name
            }}
          </td>
          <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500" v-if="columnVisibility.trader.visible">{{
              operation.trader
            }}
          </td>
          <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500" v-if="columnVisibility.description.visible">
            {{ operation.description }}
          </td>
        </tr>
        </tbody>
      </table>
    </div>
  </main>
</template>


<script setup lang="ts">
import {onMounted, ref, watch, computed} from 'vue';
import {useOperationsStore} from "@/stores/operationsStore";

interface Operation {
  id: number;
  type: string;
  date: string;
  market_name: string;
  trader: string;
  description: string;
}

const operations = ref<Operation[]>([]);
const loading = ref(false);
const error = ref(null);
const showPopup = ref(false);
const columnVisibility = ref({
  id: {visible: true, searchTerm: ''},
  type: {visible: true, searchTerm: ''},
  date: {visible: true, searchTerm: ''},
  market: {visible: true, searchTerm: ''},
  trader: {visible: true, searchTerm: ''},
  description: {visible: true, searchTerm: ''},
});

const operationsStore = useOperationsStore();

onMounted(() => {
  operationsStore.fetchOperations();
});

function togglePopup() {
  showPopup.value = !showPopup.value;
}

// Watch for changes in column visibility and save to localStorage
watch(columnVisibility, (newValue) => {
  localStorage.setItem('columnVisibility', JSON.stringify(newValue));
}, {deep: true});

watch(showPopup, (newValue) => {
  console.log('showPopup changed to:', newValue);
}, {immediate: true});

const filteredOperations = computed(() => {
  return operations.value.filter(operation => {
    return Object.entries(columnVisibility.value).every(([key, {visible, searchTerm}]) => {
      if (!visible) return true;
      if (!searchTerm) return true;
      const value = operation[key as keyof Operation]?.toString().toLowerCase() ?? '';
      return value.includes(searchTerm.toLowerCase());
    });
  });
});
</script>


<style scoped>

.operations-diary-header, .table-wrapper {
  transition: margin-right 0.3s ease;
  margin-right: var(-30%, 0%);

}

.header-style {
  text-transform: uppercase;
  font-weight: bolder;
  font-size: 24px;
  background-color: #f3f4f6;
  color: #1f2937;
  text-align: center;
  padding: 8px;
}

.table-auto {
  border-collapse: collapse;
  width: 100%;
}

th, td {
  border: 2px solid #ddd;
  text-align: left;
  padding: 8px;
}

th {
  background-color: #f3f4f6;
  color: #1f2937;
  text-align: center;
}

tr:nth-child(even) {
  background-color: #f7fafc;
}

th:first-child, td:first-child {
  width: 50px;
  text-align: center;
}

.table-auto {
  border: 1px solid transparent;
  border-collapse: collapse;
  border-spacing: 0;
  width: 100%;
  margin: 0;
}

.table-auto th {
  font-size: 18px;
}

.table-auto td {
  font-size: 14px;
}

.table-wrapper {
  border: 4px solid lightslategrey;
  border-radius: 4px;
  overflow: hidden;
  padding: 0;
  width: 100%;
  margin-left: 0;
  margin-top: 2%;
}

.popup-panel {
  border: 2px solid #e5e7eb;
  padding: 20px;
  border-radius: 8px;

}

.operations-diary-header, .table-wrapper {
  z-index: 1;
  position: relative;
}

.popup-container {
  margin-top: 2%;
  width: 25%;
  text-transform: uppercase;
  justify-content: center;
  align-items: normal;
  position: fixed;
  overflow-y: auto;
  right: 2%;
  border-radius: 8px;
}

.checkbox-container {
  display: flex;
  align-items: center;
  margin-bottom: 16px;
}

.checkbox-container input[type="checkbox"] {
  display: none;
}

.search-label {
  margin-right: 8px;
}

.search-input {
  margin-left: 8px;
  flex-grow: 1;
}

.checkbox-container input[type="checkbox"] + label {
  position: relative;
  padding-left: 30px;
  cursor: pointer;
}

.checkbox-container input[type="checkbox"] + label::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  width: 18px;
  height: 18px;
  background-color: #f9fafb;
  border: 2px solid #d1d5db;
  border-radius: 4px;
}

.checkbox-container input[type="checkbox"]:checked + label::after {
  content: '';
  position: absolute;
  left: 6px;
  top: 2px;
  width: 6px;
  height: 10px;
  border: solid #4f46e5;
  border-width: 0 2px 2px 0;
  transform: rotate(45deg);
}

.checkbox-container label {
  font-size: 16px;
  font-weight: 500;
  color: #374151;
}

button {
  background-color: #4f46e5;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: #4338ca;
}

.operations-diary-header {
  margin-top: 2%;
  padding: 8px 32px;
  border: 1px solid #ddd;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
</style>
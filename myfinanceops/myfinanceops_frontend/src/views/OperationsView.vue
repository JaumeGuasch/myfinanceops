<template>
  <main :style="{ 'margin-right': showPopup ? '30%' : '0' }">
    <div class="operations-diary-header">
      <h1 class="header-style">operations diary</h1>
      <div class="table-switch-buttons">
        <button @click="setTableView('Stock')"
                :class="{'active-button': isActiveButton('Stock'), 'inactive-button': !isActiveButton('Stock')}"
                class="table-switch-button">Stocks
        </button>
        <button @click="setTableView('Futures')"
                :class="{'active-button': isActiveButton('Futures'), 'inactive-button': !isActiveButton('Futures')}"
                class="table-switch-button">Futures
        </button>
        <button @click="setTableView('Options')"
                :class="{'active-button': isActiveButton('Options'), 'inactive-button': !isActiveButton('Options')}"
                class="table-switch-button">Options
        </button>
      </div>
      <div class="flex items-center">
        <div :class="{ 'showPopup': showPopup }">
          <button @click="togglePopup" class="py-2 px-4 bg-purple-600 text-white rounded-lg ml-2">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                 stroke="currentColor" class="size-6">
              <path stroke-linecap="round" stroke-linejoin="round"
                    d="M12 3c2.755 0 5.455.232 8.083.678.533.09.917.556.917 1.096v1.044a2.25 2.25 0 0 1-.659 1.591l-5.432 5.432a2.25 2.25 0 0 0-.659 1.591v2.927a2.25 2.25 0 0 1-1.244 2.013L9.75 21v-6.568a2.25 2.25 0 0 0-.659-1.591L3.659 7.409A2.25 2.25 0 0 1 3 5.818V4.774c0-.54.384-1.006.917-1.096A48.32 48.32 0 0 1 12 3Z"/>
            </svg>
          </button>
          <div class="popup-container" v-if="showPopup">
            <div class="popup-panel">
              <div v-for="(columnDetail, columnName) in headers" :key="columnName"
                   class="checkbox-container items-center">
                <input type="checkbox" v-model="columnDetail.visible" @click="toggleVisibility(columnName)"
                       :id="columnName">
                <label :for="columnName" class="search-label">{{ columnDetail.name }}
                  <input type="text" v-model="columnDetail.searchTerm" class="ml-2 search-input"
                         placeholder="Search...">
                </label>
              </div>
              <div class="flex justify-end">
                <button @click="resetFilters" class="py-2 px-4 mt-2 mr-2"> Reset Filters
                </button>
                <button @click="showPopup = false" class="py-2 px-4 mt-2">
                  Close
                </button>
              </div>
            </div>
          </div>
        </div>
        <button class="py-2 px-4 bg-purple-600 text-white rounded-lg ml-2" title="Add operation"
                @click="redirectToAddOperation">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
               stroke="currentColor" class="size-6">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15"/>
          </svg>
        </button>
        <button class="py-2 px-4 bg-purple-600 text-white rounded-lg ml-2" title="Settings" @click="redirectToSettings">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="size-6">
            <path fill-rule="evenodd"
                  d="M11.078 2.25c-.917 0-1.699.663-1.85 1.567L9.05 4.889c-.02.12-.115.26-.297.348a7.493 7.493 0 0 0-.986.57c-.166.115-.334.126-.45.083L6.3 5.508a1.875 1.875 0 0 0-2.282.819l-.922 1.597a1.875 1.875 0 0 0 .432 2.385l.84.692c.095.078.17.229.154.43a7.598 7.598 0 0 0 0 1.139c.015.2-.059.352-.153.43l-.841.692a1.875 1.875 0 0 0-.432 2.385l.922 1.597a1.875 1.875 0 0 0 2.282.818l1.019-.382c.115-.043.283-.031.45.082.312.214.641.405.985.57.182.088.277.228.297.35l.178 1.071c.151.904.933 1.567 1.85 1.567h1.844c.916 0 1.699-.663 1.85-1.567l.178-1.072c.02-.12.114-.26.297-.349.344-.165.673-.356.985-.57.167-.114.335-.125.45-.082l1.02.382a1.875 1.875 0 0 0 2.28-.819l.923-1.597a1.875 1.875 0 0 0-.432-2.385l-.84-.692c-.095-.078-.17-.229-.154-.43a7.614 7.614 0 0 0 0-1.139c-.016-.2.059-.352.153-.43l.84-.692c.708-.582.891-1.59.433-2.385l-.922-1.597a1.875 1.875 0 0 0-2.282-.818l-1.02.382c-.114.043-.282.031-.449-.083a7.49 7.49 0 0 0-.985-.57c-.183-.087-.277-.227-.297-.348l-.179-1.072a1.875 1.875 0 0 0-1.85-1.567h-1.843ZM12 15.75a3.75 3.75 0 1 0 0-7.5 3.75 3.75 0 0 0 0 7.5Z"
                  clip-rule="evenodd"/>
          </svg>
        </button>
      </div>
    </div>
    <!-- Separate div for the operations table -->
    <table v-if="!loading && operations" class="table-auto divide-y divide-gray-200 mt-4 w-full">
      <thead class="bg-gray-50">
      <tr>
        <template v-for="(columnDetail, columnName) in headers" :key="columnName">
          <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
              v-if="columnDetail.visible">
            {{ columnDetail.name }}
          </th>
        </template>
      </tr>
      </thead>
      <tbody class="bg-white divide-y divide-gray-200">
      <tr v-for="operation in filteredOperations" :key="operation.id">
        <template v-for="(columnDetail, columnName) in headers" :key="columnName">
          <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500" v-if="columnDetail.visible">
        <span v-if="columnName === 'id'">
          <a @click="goToOperationDetail(operation.id)" class="text-blue-500 cursor-pointer">
            {{ operation[columnName as keyof Operation] }}
          </a>
        </span>
            <span v-else>
          {{ operation[columnName as keyof Operation] }}
        </span>
          </td>
        </template>
      </tr>
      </tbody>
    </table>
  </main>
</template>


<script setup lang="ts">
import {onMounted, ref, watch, computed, reactive} from 'vue';
import {useOperationsStore} from "@/stores/operationsStore";
import {useRouter} from 'vue-router';


interface Operation {
  id: number;
  type: string;
  date: string;
  market_name: string;
  trader: string;
  description: string;
  shares: number;
  contract: string;
  price: number;
  strike_price: number;
  call_put: string;
}

const operations = ref<Operation[]>([]);
const loading = ref(true);
const showPopup = ref(false);
const operationsStore = useOperationsStore();
const currentTableView = ref<TableView>('Stock'); // Default to 'Stocks'
const isActiveButton = computed(() => (view: string) => view === currentTableView.value);
const router = useRouter();

type TableView = 'Stock' | 'Futures' | 'Options';

interface ColumnDetail {
  name: string;
  visible: boolean;
  searchTerm: string;
}

function loadHeadersFromLocalStorage() {
  const views: TableView[] = ['Stock', 'Futures', 'Options'];
  views.forEach((view) => {
    const savedHeadersJSON = localStorage.getItem(`${view}Headers`);
    if (savedHeadersJSON) {
      const savedHeaders = JSON.parse(savedHeadersJSON);
      // Ensure the structure for each view exists in tableHeaders
      if (!tableHeaders[view]) {
        tableHeaders[view] = {};
      }
      // Update tableHeaders for the view with the loaded configuration
      Object.keys(savedHeaders).forEach((key) => {
        if (savedHeaders[key] !== undefined) {
          // Initialize or update the column detail for each key in the view
          tableHeaders[view][key] = savedHeaders[key];
        }
      });
    }
  });
}

const headers = computed(() => {
  return tableHeaders[currentTableView.value];
});


const tableHeaders = reactive<Record<TableView, Record<string, ColumnDetail>>>({
  Stock: {
    id: {name: 'ID', visible: true, searchTerm: ''},
    type: {name: 'Type', visible: true, searchTerm: ''},
    stock_code: {name: 'Stock', visible: true, searchTerm: ''},
    date: {name: 'Date', visible: true, searchTerm: ''},
    market_name: {name: 'Market', visible: true, searchTerm: ''},
    trader: {name: 'Trader', visible: true, searchTerm: ''},
    shares_amount: {name: 'Shares', visible: true, searchTerm: ''},
    description: {name: 'Description', visible: true, searchTerm: ''},
  },
  Futures: {
    id: {name: 'ID', visible: true, searchTerm: ''},
    type: {name: 'Type', visible: true, searchTerm: ''},
    date: {name: 'Date', visible: true, searchTerm: ''},
    market_name: {name: 'Market', visible: true, searchTerm: ''},
    contract: {name: 'Contract', visible: true, searchTerm: ''},
    price: {name: 'Price', visible: true, searchTerm: ''},
    description: {name: 'Description', visible: true, searchTerm: ''},
  },
  Options: {
    id: {name: 'ID', visible: true, searchTerm: ''},
    type: {name: 'Type', visible: true, searchTerm: ''},
    date: {name: 'Date', visible: true, searchTerm: ''},
    market_name: {name: 'Market', visible: true, searchTerm: ''},
    contract: {name: 'Contract', visible: true, searchTerm: ''},
    strike_price: {name: 'Strike Price', visible: true, searchTerm: ''},
    call_put: {name: 'Call/Put', visible: true, searchTerm: ''},
  },
});

function setTableView(view: TableView) {
  currentTableView.value = view;
}

onMounted(async () => {
  loadHeadersFromLocalStorage();
  console.log("Loading operations...");
  await operationsStore.getOperations(); // Fetch operations and store them in localStorage
  operations.value = loadOperations(); // Directly set the operations ref with the loaded operations
  console.log("Operations loaded!");
  loading.value = false;
});

const loadOperations = () => {
  const operationsJSON = localStorage.getItem('operations');
  const operations = operationsJSON ? JSON.parse(operationsJSON) : [];
  return operations.sort((a: Operation, b: Operation) => new Date(b.date).getTime() - new Date(a.date).getTime());
};

function togglePopup() {
  showPopup.value = !showPopup.value;
}

watch(showPopup, (newValue) => {
  console.log('showPopup changed to:', newValue);
}, {immediate: true});


function toggleVisibility(columnName: string) {
  const savedHeaders = headers.value; // Current headers from the reactive state
  savedHeaders[columnName].visible = !savedHeaders[columnName].visible;
  localStorage.setItem(`${currentTableView.value}Headers`, JSON.stringify(savedHeaders));
}

watch(() => tableHeaders, (newVal, oldVal) => {
  filterOperationsBasedOnSearch();
}, {deep: true});

function filterOperationsBasedOnSearch() {
  const currentHeaders = tableHeaders[currentTableView.value];
  operations.value = loadOperations().filter((operation: Operation) => {
    let matchesSearchTerms = true;
    for (const [columnName, columnDetail] of Object.entries(currentHeaders)) {
      if (columnDetail.visible && columnDetail.searchTerm) {
        const operationValue = operation[columnName as keyof Operation]?.toString().toLowerCase() || '';
        if (!operationValue.includes(columnDetail.searchTerm.toLowerCase())) {
          matchesSearchTerms = false;
          break;
        }
      }
    }
    return matchesSearchTerms;
  });
}

const filteredOperations = computed(() => {
  return operations.value.filter(operation => operation.type.toLowerCase() === currentTableView.value.toLowerCase());
});

function resetFilters() {
  const currentHeaders = tableHeaders[currentTableView.value];
  Object.keys(currentHeaders).forEach(columnName => {
    currentHeaders[columnName].visible = true; // Set all columns to be visible
    currentHeaders[columnName].searchTerm = ''; // Clear the search term
  });
  // Save the updated headers to localStorage
  localStorage.setItem(`${currentTableView.value}Headers`, JSON.stringify(currentHeaders));
  // Trigger UI update if necessary
  filterOperationsBasedOnSearch(); // Assuming this method updates the displayed operations based on filters
}

const redirectToAddOperation = () => {
  router.push('/operations/new');
};

const redirectToSettings = () => {
  router.push('/operations/settings');
};

const goToOperationDetail = (operationId: number) => {
  router.push(`/operations/${operationId}`);
};

</script>

<style scoped>

.operations-diary-header {
  transition: margin-right 0.3s ease;
  margin-right: var(-30%, 0%);
  background-color: #ffffff; /* Replace #f0f0f0 with your desired color */
}

.header-style {
  text-transform: uppercase;
  font-weight: bolder;
  font-size: 24px;
  color: #374151; /* Slightly darker grey tone */
  text-align: center;
  padding: 8px;
  background-color: #ffffff;
}

th, td {
  border: 2px solid #ddd;
  text-align: left;
  padding: 8px;
  color: #4b5563;
}

th {
  background-color: #4f46e5;
  color: #ffffff;
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
  border: 2px solid transparent;
  border-collapse: collapse;
  border-spacing: 0;
  width: 100%;
  margin-top: 1%;
  border-radius: 8px; /* Adjust this value to increase or decrease the roundness */
  overflow: hidden; /* Ensures the inner elements do not overflow the rounded corners */
  background-color: #ffffff; /* Replace #f0f0f0 with your desired color */


}

th:first-child {
  border-top-left-radius: 12px; /* Match the table's border-radius */
}

th:last-child {
  border-top-right-radius: 12px; /* Match the table's border-radius */
}

tr:last-child td:first-child {
  border-bottom-left-radius: 12px; /* Match the table's border-radius */
}

tr:last-child td:last-child {
  border-bottom-right-radius: 12px; /* Match the table's border-radius */
}

.table-auto th {
  font-size: 18px;
}

.table-auto td {
  font-size: 16px;
}

tbody tr:nth-child(odd) {
  background-color: #ffffff; /* White for odd rows */
}

tbody tr:nth-child(even) {
  background-color: #d8e4f0; /* Light blue for even rows */
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

.active-button {
  background-color: #4f46e5; /* Active color */
  color: white;
}

.inactive-button {
  background-color: #d1d5db; /* Greyed out for inactive */
  color: #4b5563;
}

.table-switch-button {
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.operations-diary-header {
  display: flex;
  align-items: center;
  justify-content: space-between; /* This ensures the title and button group are on opposite ends */
  padding: 8px 32px;
  border: 2px solid #a0aec0;
  border-radius: 6px;
  margin-top: 1%;
}

.table-switch-buttons {
  display: flex;
  gap: 20px; /* Adjust the gap size as needed */
}
</style>
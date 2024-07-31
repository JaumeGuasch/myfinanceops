<script setup lang="ts">
import {ref, onMounted} from 'vue';
import api from "@/main";

// Define the type for market data
interface Market {
  mic: string;
  name: string;
  currency: string;
  trading_days?: string[];
  notes: string;
}

const markets = ref<Market[]>([]);
const selectedMarkets = ref(new Set<Market>());

onMounted(async () => {
  try {
    const response = await api.get('/api/get-markets');
    markets.value = response.data;
  } catch (error) {
    console.error('Error fetching markets:', error);
  }
});

const toggleSelection = (market: Market) => {
  if (selectedMarkets.value.has(market)) {
    selectedMarkets.value.delete(market);
  } else {
    selectedMarkets.value.add(market);
  }
};

const deleteSelectedMarkets = () => {
  // Implement delete logic here
  console.log('Deleting selected markets:', Array.from(selectedMarkets.value));
};

const addMarket = () => {
  // Implement add logic here
  console.log('Adding new market');
};



</script>

<template>
  <div class="settings-container">
    <div class="settings-section">
      <div class="header">
        <h2>Market Settings</h2>
        <div class="buttons">
          <button @click="addMarket">Add</button>
          <button @click="deleteSelectedMarkets">Delete</button>
        </div>
      </div>
      <div class="market-list">
        <div class="table-container">
          <table>
            <thead>
              <tr>
                <th></th>
                <th>MIC</th>
                <th>Market name</th>
                <th>Currency</th>
                <th>Opening days</th>
                <th>Notes</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="market in markets" :key="market.mic">
                <td><input type="checkbox" @change="toggleSelection(market)"/></td>
                <td>{{ market.mic }}</td>
                <td>{{ market.name }}</td>
                <td>{{ market.currency }}</td>
                <td>{{ market.trading_days ? market.trading_days.join(', ') : 'N/A' }}</td>
                <td>{{ market.notes }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
    <div class="settings-section">
      <h2>Commissions</h2>
      <p>Define all possible types of commissions here...</p>
    </div>
    <div class="settings-section">
      <h2>Company Settings</h2>
      <p>Define company settings here...</p>
    </div>
  </div>
</template>

<style scoped>
.settings-container {
  display: flex;
  flex-direction: row;
  gap: 20px;
  padding: 20px;
  background-color: #f9fafb;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.settings-section {
  background-color: #ffffff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  flex: 1; /* Ensures equal width for each column */
}

.settings-section h2 {
  margin-bottom: 10px;
  font-size: 24px;
  color: #4f46e5;
}

.settings-section p {
  font-size: 16px;
  color: #374151;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

button {
  background-color: #4f46e5;
  color: white;
  border: none;
  padding: 6px 12px; /* Smaller padding */
  border-radius: 12px; /* More rounded corners */
  cursor: pointer;
}

.buttons {
  display: flex;
  gap: 10px;
}

.market-list {
  overflow-x: auto;
}

.table-container {
  width: 100%;
  overflow-x: auto;
  padding-bottom: 20px; /* Add padding to create space between the table and the scrollbar */
}

table {
  width: 150%; /* Set a width larger than the container to enable horizontal scrolling */
  border-collapse: collapse;
}

th, td {
  padding: 8px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

th {
  background-color: #f4f4f4;
}

tr:hover {
  background-color: #f1f1f1;
}
</style>
<script setup lang="ts">
import {ref, onMounted} from 'vue';
import api from "@/main";

interface Market {
  id: number;
  mic: string;
  name: string;
  currency: string;
  trading_days?: string[];
  notes: string;
}

interface NewMarket {
  mic: string;
  name: string;
  currency: string;
  trading_days?: string[];
  notes: string;
}

interface Commission {
  id: number;
  name: string;
}

interface NewCommission {
  name: string;
}

interface TradingCompany {
  id: number;
  name: string;
  country: string;
}

interface TradingAccount {
  id: number;
  trading_company: string;
  account_number: string;
  currency: string;
}

interface NewTradingAccount {
  trading_company_id: number;
  account_number: string;
  currency: string;
}

const markets = ref<Market[]>([]);
const selectedMarkets = ref(new Set<Market>());
const showPopup = ref(false);
const newMarket = ref<NewMarket>({
  mic: '',
  name: '',
  currency: '',
  trading_days: [],
  notes: ''
});
const message = ref('');
const dayChoices = [
  {value: 'MON', text: 'Monday'},
  {value: 'TUE', text: 'Tuesday'},
  {value: 'WED', text: 'Wednesday'},
  {value: 'THU', text: 'Thursday'},
  {value: 'FRI', text: 'Friday'},
  {value: 'SAT', text: 'Saturday'},
  {value: 'SUN', text: 'Sunday'},
];
const commissions = ref<Commission[]>([]);
const selectedCommissions = ref(new Set<Commission>());
const showCommissionPopup = ref(false);
const newCommission = ref<NewCommission>({
  name: ''
});
const countryChoices = ref<{ code: string; name: string }[]>([]);
const showTradingCompanyPopup = ref(false);
const newTradingCompany = ref<Omit<TradingCompany, 'id'>>({
  name: '',
  country: ''
});
const tradingCompanies = ref<TradingCompany[]>([]);
const selectedTradingCompanies = ref(new Set<TradingCompany>());
const tradingAccounts = ref<TradingAccount[]>([]);
const selectedTradingAccounts = ref(new Set<TradingAccount>());
const showTradingAccountPopup = ref(false);
const newTradingAccount = ref<NewTradingAccount>({
  trading_company_id: 0,
  account_number: '',
  currency: ''
});
const currencyChoices = ref<{ code: string; name: string }[]>([]);

const toggleSelection = (market: Market) => {
  if (selectedMarkets.value.has(market)) {
    selectedMarkets.value.delete(market);
  } else {
    selectedMarkets.value.add(market);
  }
};

const toggleCommissionSelection = (commission: Commission) => {
  if (selectedCommissions.value.has(commission)) {
    selectedCommissions.value.delete(commission);
  } else {
    selectedCommissions.value.add(commission);
  }
};

const addMarket = () => {
  showPopup.value = true;
};

const addCommission = () => {
  showCommissionPopup.value = true;
};

const addTradingCompany = () => {
  showTradingCompanyPopup.value = true;
};

const closeMarketPopup = () => {
  showPopup.value = false;
  message.value = '';
};

const closeCommissionPopup = () => {
  showCommissionPopup.value = false;
  message.value = '';
};

const closeTradingCompanyPopup = () => {
  showTradingCompanyPopup.value = false;
  message.value = '';
};

const closeTradingAccountPopup = () => {
  showTradingAccountPopup.value = false;
  message.value = '';
};

const submitMarket = async () => {
  try {
    const response = await api.post('/api/create-market', newMarket.value);
    markets.value.push(response.data.market);
    closeMarketPopup();
  } catch (error) {
    const err = error as any;
    console.log('Error creating market:', err.response.data);
  }
};

const submitCommission = async () => {
  try {
    const response = await api.post('/api/create-commission', newCommission.value);
    commissions.value.push(response.data.commission);
    closeCommissionPopup();
  } catch (error) {
    const err = error as any;
    console.log('Error creating commission:', err.response.data);
  }
};

const deleteSelectedMarkets = async () => {
  try {
    const marketIds = Array.from(selectedMarkets.value).map(market => market.id);
    await api.post('/api/delete-market', {ids: marketIds});
    markets.value = markets.value.filter(market => !selectedMarkets.value.has(market));
    selectedMarkets.value.clear();
  } catch (error) {
    console.error('Error deleting markets:', error);
  }
};

const deleteSelectedCommissions = async () => {
  try {
    const commissionIds = Array.from(selectedCommissions.value).map(commission => commission.id);
    await api.post('/api/delete-commission', {ids: commissionIds});
    commissions.value = commissions.value.filter(commission => !selectedCommissions.value.has(commission));
    selectedCommissions.value.clear();
  } catch (error) {
    console.error('Error deleting commissions:', error);
  }
};

const fetchCountryChoices = async () => {
  try {
    const response = await api.get('/api/country-choices');
    countryChoices.value = response.data;
  } catch (error) {
    console.error('Error fetching country choices:', error);
  }
};

const fetchTradingCompanies = async () => {
  try {
    const response = await api.get('/api/get-trading-companies');
    tradingCompanies.value = response.data;
  } catch (error) {
    console.error('Error fetching trading companies:', error);
  }
};

const submitTradingCompany = async () => {
  try {
    const response = await api.post('/api/create-trading-company', newTradingCompany.value);
    tradingCompanies.value.push(response.data.tradingCompany);
    closeTradingCompanyPopup();
  } catch (error) {
    console.error('Error creating trading company:', error);
  }
};

const deleteTradingCompany = async () => {
  try {
    const companyNames = Array.from(selectedTradingCompanies.value).map(company => company.name);
    await api.delete('/api/delete-trading-company', {data: {names: companyNames}});
    tradingCompanies.value = tradingCompanies.value.filter(company => !selectedTradingCompanies.value.has(company));
    selectedTradingCompanies.value.clear();
  } catch (error) {
    console.error('Error deleting trading companies:', error);
  }
};

const toggleTradingCompanySelection = (company: TradingCompany) => {
  if (selectedTradingCompanies.value.has(company)) {
    selectedTradingCompanies.value.delete(company);
  } else {
    selectedTradingCompanies.value.add(company);
  }
};

const fetchTradingAccounts = async () => {
  try {
    const response = await api.get('/api/get-trading-accounts');
    tradingAccounts.value = response.data;
  } catch (error) {
    console.error('Error fetching trading accounts:', error);
  }
};

const toggleTradingAccountSelection = (account: TradingAccount) => {
  if (selectedTradingAccounts.value.has(account)) {
    selectedTradingAccounts.value.delete(account);
  } else {
    selectedTradingAccounts.value.add(account);
  }
};

const submitTradingAccount = async () => {
  try {
    const response = await api.post('/api/add-trading-account', newTradingAccount.value);
    console.log('response:', response);
    tradingAccounts.value.push(response.data.tradingAccount);
    showTradingAccountPopup.value = false;
  } catch (error) {
    console.error('Error creating trading account:', error);
  }
};

const deleteSelectedTradingAccounts = async () => {
  try {
    const accountIds = Array.from(selectedTradingAccounts.value).map(account => account.id);
    if (accountIds.length === 0) {
      console.error('No trading accounts selected for deletion');
      return;
    }
    const response = await api.delete('/api/delete-trading-account', {data: {ids: accountIds}});
    console.log('response:', response);
    tradingAccounts.value = tradingAccounts.value.filter(account => !selectedTradingAccounts.value.has(account));
    selectedTradingAccounts.value.clear();
  } catch (error) {
    console.error('Error deleting trading accounts:', error);
  }
};

const fetchCurrencyChoices = async () => {
  try {
    const response = await api.get('/api/currency-choices');
    currencyChoices.value = response.data;
  } catch (error) {
    console.error('Error fetching currency choices:', error);
  }
};

onMounted(async () => {
  try {
    const response_market = await api.get('/api/get-markets');
    markets.value = response_market.data;
    const response_commission = await api.get('/api/get-commissions');
    commissions.value = response_commission.data;
    await fetchTradingCompanies();
    await fetchTradingAccounts(); // Fetch trading accounts on mount
    await fetchCountryChoices();
    await fetchCurrencyChoices();
  } catch (error) {
    console.error('Error fetching markets or commissions:', error);
  }
});
</script>

<template>
  <div class="settings-container">
    <div class="settings-section">
      <h2>Market Settings</h2>
      <div class="buttons-and-list">
        <div class="buttons">
          <button @click="addMarket">Add</button>
          <button @click="deleteSelectedMarkets">Delete</button>
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
      <div v-if="showPopup" class="overlay"></div>
      <div v-if="showPopup" class="popup">
        <div class="popup-content">
          <h2>Add Market</h2>
          <form @submit.prevent="submitMarket">
            <div class="form-group">
              <label for="name">Name: </label>
              <input type="text" id="name" v-model="newMarket.name" required/>
            </div>

            <div class="form-group">
              <label for="mic">MIC: </label>
              <input type="text" id="mic" v-model="newMarket.mic" required/>
            </div>

            <div class="form-group">
              <label for="currency">Currency: </label>
              <input type="text" id="currency" v-model="newMarket.currency" required/>
            </div>

            <div class="form-group">
              <div class="label-container">
                <label for="trading_days">Trading days:</label>
                <div class="checkbox-group">
                  <label v-for="day in dayChoices" :key="day.value">
                    <input type="checkbox" :value="day.value" v-model="newMarket.trading_days"/>
                    {{ day.text }}
                  </label>
                </div>
              </div>
            </div>
            <div class="form-group">
              <textarea id="notes" v-model="newMarket.notes"
                        placeholder="Add any additional notes or relevant market information here..."></textarea>
            </div>
            <div class="form-buttons">
              <button type="submit">Submit</button>
              <button type="button" @click="closeMarketPopup">Cancel</button>
            </div>
          </form>
        </div>
      </div>
    </div>
    <div class="settings-section">
      <h2>Commissions Settings</h2>
      <div class="buttons-and-list">
        <div class="buttons">
          <button @click="addCommission">Add</button>
          <button @click="deleteSelectedCommissions">Delete</button>
        </div>
        <div class="commission-list">
          <div class="table-container">
            <table>
              <thead>
              <tr>
                <th></th>
                <th>Commission Name</th>
              </tr>
              </thead>
              <tbody>
              <tr v-for="commission in commissions" :key="commission.id">
                <td><input type="checkbox" @change="toggleCommissionSelection(commission)"/></td>
                <td>{{ commission.name }}</td>
              </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
      <div v-if="showCommissionPopup" class="overlay"></div>
      <div v-if="showCommissionPopup" class="popup">
        <div class="popup-content">
          <h2>Add Commission</h2>
          <form @submit.prevent="submitCommission">
            <div class="form-group">
              <label for="commission-name">Name: </label>
              <input type="text" id="commission-name" v-model="newCommission.name" required/>
            </div>
            <div class="form-buttons">
              <button type="submit">Add</button>
              <button type="button" @click="closeCommissionPopup">Cancel</button>
            </div>
          </form>
        </div>
      </div>
    </div>
    <!-- Company Settings Section -->
    <div class="settings-section">
      <h2>Company Settings</h2>
    </div>
    <!-- Trading companies settings here -->
    <div class="settings-section">
      <h2>Trading companies</h2>
      <div class="buttons-and-list">
        <div class="buttons">
          <button @click="addTradingCompany">Add</button>
          <button @click="deleteTradingCompany">Delete</button>
        </div>
        <div class="trading-company-list">
          <div class="table-container">
            <table>
              <thead>
              <tr>
                <th></th>
                <th>Trading company</th>
                <th>Country</th>
              </tr>
              </thead>
              <tbody>
              <tr v-for="company in tradingCompanies" :key="company.name">
                <td><input type="checkbox" @change="toggleTradingCompanySelection(company)"/></td>
                <td>{{ company.name }}</td>
                <td>{{ company.country }}</td>
              </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
      <div v-if="showTradingCompanyPopup" class="overlay"></div>
      <div v-if="showTradingCompanyPopup" class="popup">
        <div class="popup-content">
          <h2>Add Trading Company</h2>
          <form @submit.prevent="submitTradingCompany">
            <div class="form-group">
              <label for="company-name">Name: </label>
              <input type="text" id="company-name" v-model="newTradingCompany.name" required/>
            </div>
            <div class="form-group">
              <label for="company-country">Country: </label>
              <select id="company-country" v-model="newTradingCompany.country" required>
                <option v-for="country in countryChoices" :key="country.code" :value="country.code">
                  {{ country.name }}
                </option>
              </select>
            </div>
            <div class="form-buttons">
              <button type="submit">Add</button>
              <button type="button" @click="closeTradingCompanyPopup">Cancel</button>
            </div>
          </form>
        </div>
      </div>
    </div>
    <div class="settings-section">
      <h2>Trading Accounts</h2>
      <div class="buttons-and-list">
        <div class="buttons">
          <button @click="showTradingAccountPopup = true">Add</button>
          <button @click="deleteSelectedTradingAccounts">Delete</button>
        </div>
        <div class="trading-account-list">
          <div class="table-container">
            <table>
              <thead>
              <tr>
                <th></th>
                <th>Trading Company</th>
                <th>Account Number</th>
                <th>Currency</th>
              </tr>
              </thead>
              <tbody>
              <tr v-for="account in tradingAccounts" :key="account.id">
                <td><input type="checkbox" @change="toggleTradingAccountSelection(account)"/></td>
                <td>{{ account.trading_company }}</td>
                <td>{{ account.account_number }}</td>
                <td>{{ account.currency }}</td>
              </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
      <div v-if="showTradingAccountPopup" class="overlay"></div>
      <div v-if="showTradingAccountPopup" class="popup">
        <div class="popup-content">
          <h2>Add Trading Account</h2>
          <form @submit.prevent="submitTradingAccount">
            <div class="form-group">
              <label for="trading-company">Trading Company: </label>
              <select id="trading-company" v-model="newTradingAccount.trading_company_id" required>
                <option v-for="company in tradingCompanies" :key="company.id" :value="company.id">
                  {{ company.name }}
                </option>
              </select>
            </div>
            <div class="form-group">
              <label for="account-number">Account Number: </label>
              <input type="text" id="account-number" v-model="newTradingAccount.account_number" required/>
            </div>
            <div class="form-group">
              <label for="currency">Currency: </label>
              <select v-model="newTradingAccount.currency">
                <option v-for="currency in currencyChoices" :key="currency.code" :value="currency.code">
                  {{ currency.name }}
                </option>
              </select></div>
            <div class="form-buttons">
              <button type="submit">Add</button>
              <button type="button" @click="closeTradingAccountPopup">Cancel</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<style>
.settings-container {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
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
  flex: 1;
}

.settings-section h2 {
  margin-bottom: 20px;
  font-size: 24px;
  color: #4f46e5;
}

.settings-section p {
  font-size: 16px;
  color: #374151;
}

button {
  background-color: #4f46e5;
  color: white;
  border: none;
  padding: 6px 12px;
  border-radius: 12px;
  cursor: pointer;
}

.buttons {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.market-list {
  overflow-x: auto;
}

.table-container {
  width: 100%;
  /* Remove overflow-x: auto; */
  padding-bottom: 20px;
}

table {
  width: 100%; /* Adjust width to 100% */
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

.popup {
  width: 400px;
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  z-index: 1000;
}

.popup-content {
  display: flex;
  flex-direction: column;
}

.popup-content h2 {
  margin-bottom: 10px;
}

.popup-content .form-group {
  margin-bottom: 15px;
}

.popup-content .form-group label {
  margin-bottom: 20px; /* Add space between the label and the input */
}

.popup-content .checkbox-group {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
  justify-items: start;
}

.popup-content .checkbox-group label {
  display: flex;
  align-items: center;
}

.popup-content .checkbox-group input[type="checkbox"] {
  margin-right: 5px;
  transform: scale(1.2);
}

.popup-content .label-container {
  display: flex;
  flex-direction: column;
  margin-bottom: 10px;
}

.popup-content input,
.popup-content textarea {
  width: 100%;
  margin-top: 5px;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.popup-content button {
  margin-top: 10px;
  padding: 8px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.popup-content button[type="submit"] {
  background-color: #4f46e5;
  color: white;
}

.popup-content button[type="button"] {
  background-color: #d1d5db;
  color: #4b5563;
}

.popup-content .form-buttons {
  display: flex;
  gap: 10px;
  margin-top: 20px;
  justify-content: flex-end;
}

.overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 1000;
  backdrop-filter: blur(2px); /* Apply blur effect to the entire overlay */
}

.popup-content select {
  width: 100%;
  margin-top: 5px;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
  background-color: #ffffff;
}

</style>
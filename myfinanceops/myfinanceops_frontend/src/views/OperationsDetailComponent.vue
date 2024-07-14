<template>
  <div>
    <h2>Operation Details</h2>
    <form>
      <div>
        <label>Date:</label>
        <input type="date" v-model="operation.date" disabled>
      </div>
      <div>
        <label>Market:</label>
        <input type="text" v-model="operation.market.name" disabled>
      </div>
      <div>
        <label>Trader:</label>
        <input type="text" v-model="operation.trader" disabled>
      </div>
      <div>
        <label>Description:</label>
        <textarea v-model="operation.description" disabled></textarea>
      </div>
      <!-- Add more fields as necessary -->
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      operation: {} // This will hold the operation details
    };
  },
  mounted() {
    this.fetchOperationDetails();
  },
  methods: {
    fetchOperationDetails() {
      const operationId = this.$route.params.id;
      // Implement fetching logic here using operationId
      // this.operation = fetchedOperationDetails;
    }
  }
}
</script>
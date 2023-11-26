<template>
  <v-form>
    <v-container>
      <v-row>
        <v-col>
          <h1> Patients </h1>

          <v-card>
            <v-tabs
              v-model="tab"
              bg-color="primary"
            >
              <v-tab value="Orders">Orders</v-tab>
              <v-tab value="Results">Results</v-tab>
              <v-tab value="Billing">Billing</v-tab>
            </v-tabs>

            <v-card-text>
              <v-window v-model="tab">
                <v-window-item value="Orders">

                  <v-table>
                    <thead>
                      <tr>
                        <th class="text-left"> order_date </th>
                        <th class="text-left"> order_id </th>
                        <th class="text-left"> ordering_physician </th>
                        <th class="text-left"> status </th>
                        <th class="text-left"> test_name </th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr
                        v-for="item in orders"
                        :key="item.name"
                      >
                        <td>{{ item.order_date }}</td>
                        <td>{{ item.order_id }}</td>
                        <td>{{ item.ordering_physician }}</td>
                        <td>{{ item.status }}</td>
                        <td>{{ item.test_name }}</td>
                      </tr>
                    </tbody>
                  </v-table>
                </v-window-item>

                <v-window-item value="Results">
                  <v-table>
                    <thead>
                      <tr>
                        <th class="text-left"> result_id </th>
                        <th class="text-left"> order_id </th>
                        <th class="text-left"> report_url </th>
                        <th class="text-left"> interpretation </th>
                        <th class="text-left"> reporting_pathologist </th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr
                        v-for="item in results"
                        :key="item.name"
                      >
                        <td>{{ item.result_id }}</td>
                        <td>{{ item.order_id }}</td>
                        <td>{{ item.report_url }}</td>
                        <td>{{ item.interpretation }}</td>
                        <td>{{ item.reporting_pathologist }}</td>
                      </tr>
                    </tbody>
                  </v-table>
                </v-window-item>

                <v-window-item value="Billing">          
                  <v-table>
                    <thead>
                      <tr>
                        <th class="text-left"> bill_id </th>
                        <th class="text-left"> order_id </th>
                        <th class="text-left"> billed_amount </th>
                        <th class="text-left"> payment_status </th>
                        <th class="text-left"> insurance_claim_status </th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr
                        v-for="item in bills"
                        :key="item.name"
                      >
                        <td>{{ item.bill_id }}</td>
                        <td>{{ item.order_id }}</td>
                        <td>{{ item.billed_amount }}</td>
                        <td>{{ item.payment_status }}</td>
                        <td>{{ item.insurance_claim_status }}</td>
                      </tr>
                    </tbody>
                  </v-table>
                </v-window-item>
              </v-window>
            </v-card-text>
          </v-card>
          
        </v-col>
      </v-row>
    </v-container>
  </v-form>
</template>

<script>
export default {
  mounted() {
    this.getOrder()
    this.getResults()
    this.getBills()
  },
  data() {
    return {
      tab: null,
      orders: null,
      results: null,
      bills: null,
    };
  },
  methods: {
    getOrder(){
      var updateAPI = process.env.VUE_APP_API_URL + "/getOrder"
      var obj = JSON.parse(sessionStorage.user)
      var name = obj["User info"]["name"]
      var id = obj["User info"]["id"]
      var pwHash = obj["User info"]["pwHash"]
      
      fetch(updateAPI, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          name: name,
          id: id,
          pwHash: pwHash,
        })
      })
      .then((response) => response.json())
      .then((post) => {
        this.orders = post
        console.log(this.orders)
      })
    },
    getResults(){
      var updateAPI = process.env.VUE_APP_API_URL + "/getResults"
      var obj = JSON.parse(sessionStorage.user)
      var name = obj["User info"]["name"]
      var id = obj["User info"]["id"]
      var pwHash = obj["User info"]["pwHash"]
      
      fetch(updateAPI, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          name: name,
          id: id,
          pwHash: pwHash,
        })
      })
      .then((response) => response.json())
      .then((post) => {
        this.results = post
        console.log(this.results)
      })
    },
    getBills(){
      var updateAPI = process.env.VUE_APP_API_URL + "/getBills"
      var obj = JSON.parse(sessionStorage.user)
      var name = obj["User info"]["name"]
      var id = obj["User info"]["id"]
      var pwHash = obj["User info"]["pwHash"]
      
      fetch(updateAPI, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          name: name,
          id: id,
          pwHash: pwHash,
        })
      })
      .then((response) => response.json())
      .then((post) => {
        this.bills = post
        console.log(this.bills)
      })
    },
  }
};
</script>
  
  <style>
.chat-header {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 5rem;
  background-color: #f2f2f2;
  border-bottom: 1px solid #e2e2e2;
}

.chat-messages {
  height: calc(100vh - 10rem);
  overflow-y: scroll;
  padding: 4px;
  margin-bottom: 1rem;
}

.message {
  margin-bottom: 1rem;
}

.message-info {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
}

.message-author {
  font-weight: bold;
}

.message-timestamp {
  color: #666;
}

.message-text {
  white-space: pre-wrap;
}

.chat-input {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 20px;
  /* background-color: #f2f2f2;
  border-top: 1px solid #e2e2e2; */
}

.chat-input input {
  flex-grow: 1;
  margin-right: 1rem;
  margin-left: 8px;
  margin-bottom: 2px;
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 0.25rem;
}

.chat-input button {
  padding: 20px;
  border: none;
  background-color: #333;
  color: white;
  border-radius: 0.25rem;
  cursor: pointer;
}
</style>
  
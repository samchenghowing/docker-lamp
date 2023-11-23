<template>
  <v-form>
    <v-container>
      <v-row>
        <v-col>
          <h1> Patients 
            <v-menu>
              <template v-slot:activator="{ props }">
                <v-btn v-bind="props" class="mt-n2" @click="getUpdate">
                  refresh
                </v-btn>
              </template>
            </v-menu>
          </h1>
          

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
                v-for="item in items"
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
        </v-col>
      </v-row>
    </v-container>
  </v-form>
</template>

<script>
export default {
  mounted() {
    this.getUpdate()
  },
  name: "ChatPage",
  data() {
    return {
      timer: null,
      user: "",
      messageText: "",
      dialog: false,
      items: null,
    };
  },
  methods: {
    getUpdate(){
      var updateAPI = process.env.VUE_APP_API_URL + "/chat/getupdate"
      var obj = JSON.parse(sessionStorage.user)
      var name = obj["User info"]["name"]
      var pwHash = obj["User info"]["pwHash"]
      
      fetch(updateAPI, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          name: name,
          pwHash: pwHash,
        })
      })
      .then((response) => response.json())
      .then((post) => {
        this.items = post
        console.log(this.items)
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
  
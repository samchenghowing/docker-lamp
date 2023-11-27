<template>
  <v-form>
    <v-container>
      <v-row>
        <v-col>
          <h1> admin </h1>

          <v-table>
            <thead>
              <tr>
                <th class="text-left"> log_id </th>
                <th class="text-left"> log_date </th>
                <th class="text-left"> log_info </th>
                <th class="text-left"> send_from </th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="item in logs"
                :key="item.name"
              >
                <td>{{ item.log_id }}</td>
                <td>{{ item.log_date }}</td>
                <td>{{ item.log_info }}</td>
                <td>{{ item.send_from }}</td>
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
    this.getLog()
  },
  data() {
    return {
      dialog: false,
      logs: null,
    };
  },
  methods: {
    getLog(){
      var updateAPI = process.env.VUE_APP_API_URL + "/getLog"
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
        this.logs = post
        console.log(this.logs)
        alert("Alert! There were new suspicious queries!")
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
  
<template>
  <v-form>
    <v-container>
      <v-row>
        <v-col>
          <h1> Secretaries  </h1>

          <v-card>
            <v-tabs
              v-model="tab"
              bg-color="primary"
            >
              <v-tab value="Appointments">Appointments</v-tab>
              <v-tab value="Results">Results</v-tab>
              <v-tab value="Billing">Billing</v-tab>
            </v-tabs>

            <v-card-text>
              <v-window v-model="tab">
                <v-window-item value="Appointments">

                  <v-btn
                    color="primary"
                    @click="appDialog = true"
                  >
                    New appointments
                  </v-btn>

                  <v-dialog
                    v-model="appDialog"
                    persistent
                    width="1024"
                  >
                    <v-card>
                      <v-card-title>
                        <span class="text-h5">New appointments</span>
                      </v-card-title>
                      <v-card-text>
                        <v-container>
                          <v-row>
                            <v-col
                              cols="12"
                              sm="6"
                              md="4"
                            >
                              <v-text-field
                                v-model="patient_id"
                                label="patient_id"
                                required
                                hint="only integer is accepted"
                              ></v-text-field>
                            </v-col>
                            <v-col
                              cols="12"
                              sm="6"
                              md="4"
                            >
                              <v-text-field
                                v-model="appointment_date"
                                label="appointment_date"
                                required
                                hint="YYYY-MM-DD"
                              ></v-text-field>
                            </v-col>
                          </v-row>
                        </v-container>
                      </v-card-text>
                      <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn
                          color="blue-darken-1"
                          variant="text"
                          @click="dialog = false"
                        >
                          cancel
                        </v-btn>
                        <v-btn
                          color="blue-darken-1"
                          variant="text"
                          @click="updateAppointments"
                        >
                          Save
                        </v-btn>
                      </v-card-actions>
                    </v-card>
                  </v-dialog>    
                  <v-table>
                    <thead>
                      <tr>
                        <th class="text-left"> appointment_id </th>
                        <th class="text-left"> patient_id </th>
                        <th class="text-left"> appointment_date </th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr
                        v-for="item in appointments"
                        :key="item.name"
                      >
                        <td>{{ item.appointment_id }}</td>
                        <td>{{ item.patient_id }}</td>
                        <td>{{ item.appointment_date }}</td>
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
                        <!-- <th class="text-left"> interpretation </th>
                        <th class="text-left"> reporting_pathologist </th> -->
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
                        <!-- <td>{{ item.interpretation }}</td>
                        <td>{{ item.reporting_pathologist }}</td> -->
                      </tr>
                    </tbody>
                  </v-table>
                </v-window-item>

                <v-window-item value="Billing">
                  
                  <v-dialog
                    v-model="dialog"
                    persistent
                    width="1024"
                  >
                    <v-card>
                      <v-card-title>
                        <span class="text-h5">update billing</span>
                      </v-card-title>
                      <v-card-text>
                        <v-container>
                          <v-row>
                            <v-col
                              cols="12"
                              sm="6"
                              md="4"
                            >
                              <v-text-field
                                v-model="bill_id"
                                label="bill_id"
                                required
                                hint="only integer is accepted"
                              ></v-text-field>
                            </v-col>
                            <v-col
                              cols="12"
                              sm="6"
                              md="4"
                            >
                              <v-text-field
                                v-model="billed_amount"
                                label="billed_amount"
                                required
                                hint="only numbers are accepted"
                              ></v-text-field>
                            </v-col>
                            <v-col cols="12">
                              <v-combobox
                                v-model="payment_status"
                                label="payment_status"
                                :items="['Paid', 'Pending']"
                                required
                              ></v-combobox>
                            </v-col>
                            <v-col cols="12">
                              <v-combobox
                                v-model="insurance_claim_status"
                                label="insurance_claim_status"
                                :items="['Claimed', 'Not Claimed']"
                                required
                              ></v-combobox>
                            </v-col>
                            <v-col cols="12">
                            </v-col>
                          </v-row>
                        </v-container>
                      </v-card-text>
                      <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn
                          color="blue-darken-1"
                          variant="text"
                          @click="dialog = false"
                        >
                          cancel
                        </v-btn>
                        <v-btn
                          color="blue-darken-1"
                          variant="text"
                          @click="updateBills"
                        >
                          Save
                        </v-btn>
                      </v-card-actions>
                    </v-card>
                  </v-dialog>         
                   
                  <v-table>
                    <thead>
                      <tr>
                        <th class="text-left"> bill_id </th>
                        <th class="text-left"> order_id </th>
                        <th class="text-left"> billed_amount </th>
                        <th class="text-left"> payment_status </th>
                        <th class="text-left"> insurance_claim_status </th>
                        <th class="text-left"> update bill </th>
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
                        <td>
                        <v-btn
                          color="primary"
                          @click="openDialog(item)"
                        >
                          update bill
                        </v-btn>
                      </td>
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
    this.getResults()
    this.getBills()
    this.getAppointments()
  },
  data() {
    return {
      tab: null,
      appointments: null,
      results: null,
      bills: null,
      dialog: false,
      appDialog: false,

      bill_id: "",
      billed_amount: "",
      payment_status: "",
      insurance_claim_status: "",

      patient_id: "",
      appointment_date: "",
    };
  },
  methods: {
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
    getAppointments(){
      var updateAPI = process.env.VUE_APP_API_URL + "/getAppointments"
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
        this.appointments = post
        console.log(post)
      })
    },
    updateBills(){
      var updateAPI = process.env.VUE_APP_API_URL + "/updateBills"
      var obj = JSON.parse(sessionStorage.user)
      var name = obj["User info"]["name"]
      var pwHash = obj["User info"]["pwHash"]
      
      fetch(updateAPI, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          name: name,
          pwHash: pwHash,
          bill_id: this.bill_id,
          billed_amount: this.billed_amount,
          payment_status: this.payment_status,
          insurance_claim_status: this.insurance_claim_status,
        })
      })
      .then((response) => response.json())
      .then((post) => {
        this.dialog = false
        this.getBills()
      })
    },
    updateAppointments(){
      var updateAPI = process.env.VUE_APP_API_URL + "/updateAppointments"
      var obj = JSON.parse(sessionStorage.user)
      var name = obj["User info"]["name"]
      var pwHash = obj["User info"]["pwHash"]
      
      fetch(updateAPI, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          name: name,
          pwHash: pwHash,
          patient_id: this.patient_id,
          appointment_date: this.appointment_date,
        })
      })
      .then((response) => response.json())
      .then((post) => {
        this.appDialog = false
        this.getAppointments()
      })
    },
    openDialog(item){
      this.bill_id = item.bill_id
      this.billed_amount = item.billed_amount
      this.payment_status = item.payment_status
      this.insurance_claim_status = item.insurance_claim_status
      this.dialog=true
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
  
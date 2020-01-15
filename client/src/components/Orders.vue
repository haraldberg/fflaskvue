<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Orders</h1>
        <hr><br><br>
        <alert :message=message v-if="showMessage"></alert>
        <template v-if="!isLoading">
          <button type="button" class="btn btn-primary btn-sm mr-2" @click="gotoUser">Back</button>
          <button type="button" class="btn btn-success btn-sm" v-b-modal.order-modal>Add Order</button>
          <br><br>
          <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">UserID</th>
              <th scope="col">Order Date</th>
              <th scope="col">Status</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(order, index) in orders" :key="index" style="cursor: pointer;">
              <td>{{ userId }}</td>
              <td>{{ order.order_date }}</td>
              <td>{{ order.status }}</td>
              <td>
                <div class="btn-group" role="group">
                  <button
                          type="button"
                          class="btn btn-warning btn-sm mr-2"
                          v-b-modal.order-update-modal
                          @click="editOrder(order)">
                      Update
                  </button>
                  <button
                          type="button"
                          class="btn btn-danger btn-sm mr-2"
                          @click="onDeleteOrder(order)">
                    Delete
                  </button>
                  <button
                          type="button"
                          class="btn btn-danger btn-sm mr-2"
                          @click="gotoScene(order.id)">
                    Scenes
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
        </template>
        <div v-else class="d-flex justify-content-center mb-3">
          <b-spinner large variant="primary"></b-spinner>
        </div>
      </div>
    </div>
    <b-modal ref="addOrderModal"
             no-close-on-backdrop
            id="order-modal"
            title="Add a new order"
            hide-footer>
      <b-form @submit="onSubmit" @reset="onReset" class="w-100">
      <b-form-group id="form-status-group"
                    label="status:"
                    label-for="form-status-input">
          <b-form-input id="form-status-input"
                        type="text"
                        v-model="addOrderForm.status"
                        required
                        placeholder="Enter Status">
          </b-form-input>
        </b-form-group>
        <b-button-group>
          <b-button type="submit" variant="primary">Submit</b-button>
          <b-button type="reset" variant="danger">Reset</b-button>
        </b-button-group>
      </b-form>
    </b-modal>
    <b-modal ref="editOrderModal"
             no-close-on-backdrop
            id="order-update-modal"
            title="Update"
            hide-footer>
      <b-form @submit="onSubmitUpdate" @reset="onResetUpdate" class="w-100">
      <b-form-group id="form-status-edit-group"
                  label="Status:"
                  label-for="form-status-edit-input">
        <b-form-input id="form-status-edit-input"
                      type="text"
                      v-model="editForm.status"
                      required
                      placeholder="Enter status">
        </b-form-input>
        </b-form-group>
        <b-button-group>
          <b-button type="submit" variant="primary">Update</b-button>
          <b-button type="reset" variant="danger">Cancel</b-button>
        </b-button-group>
      </b-form>
    </b-modal>
  </div>
</template>

<script>
import axios from 'axios';
import Alert from './Alert.vue';

export default {
  data() {
    return {
      orders: [],
      addOrderForm: {
        id: '',
        status: '',
      },
      message: '',
      showMessage: false,
      editForm: {
        id: '',
        status: '',
        date_created: '',
        user_id: '',
      },
      isLoading: false,
      userId: -1,
    };
  },
  components: {
    alert: Alert,
  },
  methods: {
    getOrders() {
      this.isLoading = true
      const path = `/orders/${this.userId}`;
      axios.get(path)
        .then((res) => {
          this.orders = res.data.orders;
          if (this.message !== '') this.showMessage = true;
          this.isLoading = false;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    addOrder(payload) {
      const path = `/orders/${this.userId}`;
      axios.post(path, payload)
        .then(() => {
          this.getOrders();
          this.message = 'Order added!';
          // this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
          this.getOrders();
        });
    },
    initForm() {
      this.addOrderForm.status = '';
      this.addOrderForm.id = '';
      this.editForm.id = '';
      this.editForm.status = '';
      this.editForm.user_id = '';
      this.editForm.date_created = '';
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.addOrderModal.hide();
      this.isLoading = true;
      const payload = {
        user_id: this.userId,
        status: this.addOrderForm.status,
      };
      this.addOrder(payload);
      this.initForm();
    },
    onReset(evt) {
      evt.preventDefault();
      this.$refs.addOrderModal.hide();
      this.initForm();
    },
    editOrder(order) {
      this.editForm = order;
    },
    onSubmitUpdate(evt) {
      evt.preventDefault();
      this.$refs.editOrderModal.hide();
      this.isLoading = true;
      const payload = {
        status: this.editForm.status,
      };
      this.updateOrder(payload, this.editForm.id);
    },
    updateOrder(payload, orderID) {
      const path = `/orders/${orderID}`;
      axios.put(path, payload)
        .then(() => {
          this.getOrders();
          this.message = 'Order updated!';
          // this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getOrders();
        });
    },
    onResetUpdate(evt) {
      evt.preventDefault();
      this.$refs.editOrderModal.hide();
      this.initForm();
      this.getOrders();
    },
    removeOrder(orderID) {
      const path = `/orders/${orderID}`;
      axios.delete(path)
        .then(() => {
          this.getOrders();
          this.message = 'Order removed!';
          // this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getOrders();
        });
    },
    onDeleteOrder(order) {
      this.isLoading = true;
      this.removeOrder(order.id);
    },
    gotoUser(){
      this.$router.push({
        name: 'Users'
      });
    },
    gotoScene(orderId){
      this.$router.push({
        name: 'Scenes',
        params: { userid: this.userId, orderid: orderId },
      });
    }
  },
  mounted() {
    this.userId = this.$route.params.id;
    this.getOrders();
  },
};
</script>

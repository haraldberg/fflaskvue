<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Users</h1>
        <hr><br><br>
        <alert :message=message v-if="showMessage"></alert>
        <template v-if="!isLoading">
          <button type="button" class="btn btn-success btn-sm" v-b-modal.user-modal>Add User</button>
          <br><br>
          <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">First Name</th>
              <th scope="col">Last Name</th>
              <th scope="col">Email</th>
              <th scope="col">created</th>
              <th scope="col">active</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(user, index) in users" :key="index" style="cursor: pointer;">
              <td>{{ user.first_name }}</td>
              <td>{{ user.last_name }}</td>
              <td>{{ user.email }}</td>
              <td>{{ user.date_created }}</td>
              <td>
                <span v-if="user.active">Yes</span>
                <span v-else>No</span>
              </td>
              <td>
                <div class="btn-group" role="group">
                  <button
                          type="button"
                          class="btn btn-warning btn-sm mr-2"
                          v-b-modal.user-update-modal
                          @click="editUser(user)">
                      Update
                  </button>
                  <button
                          type="button"
                          class="btn btn-danger btn-sm mr-2"
                          @click="onDeleteUser(user)">
                    Delete
                  </button>
                  <button
                          type="button"
                          class="btn btn-primary btn-sm mr-2"
                          @click="gotoOrder(user.id)">
                    Orders
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
    <b-modal ref="addUserModal"
             no-close-on-backdrop
            id="user-modal"
            title="Add a new user"
            hide-footer>
      <b-form @submit="onSubmit" @reset="onReset" class="w-100">
      <b-form-group id="form-firstname-group"
                    label="First Name:"
                    label-for="form-firstname-input">
          <b-form-input id="form-firstname-input"
                        type="text"
                        v-model="addUserForm.first_name"
                        required
                        placeholder="Enter first name">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-lastname-group"
                      label="Last Name:"
                      label-for="form-lastname-input">
            <b-form-input id="form-lastname-input"
                          type="text"
                          v-model="addUserForm.last_name"
                          required
                          placeholder="Enter last name">
            </b-form-input>
          </b-form-group>
        <b-form-group id="form-email-group"
                      label="Email:"
                      label-for="form-email-input">
            <b-form-input id="form-email-input"
                          type="text"
                          v-model="addUserForm.email"
                          required
                          placeholder="Enter email">
            </b-form-input>
          </b-form-group>
        <b-form-group id="form-active-group">
          <b-form-checkbox-group id="form-checks">
            <b-form-checkbox v-model="addUserForm.active" button>
              Active
            </b-form-checkbox>
          </b-form-checkbox-group>
        </b-form-group>
        <b-button-group>
          <b-button type="submit" variant="primary">Submit</b-button>
          <b-button type="reset" variant="danger">Reset</b-button>
        </b-button-group>
      </b-form>
    </b-modal>
    <b-modal ref="editUserModal"
             no-close-on-backdrop
            id="user-update-modal"
            title="Update"
            hide-footer>
      <b-form @submit="onSubmitUpdate" @reset="onResetUpdate" class="w-100">
      <b-form-group id="form-firstname-edit-group"
                  label="First Name:"
                  label-for="form-firstname-edit-input">
        <b-form-input id="form-firstname-edit-input"
                      type="text"
                      v-model="editForm.first_name"
                      required
                      placeholder="Enter first_name">
        </b-form-input>
        </b-form-group>
        <b-form-group id="form-lastname-edit-group"
                    label="Last Name:"
                    label-for="form-lastname-edit-input">
          <b-form-input id="form-lastname-edit-input"
                        type="text"
                        v-model="editForm.last_name"
                        required
                        placeholder="Enter last_name">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-email-edit-group"
                      label="Email:"
                    label-for="form-email-edit-input">
          <b-form-input id="form-email-edit-input"
                        type="text"
                        v-model="editForm.email"
                        required
                        placeholder="Enter last_name">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-active-edit-group">
          <b-form-checkbox-group id="form-checks">
            <b-form-checkbox v-model="editForm.active" button>
              Active
            </b-form-checkbox>
          </b-form-checkbox-group>
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

import Alert from './Alert.vue';

export default {
  data() {
    return {
      users: [],
      addUserForm: {
        first_name: '',
        last_name: '',
        email: '',
        active: '',
      },
      message: '',
      showMessage: false,
      editForm: {
        id: '',
        first_name: '',
        last_name: '',
        email: '',
        active: '',
      },
      isLoading: false,
    };
  },
  components: {
    alert: Alert,
  },
  methods: {
    getUsers() {
      this.isLoading = true
      this.axios.get('/users')
        .then((res) => {
          this.users = res.data.users;
          if (this.message !== '') this.showMessage = true;
          this.isLoading = false;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    addUser(payload) {
      this.axios.post('/users', payload)
        .then(() => {
          this.getUsers();
          this.message = 'User added!';
          // this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
          this.getUsers();
        });
    },
    initForm() {
      this.addUserForm.first_name = '';
      this.addUserForm.last_name = '';
      this.addUserForm.email = '';
      this.addUserForm.active = 1;
      this.editForm.id = '';
      this.editForm.first_name = '';
      this.editForm.last_name = '';
      this.editForm.email = '';
      this.editForm.active = 1;
      this.editForm.date_created = '';
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.addUserModal.hide();
      this.isLoading = true;
      if (this.addUserForm.active === true) this.addUserForm.active = 1;
      else this.addUserForm.active = 0;
      const payload = {
        first_name: this.addUserForm.first_name,
        last_name: this.addUserForm.last_name,
        email: this.addUserForm.email,
        active: this.addUserForm.active,
      };
      this.addUser(payload);
      this.initForm();
    },
    onReset(evt) {
      evt.preventDefault();
      this.$refs.addUserModal.hide();
      this.initForm();
    },
    editUser(user) {
      this.editForm = user;
      if (this.editForm.active === 1) this.editForm.active = true;
      else this.editForm.active = false;
    },
    onSubmitUpdate(evt) {
      evt.preventDefault();
      this.$refs.editUserModal.hide();
      this.isLoading = true;
      if (this.editForm.active === true) this.editForm.active = 1;
      else this.editForm.active = 0;
      const payload = {
        first_name: this.editForm.first_name,
        last_name: this.editForm.last_name,
        email: this.editForm.email,
        active: this.editForm.active,
      };
      this.updateUser(payload, this.editForm.id);
    },
    updateUser(payload, userID) {
      this.axios.put(`/users/${userID}`, payload)
        .then(() => {
          this.getUsers();
          this.message = 'User updated!';
          // this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getUsers();
        });
    },
    onResetUpdate(evt) {
      evt.preventDefault();
      this.$refs.editUserModal.hide();
      this.initForm();
      this.getUsers();
    },
    removeUser(userID) {
      this.axios.delete(`/users/${userID}`)
        .then(() => {
          this.getUsers();
          this.message = 'User removed!';
          // this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getUsers();
        });
    },
    onDeleteUser(user) {
      this.isLoading = true;
      this.removeUser(user.id);
    },
    gotoOrder(userId) {
      this.$router.push({
        name: 'Orders',
        params: { id: userId },
      });
    },
  },
  mounted() {
    this.getUsers();
  },
};
</script>

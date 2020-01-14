<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Scenes</h1>
        <hr><br><br>
        <alert :message=message v-if="showMessage"></alert>
        <template v-if="!isLoading">
          <button type="button" class="btn btn-primary btn-sm mr-2" @click="gotoOrder">Back</button>
          <button type="button" class="btn btn-success btn-sm" v-b-modal.scene-modal>Add Scene</button>
          <br><br>
          <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">UserID</th>
              <th scope="col">OrderID</th>
              <th scope="col">Name</th>
              <th scope="col">Status</th>
              <th scope="col">Sensor</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(scene, index) in scenes" :key="index" style="cursor: pointer;">
              <td>{{ userId }}</td>
              <td>{{ orderId }}</td>
              <td>{{ scene.name }}</td>
              <td>{{ scene.status }}</td>
              <td>{{ scene.sensor }}</td>
              <td>
                <div class="btn-group" role="group">
                  <button
                          type="button"
                          class="btn btn-warning btn-sm"
                          v-b-modal.scene-update-modal
                          @click="editScene(scene)">
                      Update
                  </button>
                  <button
                          type="button"
                          class="btn btn-danger btn-sm"
                          @click="onDeleteScene(scene)">
                    Delete
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
    <b-modal ref="addSceneModal"
             no-close-on-backdrop
            id="scene-modal"
            title="Add a new scene"
            hide-footer>
      <b-form @submit="onSubmit" @reset="onReset" class="w-100">
        <b-form-group id="form-name-group"
                    label="Name:"
                    label-for="form-name-input">
          <b-form-input id="form-name-input"
                        type="text"
                        v-model="addSceneForm.name"
                        required
                        placeholder="Enter Name">
          </b-form-input>
        </b-form-group>
      <b-form-group id="form-status-group"
                    label="status:"
                    label-for="form-status-input">
          <b-form-input id="form-status-input"
                        type="text"
                        v-model="addSceneForm.status"
                        required
                        placeholder="Enter Status">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-sensor-group"
                    label="Sensor:"
                    label-for="form-sensor-input">
          <b-form-input id="form-sensor-input"
                        type="text"
                        v-model="addSceneForm.sensor"
                        required
                        placeholder="Enter Sensor">
          </b-form-input>
        </b-form-group>
        <b-button-group>
          <b-button type="submit" variant="primary">Submit</b-button>
          <b-button type="reset" variant="danger">Reset</b-button>
        </b-button-group>
      </b-form>
    </b-modal>
    <b-modal ref="editSceneModal"
             no-close-on-backdrop
            id="scene-update-modal"
            title="Update"
            hide-footer>
      <b-form @submit="onSubmitUpdate" @reset="onResetUpdate" class="w-100">
        <b-form-group id="form-name-edit-group"
                    label="Name:"
                    label-for="form-name-edit-input">
          <b-form-input id="form-name-edit-input"
                        type="text"
                        v-model="editForm.name"
                        required
                        placeholder="Enter Name">
          </b-form-input>
        </b-form-group>

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

        <b-form-group id="form-sensor-edit-group"
                    label="Sensor:"
                    label-for="form-sensor-edit-input">
          <b-form-input id="form-sensor-edit-input"
                        type="text"
                        v-model="editForm.sensor"
                        required
                        placeholder="Enter Sensor">
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
      scenes: [],
      addSceneForm: {
        id: '',
        order_id: '',
        name: '',
        status: '',
        sensor: '',
      },
      message: '',
      showMessage: false,
      editForm: {
        id: '',
        order_id: '',
        name: '',
        status: '',
        sensor: '',
      },
      isLoading: false,
      userId: -1,
      orderId: -1,
    };
  },
  components: {
    alert: Alert,
  },
  methods: {
    getScenes() {
      this.isLoading = true
      const path = `/scenes/${this.orderId}`;
      axios.get(path)
        .then((res) => {
          this.scenes = res.data.scenes;
          if (this.message !== '') this.showMessage = true;
          this.isLoading = false;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    addScene(payload) {
      const path = `/scenes/${this.orderId}`;
      axios.post(path, payload)
        .then(() => {
          this.getScenes();
          this.message = 'Scene added!';
          // this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
          this.getScenes();
        });
    },
    initForm() {
      this.addSceneForm.name = '';
      this.addSceneForm.status = '';
      this.addSceneForm.sensor = '';
      this.addSceneForm.id = '';
      this.addSceneForm.order_id = '';
      this.editForm.id = '';
      this.editForm.order_id = '';
      this.editForm.name = '';
      this.editForm.status = '';
      this.editForm.sensor = '';
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.addSceneModal.hide();
      this.isLoading = true;
      const payload = {
        order_id: this.orderId,
        name: this.addSceneForm.name,
        status: this.addSceneForm.status,
        sensor: this.addSceneForm.sensor,
      };
      this.addScene(payload);
      this.initForm();
    },
    onReset(evt) {
      evt.preventDefault();
      this.$refs.addSceneModal.hide();
      this.initForm();
    },
    editScene(scene) {
      this.editForm = scene;
    },
    onSubmitUpdate(evt) {
      evt.preventDefault();
      this.$refs.editSceneModal.hide();
      this.isLoading = true;
      const payload = {
        name: this.editForm.name,
        status: this.editForm.status,
        sensor: this.editForm.sensor,
      };
      this.updateScene(payload, this.editForm.id);
    },
    updateScene(payload, sceneID) {
      const path = `/scenes/${sceneID}`;
      axios.put(path, payload)
        .then(() => {
          this.getScenes();
          this.message = 'Scene updated!';
          // this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getScenes();
        });
    },
    onResetUpdate(evt) {
      evt.preventDefault();
      this.$refs.editSceneModal.hide();
      this.initForm();
      this.getScenes();
    },
    removeScene(sceneID) {
      const path = `/scenes/${sceneID}`;
      axios.delete(path)
        .then(() => {
          this.getScenes();
          this.message = 'Scene removed!';
          // this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getScenes();
        });
    },
    onDeleteScene(scene) {
      this.isLoading = true;
      this.removeScene(scene.id);
    },
    gotoOrder(){
      this.$router.push({
        name: 'Orders',
        params: { id: this.userId },
      });
    }
  },
  mounted() {
    this.userId = this.$route.params.userid;
    this.orderId = this.$route.params.orderid;
    this.getScenes();
  },
};
</script>

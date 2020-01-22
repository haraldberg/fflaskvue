import 'bootstrap/dist/css/bootstrap.css';
import BootstrapVue from 'bootstrap-vue';
import Vue from 'vue';
import VueRouter from 'vue-router';


import axios from 'axios';
import VueAxios from 'vue-axios';
import router from './router';
import App from './App.vue';
Vue.use(VueAxios, axios);
axios.defaults.baseURL = 'http://flask:5000/';
// axios.defaults.baseURL = 'http://127.0.0.1:5000/';

Vue.use(VueRouter);
Vue.use(BootstrapVue);
Vue.router = router;

Vue.config.productionTip = false;

new Vue({
  router,
  render: h => h(App),
}).$mount('#app');

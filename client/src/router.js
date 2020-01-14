import Vue from 'vue';
import Router from 'vue-router';
import Users from './components/Users.vue';
import Orders from './components/Orders.vue';
import Scenes from './components/Scenes.vue';
import Ping from './components/Ping.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'Users',
      component: Users,
    },
    {
      path: '/ping',
      name: 'Ping',
      component: Ping,
    },
    {
      path: '/order/:id',
      name: 'Orders',
      component: Orders,
    },
    {
      path: '/scene/:userid/:orderid',
      name: 'Scenes',
      component: Scenes,
    },
  ],
});

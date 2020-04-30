import Vue from 'vue'
import App from './App.vue'
import VueRouter from 'vue-router'
import router from './router'
import "chart.js";

Vue.use(VueRouter)
Vue.config.productionTip = false

const app = new Vue({
  el: '#app',
  router,
  render: h => h(App)
});
app.$mount('#app');

import Vue from 'vue';
import Router from 'vue-router';
import Starter from './pages/StarterPage.vue';
import StarterNavbar from './layout/StarterNavbar.vue';
import StarterFooter from './layout/StarterFooter.vue';

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/login',
      name: 'login-page',
      components: {
        default: Starter,
        header: StarterNavbar,
        footer: StarterFooter
      },
      props: {
        header: { colorOnScroll: 400 },
        footer: { backgroundColor: 'black' }
      }
    }
  ],
  scrollBehavior: to => {
    if (to.hash) {
      return { selector: to.hash };
    } else {
      return { x: 0, y: 0 };
    }
  }
});

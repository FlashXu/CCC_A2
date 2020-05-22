import Vue from 'vue';
import Router from 'vue-router';
import Index from './pages/Index.vue';
import Team from './pages/Team.vue';
import Maps from './pages/Maps.vue';
import Login from './pages/Login.vue';
import Profile from './pages/Profile.vue';
import MainNavbar from './layout/MainNavbar.vue';
import MainFooter from './layout/MainFooter.vue';
import Linechart from './charttype/Linechart.vue'
import Piechart from './charttype/Piechart.vue'
import Barchart from './charttype/Barchart.vue'
import Radarchart from './charttype/Radarchart.vue'
import Mixedchart from './charttype/Mixedchart.vue'


Vue.use(Router);

export default new Router({
  linkExactActiveClass: 'active',
  routes: [
    {
      path: '/',
      name: 'index',
      components: { default: Index, header: MainNavbar, footer: MainFooter },
      props: {
        header: { colorOnScroll: 400 },
        footer: { backgroundColor: 'black' }
      }
    },
    {
      path: '/team',
      name: 'team',
      components: { default: Team, header: MainNavbar, footer: MainFooter },
      props: {
        header: { colorOnScroll: 400 },
        footer: { backgroundColor: 'black' }
      }
    },
    {
      path: '/login',
      name: 'login',
      components: { default: Login, header: MainNavbar },
      props: {
        header: { colorOnScroll: 400 }
      }
    },
    {
      path: '/profile',
      name: 'profile',
      components: { default: Profile, header: MainNavbar, footer: MainFooter },
      props: {
        header: { colorOnScroll: 400 },
        footer: { backgroundColor: 'black' }
      }
    },
    {
      path: '/maps',
      name: 'maps',
      components: { default: Maps, header: MainNavbar, footer: MainFooter },
      props: {
        header: { colorOnScroll: 400 },
        footer: { backgroundColor: 'black' }
      }
    },
    {
      path: '/linechart',
      name:'line',
      component: Linechart,
    },
    {
      path: '/piechart',
      name:'pie',
      component: Piechart
    },
    {
      path: '/barchart',
      name:'bar',
      component: Barchart
    },
    {
      path: '/radarchart',
      name:'radar',
      component: Radarchart
    },
    {
      path: '/mixedchart',
      name:'mixed',
      component: Mixedchart
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

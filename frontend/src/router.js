import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

const Map = () => import('@/views/Map.vue')
const Landing = () => import('@/views/Landing.vue')
const MainNavbar = () => import ('@/layout/MainNavbar.vue')
const MainFooter = () => import ('@/layout/MainFooter.vue')

export default new Router({
  routes: [
    {
      path: '/map', 
      component: Map
    },
    {
      path: '/landing',
      name: 'landing',
      components: { default: Landing, header: MainNavbar, footer: MainFooter },
      props: {
        header: { colorOnScroll: 400 },
        footer: { backgroundColor: 'black' }
      }
    }
  ],
	mode: 'history'
})
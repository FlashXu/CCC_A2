import Vue from 'vue'
import Router from 'vue-router'
import Linechart from '@/charttype/Linechart.vue'
import Piechart from '@/charttype/Piechart.vue'
import Barchart from '@/charttype/Barchart.vue'

Vue.use(Router)


export default new Router({
  routes: [{
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
  }
  ],
	mode: 'history'
})
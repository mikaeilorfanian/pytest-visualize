import Vue from 'vue'
import Router from 'vue-router'
import Run from '@/components/Run'


Vue.use(Router)

export default new Router({
    routes: [
      {
        path: '/',
        name: 'root',
        component: Run
      },
    ]
})
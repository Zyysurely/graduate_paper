import Vue from 'vue'
import Router from 'vue-router'
import Dashboard from '@/components/Dashboard.vue'
import login from '@/components/login.vue'

Vue.use(Router)
const BannerList = r => require.ensure([], () => r(require('@/components/content/Algorithm.vue')), 'group-offer')
const data = r => require.ensure([], () => r(require('@/components/content/manage_data.vue')), 'group-offer')
const demo = r => require.ensure([], () => r(require('@/components/content/demo.vue')), 'group-offer')
const result = r => require.ensure([], () => r(require('@/components/content/result.vue')), 'group-offer')


const router = new Router({
  routes: [
    {
      path: '/login',
      name: 'login',
      component: login
    },
    {
      path: '/',
      name: 'Dashboard',
      component: Dashboard,
      children: [
        {
          name: 'algorithm',
          path: '/algorithm',
          component: BannerList
        },
        {
          name: 'dataManagement',
          path: '/datamanagement',
          component: data
        },
        {
          name: 'demo',
          path: '/demo',
          component: demo
        },
        {
          name: 'result',
          path: '/result',
          component: result
        }
      ]
    }
  ]
})

// router.beforeEach((to, from, next) => {
//   if (sessionStorage.getItem('user_name') == null && !to.fullPath.startsWith('/login')) {
//     next({
//       path: '/login',
//       query: {redirect: to.fullPath}
//     })
//   } else {
//     next()
//   }
// })
export default router



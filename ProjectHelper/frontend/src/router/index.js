import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '../components/HelloWorld'
import login from '../components/login'
import homepage from '../components/homepage'
import profile from '../components/profile'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'HelloWorld',
      component: HelloWorld,
    },
    {
      path: '/login',
      name: 'login',
      component: login,
    },
    {
      path: '/homepage',
      name: 'homepage',
      component: homepage,
    },
    {
      path: '/homepage/profile',
      name: 'homepage_profile',
      component: profile,
    },
  ],
})

import Vue from 'vue'
import Router from 'vue-router'
// import HelloWorld from '../components/HelloWorld'
import login from '../components/login'
import homepage from '../components/homepage'
import profile from '../components/profile'
import new_password from '../components/new_password'

Vue.use(Router)

export default new Router({
  routes: [
    // {
    //   path: '/',
    //   name: 'HelloWorld',
    //   component: HelloWorld,
    // },
    {
      path: '/login',
      name: 'login',
      component: login,
    },
    {
      path: '/homepage',
      name: 'homepage',
      component: homepage,
      meta: {
        requireAuth: true,
      },
    },
    {
      path: '/homepage/profile',
      name: 'homepage_profile',
      component: profile,
      meta: {
        requireAuth: true,
      },
    },
    {
      path: '/homepage/profile/newpassword',
      name: 'homepage_profile_newpassword',
      component: new_password,
    },
  ],
})

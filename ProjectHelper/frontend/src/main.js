// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import Axios from 'axios'
import Vuex from 'vuex'
import store from './store/index.js'
import VueResource from 'vue-resource'

Vue.prototype.$axios = Axios
Axios.defaults.baseURL = '/api'
Axios.defaults.headers.post['Content-Type'] = 'application/json'
Vue.config.productionTip = false
Vue.use(ElementUI)
Vue.use(Vuex)
Vue.use(VueResource)

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  components: { App },
  template: '<App/>',
})

Axios.interceptors.request.use(
  config => {
    if (localStorage.getItem('Authorization')) {
      config.data.token = localStorage.getItem('Authorization')
    }
    return config
  },
  error => {
    return Promise.reject(error)
  })

// this.Axios.interceptors.response.use(
//   response => {
//     console.log('response token有效')
//     return response
//   },
//   error => {
//     var self = this
//     if (error.response) {
//       switch (error.response.status) {
//         case 401:
//           localStorage.removeItem('Authorization')
//           // console.log('token删除了')
//           this.$router.push({
//             name: 'Login',
//           })
//       }
//     }
//   },
// )
//
// router.beforeEach((to, from, next) => {
//   let token = localStorage.getItem('Authorization')
//   console.log('p',to.path)
//   if (to.path !== '/login' && to.path !== '/' && (token === 'null' || token === '')) {
//     console.log('无token || token失效')
//     next({ path: '/login', query: { Rurl: to.fullPath } })
//   } else {
//     console.log('token验证成功')
//     next()
//   }
// })

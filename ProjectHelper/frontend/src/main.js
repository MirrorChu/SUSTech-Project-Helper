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

Vue.prototype.$axios = Axios
Axios.defaults.baseURL = '/api'
Axios.defaults.headers.post['Content-Type'] = 'application/json'
Vue.config.productionTip = false
Vue.use(ElementUI)
Vue.use(Vuex)

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  components: { App },
  template: '<App/>',
})

//异步请求前在header里加入token
Axios.interceptors.request.use(
  config => {
    if (config.url === '/login' || config.url === '/') {  //如果是登录操作，则不需要携带header里面的token
    } else {
      if (localStorage.getItem('Authorization')) {
        config.headers.Authorizatior = localStorage.getItem('Authorization')
      }
    }
    return config
  },
  error => {
    return Promise.reject(error)
  })

//异步请求后，判断token是否过期
Axios.interceptors.response.use(
  response => {
    console.log('token有效')
    return response
  },
  error => {
    if (error.response) {
      switch (error.response.status) {
        case 401:
          localStorage.removeItem('Authorization')
          console.log('token删除了')
          this.$router.push('/')
      }
    }
  },
)

//异步请求前判断请求的连接是否需要token
router.beforeEach((to, from, next) => {
  if (to.path === '/' || to.path === '/login') {
    next()
  } else {
    let token = localStorage.getItem('Authorization')
    console.log('beforeEach')
    console.log('我是浏览器本地缓存的token: ' + token)
    if (token === 'null' || token === '') {
      console.log('无token || token失效')
      next({ path: '/login', query: { Rurl: to.fullPath } })
    } else {
      console.log('token验证成功')
      next()
    }
  }
})

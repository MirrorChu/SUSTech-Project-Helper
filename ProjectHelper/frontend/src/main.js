// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue';
import App from './App';
import router from './router';
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import Axios from 'axios';
import Vuex from 'vuex';
import store from './store/index.js';
import VueResource from 'vue-resource';
import da from 'element-ui/src/locale/lang/da';

Vue.prototype.$axios = Axios;
Axios.defaults.baseURL = '/api';
Axios.defaults.headers.post['Content-Type'] = 'application/json';
Vue.config.productionTip = false;
Vue.use(ElementUI);
Vue.use(Vuex);
Vue.use(VueResource);

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  components: {App},
  template: '<App/>',
});

Axios.interceptors.request.use(config => {
  if (localStorage.getItem('Authorization')) {
    config.data.token = localStorage.getItem('Authorization');
  }
  return config;
}, error => {
  return Promise.reject(error);
});

Axios.interceptors.response.use(res => {
      console.log('from main.js', res);
      return res;
    }, err => {
      console.log('from main.js', err);
      if (err.response) {
        console.log('from main.js', err.response.status);
        if (err.response.status === 401) {
          console.log('from main.js status 401', 401);
          localStorage.removeItem('Authorization');
          router.push({
            name: 'Login',
          }).then(res => {
            console.log(res);
          });
        }
      }
    },
);

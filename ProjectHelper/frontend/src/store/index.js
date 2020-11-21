import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({

  state:{
    //存储数据
    sid:'',
    Login_status:0,  //0: not Login 1: general user
    token:'',
    Authorization: localStorage.getItem('Authorization') ? localStorage.getItem('Authorization') : '',
  },
  mutations:{
    //数据处理方法
    Login(state, user)
    {
      state.Authorization = user.Authorization;
      state.sid = user.sid;
      console.log('token加载好了')
      localStorage.setItem('Authorization', user.Authorization)
    },
    Logout(state)
    {
      state.Authorization = ''
      state.sid = ''
      console.log('token删了')
      localStorage.removeItem('Authorization')
    }
  },
  getters:{
    //数据包装
  }

})

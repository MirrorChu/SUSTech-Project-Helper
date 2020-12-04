<template>
  <div class="login">
    <el-form :label-position="labelPosition" :label-width="labelWidth">
      <el-form-item label="Student ID">
        <el-input v-model="sid" placeholder="SID" clearable></el-input>
      </el-form-item>
      <el-form-item label="PASSWORD">
        <el-input v-model="pswd" show-password placeholder="PASSWORD" clearable></el-input>
      </el-form-item>
      <el-form-item>
        <el-button @click="onLoginClick()">LOGIN</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>
<script>
import { setCookie, getCookie } from '../assets/js/cookie.js'
import axios from 'axios'

export default {
  name: 'login',
  data () {
    return {
      sid: '',
      pswd: '',
      labelPosition: 'left',
      labelWidth: '100px',
    }
  },
  mounted () {
    /*页面挂载获取cookie，如果存在username的cookie，则跳转到主页，不需登录*/
    // if (getCookie('sid'))
    // {
    //   this.$router.push('/homepage')
    // }
  },
  methods: {
    onLoginClick () {
      //TODO Login request.
      axios.defaults.xsrfCookieName = 'csrftoken'
      axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN'
      var status = ''
      this.$axios.post('/login/', { sid: this.sid, pswd: this.pswd }).then(res => {
        console.log(res)
        status = res.data['LoginCheck']
        if (status === 'student' || status === 'teacher') {
          let token = 'Bearer ' + res.data.token
          // setCookie('sid', this.sid, 1000 * 60)
          console.log('token: ', token)
          this.$store.commit('Login', { Authorization: token, sid: this.sid })
          this.$router.push({
            name: 'homepage',
            params: {
              sid: this.sid,
              pswd: this.pswd,
            },
          })
        } else {
          this.sid = ''
          this.pswd = ''
          alert('WRONG SID OR PASSWORD')
        }

      }).catch(err => {
        console.log('err', err)
        alert(err)
      })
    },
  },
}
</script>

<!--<style scoped>-->

<!--</style>-->

<template>
  <div class="login">
    <h1>LOGIN</h1>
    <el-input v-model="sid" placeholder="SID" clearable></el-input>
    <el-input v-model="pswd" show-password placeholder="PASSWORD" clearable></el-input>
    <el-button @click="onLoginClick()">LOGIN</el-button>
  </div>
</template>
<script>
import { setCookie, getCookie } from '../assets/js/cookie.js'

export default {
  name: 'login',
  data ()
  {
    return {
      sid: '',
      pswd: '',
    }
  },
  mounted ()
  {
    /*页面挂载获取cookie，如果存在username的cookie，则跳转到主页，不需登录*/
    if (getCookie('sid'))
    {
      this.$router.push('/homepage')
    }
  },
  methods: {
    onLoginClick ()
    {
      this.$axios.get('').then(res =>
      {
        console.log('res', res)
      }).catch(err =>
      {
        console.log('err', err)
      })
      if (this.sid === '11813121' && this.pswd === '11813121')
      {
        setCookie('sid', this.sid, 1000 * 10)
        this.$router.push(
          {
            name: 'homepage',
            params: {
              sid: this.sid,
              pswd: this.pswd,
            },
          })
      }
      else
      {
        this.sid = ''
        this.pswd = ''
        alert('WRONG SID OR PASSWORD')
      }
    },
  },
}
</script>

<!--<style scoped>-->

<!--</style>-->

<template>
  <div class="homepage">
    <el-header>HOMEPAGE</el-header>
    <el-row>
      Hello, {{ name }}
    </el-row>
    <el-row>
      <el-button @click="onClickProfile">My Profile</el-button>
      <el-button @click="onClickLogout">Logout</el-button>
    </el-row>
  </div>
</template>

<script>
import profile from './profile'
import { updateCookie, getCookie, delCookie } from '../assets/js/cookie.js'

export default {
  name: 'homepage',
  components: { profile },
  data ()
  {
    return {
      sid: 3463462,
      pswd: this.$route.params.pswd,
      name: '',
    }
  },
  created ()
  {
    /*页面挂载获取保存的cookie值，渲染到页面上*/
    let cookie = getCookie('sid')
    console.log(cookie)
    this.sid = cookie
    console.log('sid', this.sid)
    /*如果cookie不存在，则跳转到登录页*/
    if (cookie === '')
    {
      this.$router.push('/login')
    }
    //TODO: Do we use a request to get name?
    else
    {
      this.name = 'JIASHU'
    }
  },
  methods: {
    //TODO: Personal profile request.
    onClickProfile ()
    {
      let cookie = getCookie('sid')
      if (cookie === '')
      {
        this.$router.push('/login')
      }
      else
      {
        updateCookie('sid', this.sid, 1000 * 60)
        //Why is this a warning here?
        this.$router.push({ name: 'homepage_profile', params: { name: this.name, sid: this.sid } })
      }
    },

    //TODO: Logout request.
    onClickLogout ()
    {
      delCookie('sid')
      this.$router.push('/')
    },
  },
}
</script>

<style scoped>

</style>

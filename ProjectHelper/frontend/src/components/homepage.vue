<template>
  <div class="homepage">
    <el-header>HOMEPAGE</el-header>
    <el-row>
      Hello, {{ name }}
    </el-row>
    <el-row>
      <el-button @click="onClickProfile">My Profile</el-button>
      <el-button @click="onClickNewPassword">New Password</el-button>
      <el-button @click="onClickLogout">Logout</el-button>
    </el-row>
    <profile id="my_profile" v-if="show_profile" v-bind:sid="this.sid" v-bind:name="this.name"></profile>
  </div>
</template>

<script>
import profile from './profile'
import { getCookie,delCookie } from '../assets/js/cookie.js'

export default {
  name: 'homepage',
  components: { profile },
  data ()
  {
    return {
      sid: 3463462,
      pswd: this.$route.params.pswd,
      name: '',
      show_profile: false,
    }
  },
  created ()
  {
    // console.log('sid', this.sid)
    // if (this.sid !== '11813121' || this.pswd !== '11813121')
    // {
    //   this.$router.push('/login')
    // }
    // else
    // {
    //   this.name = 'Jiashu'
    // }
    /*页面挂载获取保存的cookie值，渲染到页面上*/
    let cookie = getCookie('sid')
    this.sid = cookie;
    console.log('sid', this.sid)
    /*如果cookie不存在，则跳转到登录页*/
    if(cookie === ""){
      this.$router.push('/login')
    }
    else
    {
      this.name = 'JIASHU';
    }
  },
  methods: {
    onClickProfile ()
    {
      this.show_profile = !this.show_profile
    },
    onClickNewPassword ()
    {

    },
    onClickLogout ()
    {
      delCookie('sid');
      this.$router.push('/')
    },
  },
}
</script>

<style scoped>

</style>

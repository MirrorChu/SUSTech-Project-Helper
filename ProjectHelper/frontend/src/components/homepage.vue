<template>
  <div class="homepage">
    <el-container direction="horizontal">

      <el-aside>
        <el-menu default-active="1-4-1" class="nav" :collapse="!showNav">
          <el-header v-if="showNav">
            Project Helper
          </el-header>
          <el-header v-if="!showNav">
            PH
          </el-header>
          <el-menu-item @click="onClickProfile">
            <i class="el-icon-user"></i>
            <span slot="title">My Profile</span>
          </el-menu-item>
          <el-menu-item>
            <i class="el-icon-folder"></i>
            <span slot="title">My Projects</span>
          </el-menu-item>
          <el-menu-item>
            <i class="el-icon-message"></i>
            <span slot="title">Messages</span>
          </el-menu-item>
          <el-menu-item>
            <i class="el-icon-setting"></i>
            <span slot="title">Settings</span>
          </el-menu-item>
          <el-menu-item @click="onClickLogout">
            <i class="el-icon-circle-close" @click="onClickLogout"></i>
            <span slot="title" @click="onClickLogout">Logout</span>
          </el-menu-item>
          <el-menu-item v-if="this.showNav" @click="openCloseNav">
            <i class="el-icon-arrow-left"></i>
          </el-menu-item>
          <el-menu-item v-if="!this.showNav" @click="openCloseNav">
            <i class="el-icon-arrow-right"></i>
          </el-menu-item>
        </el-menu>
      </el-aside>

      <el-main>

      </el-main>
    </el-container>
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
      showNav: false,
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
    // if (cookie === '')
    // {
    //   this.$router.push('/login')
    // }
    //TODO: Do we use a request to get name?
    // else
    // {
      this.name = 'JIASHU'
    // }
  },
  methods: {
    openCloseNav ()
    {
      this.showNav = !this.showNav
    },

    //TODO: Personal profile request.
    onClickProfile ()
    {
      // let cookie = getCookie('sid')
      // if (cookie === '')
      // {
      //   this.$router.push('/login')
      // }
      // else
      // {
        updateCookie('sid', this.sid, 1000 * 60)
        //Why is this a warning here?
        console.log(this.sid, this.name)
        this.$router.push({ name: 'homepage_profile', params: { sid: this.sid, name: this.name } })
      // }
    },

    //TODO: New password request.
    onClickNewPassword ()
    {
      updateCookie('sid', this.sid, 1000 * 60)
    },

    //TODO: Logout request.
    onClickLogout ()
    {
      console.log('logout')
      delCookie('sid')
      this.$router.push('/')
    },
  },
}
</script>

<style scoped>
.nav:not(.el-menu--collapse) {
  width: 200px;
  min-height: 400px;
}
</style>

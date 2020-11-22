<template>
  <div class="homepage">
    <el-container direction="horizontal">

      <el-aside :width="asideWidth">
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
            <i class="el-icon-setting" @click="onClickSettings"></i>
            <span slot="title">Settings</span>
          </el-menu-item>
          <el-menu-item @click="onClickLogout">
            <i class="el-icon-circle-close" @click="onClickLogout"></i>
            <span slot="title" @click="onClickLogout">Logout</span>
          </el-menu-item>
          <el-menu-item v-if="this.showNav" @click="openCloseNav">
            <i class="el-icon-arrow-left"></i>
          </el-menu-item>
          <!--          <el-menu-item v-if="!this.showNav" @click="openCloseNav">-->
          <!--            <i class="el-icon-arrow-right"></i>-->
          <!--          </el-menu-item>-->
        </el-menu>
      </el-aside>

      <el-main>

        <profile v-show="mainContent.profile" v-bind:sid="this.sid" v-bind:pswd="this.pswd"></profile>

        <new_password v-if="mainContent.settings" v-bind:sid="this.sid"></new_password>

      </el-main>

    </el-container>
  </div>
</template>

<script>
import profile from './profile'
import { updateCookie, getCookie, delCookie } from '../assets/js/cookie.js'
import New_password from './new_password'

export default {
  name: 'homepage',
  components: { New_password, profile },
  props: {},
  data ()
  {
    return {
      sid: '11813121',
      pswd: '456',
      name: '',
      asideWidth: '160px',
      showNav: false,
      mainContent: {
        profile: false,
        projects: false,
        messages: false,
        settings: false,
      },
    }
  },
  created ()
  {
    /*页面挂载获取保存的cookie值，渲染到页面上*/
    // let cookie = getCookie('sid')
    // console.log(cookie)
    // this.sid = cookie
    // console.log('sid', this.sid)
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
    changeMainContent (item)
    {
      for (const iter in this.mainContent)
      {
        if (iter === item)
        {
          this.mainContent[iter] = !this.mainContent[iter]
        } else
        {
          this.mainContent[iter] = false
        }
      }
    },
    openCloseNav ()
    {
      this.showNav = !this.showNav
      // if (this.showNav)
      // {
      //   this.asideWidth = '160px';
      // }
      // else
      // {
      //   this.asideWidth = '160px';
      // }
    },

    onClickSettings ()
    {
      this.changeMainContent('settings')
    },

    //TODO: Personal profile request.
    onClickProfile ()
    {
      this.changeMainContent('profile')
      console.log(this.sid, this.name)
    },

    //TODO: New password request.
    onClickNewPassword ()
    {
      // updateCookie('sid', this.sid, 1000 * 60)
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
  min-height: 400px;
}
</style>

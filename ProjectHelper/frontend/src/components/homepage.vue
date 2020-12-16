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
          <el-menu-item @click="onClickProjects">
            <i class="el-icon-folder"></i>
            <span slot="title" @click="onClickProjects">My Projects</span>
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
        </el-menu>
      </el-aside>

      <el-main>

        <profile v-show="mainContent.profile" v-bind:sid="this.sid"></profile>

        <NewPassword v-if="mainContent.settings" v-bind:sid="this.sid"></NewPassword>

        <ProjectList v-show="mainContent.projects"></ProjectList>

      </el-main>

    </el-container>
  </div>
</template>

<script>
import profile from './profile'
import NewPassword from './NewPassword'
import ProjectDetail from './ProjectDetail'
import ProjectList from './ProjectList'

export default {
  name: 'Homepage',
  components: { ProjectList, ProjectDetail, NewPassword, profile },
  props: {},
  data () {
    return {
      searchKey: '',
      sid: this.$route.params.sid,
      identity: this.$route.params.identity,
      name: '',
      asideWidth: '160px',
      showNav: false,
      mainContent: {
        profile: false,
        projects: false,
        messages: false,
        settings: false,
        showProjectDetail: false,
      },
      projectDetail: null,
      groupInfo: null,
      courses: null,
    }
  },
  created () {
    console.log('/student_gets_all_projects/')
    this.$axios.post('/student_gets_all_projects/').then(res => {
      console.log('all projects', res.data['Data'])
      this.courses = res.data['Data']
    }).catch(err => {
      console.log(err)
    })
  },
  methods: {
    changeMainContent (item) {
      for (const iter in this.mainContent) {
        if (iter === item) {
          console.log(item, iter)
          this.mainContent[iter] = !this.mainContent[iter]
        } else {
          this.mainContent[iter] = false
        }
      }
    },
    openCloseNav () {
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

    onClickSettings () {
      this.changeMainContent('settings')
    },

    //TODO: Personal profile request.
    onClickProfile () {
      this.changeMainContent('profile')
      console.log(this.sid, this.name)
    },

    onClickProjects () {
      this.changeMainContent('projects')
    },

    //TODO: New password request.
    onClickNewPassword () {
      // updateCookie('sid', this.sid, 1000 * 60)
    },

    //TODO: Logout request.
    onClickLogout () {
      this.$axios.post('/logout/', {}).then(res => {
        console.log('logout', res.data)
        localStorage.removeItem('Authorization')
        this.$router.push('/login')
      }).catch(err => {
        console.log('logout err', err)
      })
    },
  },
}
</script>

<style scoped>
.nav:not(.el-menu--collapse) {
  min-height: 400px;
}
.el-aside{
  position: fixed;
  width: 100%;
  top: 150px;
}
.el-main{
  margin-left: 160px;
}

</style>

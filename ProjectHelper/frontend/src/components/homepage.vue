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
          <!--          <el-menu-item v-if="!this.showNav" @click="openCloseNav">-->
          <!--            <i class="el-icon-arrow-right"></i>-->
          <!--          </el-menu-item>-->
        </el-menu>
      </el-aside>

      <el-main>

        <profile v-show="mainContent.profile" v-bind:sid="this.sid" v-bind:pswd="this.pswd"></profile>

        <new_password v-if="mainContent.settings" v-bind:sid="this.sid"></new_password>

        <el-table v-if="mainContent.projects" :data="courses.filter(data =>
          !searchKey || JSON.stringify(data).toLocaleLowerCase().includes(searchKey.toLocaleLowerCase()))"
                  style="width: 100%" height="500">

          <el-table-column fixed prop=1 label="Course" width="120"></el-table-column>

          <el-table-column prop=2 label="Project" width="120"></el-table-column>

          <!--          <el-table-column prop="status" label="Status" width="120"></el-table-column>-->

          <el-table-column width="120" align="right">
            <template slot="header" slot-scope="scope">
              <el-input size="mini" v-model="searchKey" placeholder="Search"/>
            </template>
            <template slot-scope="scope">
              <el-button @click="onClickDetail(scope.$index)">Detail</el-button>
            </template>
          </el-table-column>

        </el-table>

        <ProjectDetail v-if="mainContent.showProjectDetail" v-bind:sid="this.sid" v-bind:pswd="this.pswd"
                       v-bind:projectDetail="this.projectDetail" v-bind:groupInfo="this.groupInfo">
        </ProjectDetail>

      </el-main>

    </el-container>
  </div>
</template>

<script>
import profile from './profile'
// import { updateCookie, getCookie, delCookie } from '../assets/js/cookie.js'
import New_password from './new_password'
import ProjectDetail from "./ProjectDetail";

export default {
  name: 'homepage',
  components: {ProjectDetail, New_password, profile},
  props: {},
  data() {
    return {
      //TODO: Data is lost after refresh.
      searchKey: '',
      sid: this.$route.params.sid,
      pswd: this.$route.params.pswd,
      name: '',
      asideWidth: '160px',
      showNav: false,
      mainContent: {
        profile: false,
        projects: false,
        messages: false,
        settings: false,
        showProjectDetail: false
      },
      projectDetail: null,
      groupInfo: null,
      courses: null
    }
  },
  created() {
    console.log('/student_gets_all_projects/')
    this.$axios.post('/student_gets_all_projects/', {sid: this.sid, pswd: this.pswd}).then(res => {
      console.log('all projects', res.data.Data)
      this.courses = res.data.Data
    }).catch(err => {
      console.log(err)
    })
  },
  methods: {
    changeMainContent(item) {
      for (const iter in this.mainContent) {
        if (iter === item) {
          console.log(item, iter)
          this.mainContent[iter] = !this.mainContent[iter]
        } else {
          this.mainContent[iter] = false
        }
      }
    },
    openCloseNav() {
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

    onClickDetail(index) {
      const localCourses = this.courses.filter(data => !this.searchKey ||
        JSON.stringify(data).toLocaleLowerCase().includes(this.searchKey.toLocaleLowerCase()))
      const local_project = localCourses[index]

      this.$axios.post('/student_gets_single_project_information/', {
        sid: this.sid,
        pswd: this.pswd,
        project_id: local_project[0]
      }).then(res => {
        console.log('projectDetail', res.data)
        this.projectDetail = res.data
      }).catch(err => {
        console.log(err)
      })

      this.$axios.post('/student_gets_group_information_in_project/', {
        sid: this.sid,
        pswd: this.pswd,
        project_id: local_project[0]
      }).then(res => {
        console.log('groupInfo', res.data)
        this.groupInfo = res.data
        this.changeMainContent('showProjectDetail')
      }).catch(err => {
        this.projectDetail = null
        console.log(err)
      })
    },

    onClickSettings() {
      this.changeMainContent('settings')
    },

    //TODO: Personal profile request.
    onClickProfile() {
      this.changeMainContent('profile')
      console.log(this.sid, this.name)
    },

    onClickProjects() {
      this.changeMainContent('projects')
    },

    //TODO: New password request.
    onClickNewPassword() {
      // updateCookie('sid', this.sid, 1000 * 60)
    },

    //TODO: Logout request.
    onClickLogout() {
      console.log('logout')
      // delCookie('sid')
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

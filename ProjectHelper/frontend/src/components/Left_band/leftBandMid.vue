<template>
  <div class="left-mid">
    <div class="item-margin" >
      <el-container direction="horizontal">

        <el-aside :width="asideWidth">
          <el-menu default-active="1-4-1" class="nav" :collapse="!showNav" style="background-color: black">
            <el-header v-if="showNav">
              Project Hub
            </el-header>
            <el-header v-if="!showNav">
              PH
            </el-header>
            <el-menu-item @click="onClickProfile" style="color: #FF9900">
              <i class="el-icon-user"></i>
              <span slot="title">My Profile</span>
            </el-menu-item>
            <el-menu-item @click="onClickProjects" style="color: #FF9900">
              <i class="el-icon-folder"></i>
              <span slot="title" @click="onClickProjects">My Projects</span>
            </el-menu-item>
            <el-menu-item style="color: #FF9900">
              <i class="el-icon-message" ></i>
              <span slot="title">Messages</span>
            </el-menu-item>
            <el-menu-item style="color: #FF9900">
              <i class="el-icon-setting" @click="onClickSettings"></i>
              <span slot="title" >Settings</span>
            </el-menu-item>
            <el-menu-item @click="onClickLogout" style="color: #FF9900">
              <i class="el-icon-circle-close" @click="onClickLogout"></i>
              <span slot="title" @click="onClickLogout">Logout</span>
            </el-menu-item>
            <el-menu-item v-if="this.showNav" @click="openCloseNav">
              <i class="el-icon-arrow-left"></i>
            </el-menu-item>
          </el-menu>
        </el-aside>

        <el-main>
          <profile v-show="mainContent.profile" v-bind:sid="this.sid" v-bind:pswd="this.pswd"></profile>

          <new_password v-if="mainContent.settings" v-bind:sid="this.sid"></new_password>

          <AllProjectsList v-show="mainContent.projects" v-bind:pswd="this.pswd" v-bind:sid="this.sid"
                           v-bind:identity="this.identity"></AllProjectsList>
        </el-main>

      </el-container>
<!--      <i class="icon-margin" :class="item.icon"></i>{{ item.title }}-->
    </div>
  </div>
</template>
<script>
import {delCookie, getCookie, updateCookie} from "../../assets/js/cookie";
import AllProjectsList from "../AllProjectsList";
import ProjectDetail from "../ProjectDetail";
import New_password from "../new_password";
import profile from "../profile";

export default {
  name: 'leftBandMid',
  components: { AllProjectsList, ProjectDetail, New_password, profile },
  data () {
    return {
      //TODO: Data is lost after refresh.
      searchKey: '',
      sid: this.$route.params.sid,
      pswd: this.$route.params.pswd,
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
  props: {
    midList: {
      default() {
        return []
      },
    },
  },
  created () {
    console.log('/student_gets_all_projects/')
    this.$axios.post('/student_gets_all_projects/', { sid: this.sid, pswd: this.pswd }).then(res => {
      console.log('all projects', res.data.Data)
      this.courses = res.data.Data
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
    openCloseNav ()
    {
      this.showNav = !this.showNav
    },
    onClickDetail (index) {
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
      console.log('logout')
      // delCookie('sid')
      this.$router.push('/')
    },
  },
}
</script>
<style scoped>
.el-aside{
  position: fixed;
  width: 100%;
  top: 150px;
}
.el-main{
  margin-left: 160px;
}
.left-mid {
  color: rgb(255, 255, 255);
  padding: 0;
  /* background-color: rgb(102, 66, 66); */
}
.item-margin {
  border-right: 3px solid #FF9900;
  /*padding-bottom: 15px;*/
  background-color: black;
  /*margin-top:  100px;*/
}
/*.icon-margin {*/
/*  padding-right: 10px;*/
/*}*/
</style>

<template>
  <div>

    <el-button v-if="!this.displayControl.projectsList" @click="onClickBackToList">Projects List</el-button>

    <el-table v-show="this.displayControl.projectsList"
              :data="projects.filter(data => !searchKey ||
      JSON.stringify(data).toLocaleLowerCase().includes(searchKey.toLocaleLowerCase()))"
              style="width: 100%" height="500">

      <el-table-column fixed prop=1 label="Course" width="120"></el-table-column>

      <el-table-column prop=2 label="Project" width="120"></el-table-column>

      <el-table-column width="120" align="right">
        <template slot="header" slot-scope="scope">
          <el-input size="mini" v-model="searchKey" placeholder="Search"/>
        </template>
        <template slot-scope="scope">
          <el-button @click="onClickDetail(scope.$index)">Detail</el-button>
        </template>
      </el-table-column>
    </el-table>

    <ProjectDetail v-if="this.displayControl.projectDetail"
                   v-bind:sid="this.sid"
                   v-bind:pswd="this.pswd"
                   v-bind:groupInfo="this.groupInfo"
                   v-bind:projectDetail="this.projectDetail"
                   v-bind:identity="this.$props.identity"></ProjectDetail>

    <CreateProject
      v-bind:pswd="this.pswd"
      v-bind:sid="this.sid"
      v-if="this.createProjectForm"></CreateProject>

    <el-button v-if="this.displayControl.createProjectButton" @click="onClickCreateProject">{{ createProjectLiteral }}
    </el-button>

  </div>
</template>

<script>
import ProjectDetail from './ProjectDetail'
import CreateProject from './CreateProject'

export default {
  name: 'AllProjectsList',
  components: { CreateProject, ProjectDetail },
  props: {
    sid: {
      type: String,
      required: true,
    },
    pswd: {
      type: String,
      required: true,
    },
    identity: {
      type: String,
      required: true,
    },
  },
  data () {
    return {
      projects: [],
      searchKey: '',
      projectDetail: '',
      groupInfo: '',
      displayControl: {
        projectsList: true,
        projectDetail: false,
        createProjectButton: this.$props.identity === 'teacher',
        createProjectForm: false,
      },
      createProjectLiteral: 'Create New Project',
    }
  },
  created () {
    this.$axios.post('/student_gets_all_projects/',
      { sid: this.$props.sid, pswd: this.$props.pswd }).then(res => {
      console.log(res.data)
      this.projects = res.data.Data
    }).catch(err => {
      console.log(err)
    })
  },
  methods: {
    onClickCreateProject () {
      this.createProjectForm = !this.createProjectForm
      if (!this.createProjectForm) {
        this.createProjectLiteral = 'Create New Project'
      } else {
        this.createProjectLiteral = '      Cancel      '
      }
    },
    onClickBackToList () {
      this.controlDisplay('projectsList')
    },
    controlDisplay (item) {
      for (const iter in this.displayControl) {
        this.displayControl[iter] = iter === item
      }
    },
    onClickDetail (index) {
      const localProjects = this.projects.filter(data => !this.searchKey ||
        JSON.stringify(data).toLocaleLowerCase().includes(this.searchKey.toLocaleLowerCase()))
      const localProject = localProjects[index]

      this.$axios.post('/student_gets_single_project_information/', {
        sid: this.sid,
        pswd: this.pswd,
        project_id: localProject[0],
      }).then(res => {
        console.log('projectDetail', res.data)
        this.projectDetail = res.data
      }).catch(err => {
        console.log(err)
      })
      this.$axios.post('/student_gets_group_information_in_project/', {
        sid: this.sid,
        pswd: this.pswd,
        project_id: localProject[0],
      }).then(res => {
        console.log('groupInfo', res.data)
        this.groupInfo = res.data
        this.controlDisplay('projectDetail')
      }).catch(err => {
        this.projectDetail = null
        console.log(err)
      })
    },
  },
}
</script>

<style scoped>

</style>

<template>
  <div>

    <el-button v-if="!this.displayControl.projectsList" @click="onClickBackToList">Projects List</el-button>

    <el-table v-show="this.displayControl.projectsList"
              :data="projects.filter(data => !searchKey ||
      JSON.stringify(data).toLocaleLowerCase().includes(searchKey.toLocaleLowerCase()))"
              style="width: 100%" height="500"
              :header-cell-style="{background:'#F7F8F8',color:'#606266'}">

      <!--      sortable is not supported-->
      <el-table-column fixed prop=1 label="Course" width="400"></el-table-column>

      <!--      sortable is not supported-->
      <el-table-column prop=2 label="Project" width="400"></el-table-column>

      <el-table-column width="200" align="right">
        <template slot="header" slot-scope="scope">
          <el-input size="mini" v-model="searchKey" placeholder="Search"/>
        </template>
        <template slot-scope="scope">
          <el-button @click="onClickDetail(scope.$index)">Detail</el-button>
          <el-button v-if="identity === 'teacher'" @click="onClickDeleteProject(scope.$index)">Delete</el-button>
        </template>
      </el-table-column>


    </el-table>

    <ProjectDetail v-if="this.displayControl.projectDetail"
                   v-bind:sid="this.sid"
                   v-bind:projectId="this.projectId"
                   v-bind:courseId="this.courseId"></ProjectDetail>

    <CreateProject
        v-bind:sid="this.sid"
        v-if="this.displayControl.createProjectForm">
    </CreateProject>

    <el-button v-if="this.identity === 'teacher'" @click="onClickCreateProject">{{ createProjectLiteral }}
    </el-button>

  </div>
</template>

<script>
import ProjectDetail from './ProjectDetail'
import CreateProject from './CreateProject'

export default {
  name: 'ProjectList',
  components: { CreateProject, ProjectDetail },
  props: {},
  data () {
    return {
      projects: [],
      searchKey: '',
      projectDetail: '',
      groupInfo: '',
      displayControl: {
        projectsList: true,
        projectDetail: false,
        createProjectButton: true,
        createProjectForm: false,
      },
      createProjectLiteral: 'Create New Project',
      identity: '',
      sid: '',
      projectId: '',
      courseId: '',
      privileges: {},
    }
  },
  created () {
    this.$axios.post('/is_teacher/', {}).then(res => {
      console.log(res)
      if (res.data['IsTeacher'] === 1) {
        this.identity = 'teacher'
      }
      else {
        this.identity = ''
      }
      this.loadProjects()
    }).catch(err => {
      console.log(err)
    })
  },
  methods: {
    loadProjects() {
      this.$axios.post('/student_gets_all_projects/', {}).then(res => {
        this.projects = res.data['projects']
        this.sid = res.data['sid']
        this.displayControl.createProjectButton = (this.identity === 'teacher')
      }).catch(err => {
        console.log('err', err)
      })
    },
    onClickDeleteProject (index) {
      const localProjects = this.projects.filter(data => !this.searchKey ||
          JSON.stringify(data).toLocaleLowerCase().includes(this.searchKey.toLocaleLowerCase()))
      const localProject = localProjects[index]
      this.projectId = localProject[0]
      this.$axios.post('/delete_project/', {'project_id': this.projectId}).then(res => {
        console.log(res)
        this.loadProjects()
      }).catch(err => {
        console.log('err', err)
      })
    },
    onClickCreateProject () {
      this.displayControl.createProjectForm = !this.displayControl.createProjectForm
      if (!this.displayControl.createProjectForm) {
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
      this.projectId = localProject[0]
      this.courseId = localProject[3]
      this.controlDisplay('projectDetail')
    },
  },
}
</script>

<style scoped>

</style>

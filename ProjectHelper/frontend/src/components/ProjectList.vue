<template>
  <div>

    <el-button v-if="!this.displayControl.projectsList" @click="onClickBackToList">Projects List</el-button>

    <el-table v-show="this.displayControl.projectsList"
              :data="projects.filter(data => !searchKey ||
      JSON.stringify(data).toLocaleLowerCase().includes(searchKey.toLocaleLowerCase()))"
              style="width: 100%" height="500">

      <el-table-column fixed prop=1 label="Course" width="350"></el-table-column>

      <el-table-column prop=2 label="Project" width="350"></el-table-column>

      <el-table-column width="350" align="right">
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
                   v-bind:projectId="this.projectId"
                   v-bind:courseId="this.courseId"></ProjectDetail>

    <CreateProject
        v-bind:sid="this.sid"
        v-if="this.displayControl.createProjectForm"></CreateProject>

    <el-button v-if="this.displayControl.createProjectButton" @click="onClickCreateProject">{{ createProjectLiteral }}
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
        createProjectButton: false,
        createProjectForm: false,
      },
      createProjectLiteral: 'Create New Project',
      identity: '',
      sid: '',
      projectId: '',
      courseId: '',
    }
  },
  created () {
    this.$axios.post('/student_gets_all_projects/', {}).then(res => {
      console.log('project', res.data)
      this.projects = res.data['projects']
      this.sid = res.data['sid']
      this.$axios.post('/get_identity/', {}).then(res => {
        this.identity = res.data['identity']
        this.displayControl.createProjectButton = (this.identity === 'teacher')
      }).catch(err => {
        console.log('err', err)
      })
    }).catch(err => {
      console.log('err', err)
    })

  },
  methods: {
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
      console.log(this.projectId, this.courseId, this.sid)

      this.controlDisplay('projectDetail')


      // this.$axios.post('/student_gets_single_project_information/', {
      //   'projectId': localProject[0],
      // }).then(res => {
      //   console.log('res', res)
      //   this.projectDetail = res.data
      //   this.projectDetail['projectId'] = localProject[0]
      //   this.courseId = localProject[3]
      //   this.$axios.post('/student_gets_group_information_in_project/', {
      //     sid: this.sid,
      //     project_id: localProject[0],
      //   }).then(res => {
      //     console.log('groupInfo', res.data)
      //     this.groupInfo = res.data
      //   }).catch(err => {
      //     this.projectDetail = null
      //     console.log(err)
      //   })
      // }).catch(err => {
      //   console.log(err)
      // })


    },
  },
}
</script>

<style scoped>

</style>

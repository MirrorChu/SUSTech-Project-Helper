<template>
  <div>

    <el-table
      :data="projects.filter(data => !searchKey ||
      JSON.stringify(data).toLocaleLowerCase().includes(searchKey.toLocaleLowerCase()))"
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

  </div>
</template>

<script>
export default {
  name: 'AllProjectsList',
  props: {
    sid: {
      type: String,
      required: true
    },
    pswd: {
      type: String,
      required: true
    }
  },
  data () {
    return {
      projects: [],
      searchKey: '',
      projectDetail: '',
      groupInfo: '',
    }
  },
  created () {
    this.$axios.post('/student_gets_all_projects/', { sid: this.$props.sid, pswd: this.$props.pswd }).then(res => {

    }).catch(err => {

    })
  },
  methods: {
    onClickDetail () {
      const localProjects = this.courses.filter(data => !this.searchKey ||
        JSON.stringify(data).toLocaleLowerCase().includes(this.searchKey.toLocaleLowerCase()))
      const localProject = localProjects[index]

      this.$axios.post('/student_gets_single_project_information/', {
        sid: this.sid,
        pswd: this.pswd,
        project_id: localProject[0]
      }).then(res => {
        console.log('projectDetail', res.data)
        this.projectDetail = res.data
      }).catch(err => {
        console.log(err)
      })

      this.$axios.post('/student_gets_group_information_in_project/', {
        sid: this.sid,
        pswd: this.pswd,
        project_id: localProject[0]
      }).then(res => {
        console.log('groupInfo', res.data)
        this.groupInfo = res.data
        this.changeMainContent('showProjectDetail')
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

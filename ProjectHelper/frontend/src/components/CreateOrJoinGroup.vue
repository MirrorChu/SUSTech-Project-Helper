<template>
  <div>
    <el-button @click="onClickCreateGroup">Create Group</el-button>
    <el-button @click="onClickJoinGroup">Join Group</el-button>

    <el-form v-if="this.showCreateGroupForm">
      <h1>Create Group</h1>
      <el-form-item>
        <el-input v-model="createGroupName" placeholder="Group Name" clearable></el-input>
      </el-form-item>
      <el-form-item label="Introduction">
        <el-input type="textarea" :rows="2" placeholder="Introduction" v-model="createIntroduction"
                  clearable></el-input>
      </el-form-item>
      <el-form-item>
        <el-button @click="onClickConfirmCreateGroup">Confirm Create Group</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
export default {
  name: 'CreateOrJoinGroup',
  props: {
    sid: {
      type: String,
      required: true,
    },
    pswd: {
      type: String,
      required: true,
    },
    projectId: {
      required: true,
    },
  },
  data () {
    return {
      showCreateGroupForm: false,
      showJoinGroupList: false,
      createGroupName: '',
      createIntroduction: '',
      joinGroupList: [],
    }
  },
  methods: {
    onClickCreateGroup () {
      this.showCreateGroupForm = !this.showCreateGroupForm
      this.showJoinGroupList = false
      if (!this.showCreateGroupForm) {
        this.createGroupName = ''
        this.createIntroduction = ''
      }
    },
    onClickJoinGroup () {
      this.showJoinGroupList = !this.showJoinGroupList
      this.showCreateGroupForm = false
      if (!this.showJoinGroupList) {
        this.createGroupName = ''
        this.createIntroduction = ''
      } else {
        //  TODO: Implement this.
      }
    },
    onClickConfirmCreateGroup () {
      if (this.createGroupName.length === 0) {
        alert('Group name cannot be empty!')
      } else {
        this.$axios.post('/student_creates_group/', {
          sid: this.sid,
          pswd: this.pswd,
          project_id: this.projectId,
          group_name: this.createGroupName,
          introduction: this.createIntroduction
        }).then(res => {
          console.log(res.data)
        }).catch(err => {
          alert(err.data)
        })
      }
    },
  },
}
</script>

<style scoped>

</style>

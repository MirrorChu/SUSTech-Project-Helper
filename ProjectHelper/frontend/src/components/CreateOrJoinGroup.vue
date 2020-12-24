<template>
  <div>
    <el-button v-if="!showCreateGroupForm" @click="onClickShowCreateGroup">Create Group</el-button>
    <el-button v-if="!showJoinGroupList" @click="onClickShowJoinGroup">Join Group</el-button>

    <el-form v-if="this.showCreateGroupForm">
      <h3 style="color:#003371">Create Group</h3>
      <el-form-item label="Group Name">
        <el-input v-model="createGroupName" placeholder="Group Name" clearable></el-input>
      </el-form-item>
      <el-form-item label="Introduction">
        <el-input type="textarea" :rows="3" placeholder="Introduction" v-model="createIntroduction"
                  clearable></el-input>
      </el-form-item>
      <el-form-item>
        <el-button @click="onClickConfirmCreateGroup">Confirm Create Group</el-button>
      </el-form-item>
    </el-form>
    <el-divider></el-divider>
    <div v-if="showJoinGroupList">
      <el-table
        :data="joinGroupList"
        stripe
        style="width: 100%">
        <el-table-column
          prop="group_name"
          label="Group Name">
        </el-table-column>
        <el-table-column
          prop="captain_name"
          label="Captain Name">
        </el-table-column>
        <el-table-column
          prop="namelist"
          label="Members">
        </el-table-column>
        <el-table-column>
          <template slot-scope="scope">
            <el-button @click="onClickJoinGroup(scope.row.group_id)">Apply to Join</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
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
    onClickShowCreateGroup () {
      this.showCreateGroupForm = !this.showCreateGroupForm
      this.showJoinGroupList = false
      if (!this.showCreateGroupForm) {
        this.createGroupName = ''
        this.createIntroduction = ''
      }
    },
    onClickShowJoinGroup () {
      this.showJoinGroupList = !this.showJoinGroupList
      this.showCreateGroupForm = false
      if (!this.showJoinGroupList) {
        this.createGroupName = ''
        this.createIntroduction = ''
      } else {
        this.pullgroupData()
      }
    },
    onClickJoinGroup (group_id)
    {
      this.$axios.post('/send_mail_to_apply/', {
        t_sid: this.sid,
        group_id: group_id,
      }).then(res =>
      {
        console.log('apply', res.data)
      }).catch(err =>
      {
        console.log(err);
      });
    },
    onClickConfirmCreateGroup () {
      if (this.createGroupName.length === 0) {
        this.$message.error('Group name cannot be empty!')
      } else {
        this.$axios.post('/student_creates_group/', {
          sid: this.sid,
          project_id: this.projectId,
          group_name: this.createGroupName,
          introduction: this.createIntroduction
        }).then(res => {
          console.log('ConfirmCreateProject',res.data)
        }).catch(err => {
          this.$message.error(err.data)
        })
      }
    },
    pullgroupData ()
    {
      this.$axios.post('/teacher_get_situation_in_project/', {
        project_id: this.projectId,
      }).then(res =>
      {
        console.log('sss', res.data)
        if (res.data.TeacherGetSituationInProject === 'success')
        {
          this.joinGroupList = res.data.Data
        }
      }).catch(err =>
      {
        console.log(err);
      });
    }
  },
}
</script>

<style scoped>

</style>

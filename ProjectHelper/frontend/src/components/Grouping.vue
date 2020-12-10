<template>
  <el-table
    :data="groupData"
    stripe
    style="width: 100%">
    <el-table-column
      prop="group_id"
      label="GROUP ID">
    </el-table-column>
    <el-table-column
      prop="captain_name"
      label="CAPTAIN NAME">
    </el-table-column>
    <el-table-column
      prop="namelist"
      label="MEMBERS">
    </el-table-column>
    <el-table-column
      label="ACTION">
      <template slot-scope="scope">
        <el-button @click="onClickShowGroupDetail(scope.row)">Detail</el-button>
      </template>
    </el-table-column>
  </el-table>

  <div>
    <el-dialog title="Group Data" :visible.sync="dialogGroupDataVisible">
      <el-form ref="form" label-position="left" label-width="80px">
        <el-form-item label="GROUP ID">
          <el-row>{{ groupInformation.group_id }}</el-row>
        </el-form-item>
      <div v-for="(stu_sid,index) in groupInformation.member_sid">
        <el-form-item label="Name">
          <el-row>{{ stu_sid+' '+groupInformation.membername[index] }}<el-button @click="onClickKick(stu_sid, groupInformation.group_id)">Kick</el-button></el-row>
        </el-form-item>
      </div>
        <el-form-item>
          <el-input v-model="sid_invite" placeholder="input sid of the one you want to invite"></el-input>
          <el-button @click="onClickInvite(groupInformation.group_id)">Invite</el-button>
        </el-form-item>

      </el-form>
    </el-dialog>
  </div>
</template>

<script>
    export default {
        name: "Grouping",
      data() {
        return {
          groupData: '',
          dialogGroupDataVisible: false,
          groupInformation: '',
          sid_invite: '',
        }
      },
      created() {
          this.pullGroupingData()
      },
      methods: {
        pullGroupingData ()
        {
          this.$axios.post('/', {
            project_id: this.project_id,
          }).then(res => {
            console.log(res.data)
            this.groupData = res.data
          }).catch(err => {
            console.log(err)
          })
        },
        onClickShowGroupDetail()
        {
          this.dialogGroupDataVisible = true
        },
        onClickInvite(group_id)
        {
          this.$axios.post('/', {
            group_id: group_id,
            sid_invite: this.sid_invite,
          }).then(res => {
            console.log(res.data)
          }).catch(err => {
            console.log(err)
          })
        },
        onClickKick(sid, group_id)
        {
          this.$axios.post('/', {
            group_id: group_id,
            sid_kick: sid,
          }).then(res => {
            console.log(res.data)
          }).catch(err => {
            console.log(err)
          })
        },
      },
    }
</script>

<style scoped>

</style>

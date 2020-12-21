<template>
  <div>
    <h2>Group Info</h2>
    Group Introduction: {{ this.$props.groupInfo.group_introduction }}
    <br>
    Group Name: {{ this.$props.groupInfo.group_name }}
    <br>
    Captain Name: {{ this.$props.groupInfo.captain_name }}
    <br>
    Members: {{ this.$props.membersList }}
    <br>
    <el-divider></el-divider>
    <h2>Wanna invite someone?</h2>
    <el-select v-model="toInviteList" multiple clearable placeholder="select people to invite">
      <el-option
          v-for="item in invitableList"
          :key="item.value"
          :label="item.label"
          :value="item.value">
      </el-option>
    </el-select>
    <el-button @click="onClickInvite">invite</el-button>
    <el-divider></el-divider>
  </div>
</template>

<script>
export default {
  props: {
    groupInfo: {
      required: true,
    },
    membersList: {
      required: true,
    },
    sid: {
      type: String,
      required: true,
    },
    pswd: {
      type: String,
      requires: true,
    },
    projectId: {
      type: Number,
      required: true,
    },
  },
  created () {
    this.$axios.post('/teacher_get_single_in_project/', { 'project_id': this.$props.projectId }).then(res => {
      console.log(res)
      const tempList = res.data['Data']
      for (let i = 0; i < tempList.length; i += 1) {
        const studentToInvite = {
          'label': tempList[i]['sid'],
          'value': tempList[i]['sid'],
          'name': tempList[i]['realname'],
        }
        this.invitableList.push(studentToInvite)
      }
    }).catch(err => {
      console.log(err)
    })
  },
  data () {
    return {
      toInviteList: [],
      invitableList: [],
    }
  },
  methods: {
    onClickInvite () {
      if (this.toInviteList.length === 0) {
        alert('You are not inviting anyone!')
      } else {
        console.log(this.toInviteList)
        for (let i = 0; i < this.toInviteList.length; i += 1) {
          const dataBlock = {'group_id': this.$props.groupInfo['group_id'], 't_sid': this.toInviteList[i]}
          console.log(dataBlock)
          this.$axios.post('/send_mail_to_invite/', dataBlock).then(res => {
            console.log(res)
          }).catch(err => {
            console.log(err)
          })
        }
        alert('You invited ' + this.toInviteList + '.')
      }
    },
  },
  name: 'GroupInfo',
}
</script>

<style scoped>

</style>

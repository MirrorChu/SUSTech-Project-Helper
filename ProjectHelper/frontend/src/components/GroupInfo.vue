<template>
  <div>

    <div>
      <h2>Group Info</h2>
      <div v-show="!this.edit">
        Group Name: {{ this.groupInfo.group_name }}
        <br>
        Group Introduction: {{ this.groupInfo.group_introduction }}
        <br>
        Captain: {{ this.groupInfo.captain_name }}
        <br>
        Members: <span v-if="this.groupInfo.members&&this.groupInfo.members.length !== 0"> {{ this.membersList }}</span><span v-else>No memeber</span>
      </div>

      <div v-if="this.edit">
        Group Name: <el-input v-model="group_name" ></el-input> <br>
        Group Introduction: <el-input v-model="group_introduction" ></el-input> <br>
        Captain: {{this.groupInfo.captain_name}} <br>
        Members: <br>

        <span v-if="this.groupInfo.members&&this.groupInfo.members.length !== 0">
          <div v-for="(item,index) in this.groupInfo.members_name">
            <span>{{ item }}</span> &nbsp <el-button @click="onClickKick(index)">Kick</el-button>
          </div>
        </span>
        <span v-else>
          No memeber
        </span>
      </div>

      <br>
      <el-button v-show="!this.edit" @click="onClickEdit">Edit</el-button>
      <el-button v-show="this.edit" @click="onClickConfirmEdit">Confirm Edit</el-button>

      <el-divider></el-divider>
      <h2>Wanna invite someone?</h2>
      <el-select v-model="toInviteList" multiple clearable placeholder="select people to invite">
        <el-option
            v-for="item in invitableList"
            :key="item.value"
            :label="item.label"
            :value="item.value">
          <span>{{ item.label}}  &nbsp {{ item.name }}</span>
        </el-option>
      </el-select>
      <el-button @click="onClickInvite">invite</el-button>
      <el-divider></el-divider>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    project_id: {
      type: Number,
      required: true,
    },
  },
  data () {
    return {
      toInviteList: [],
      invitableList: [],
      edit: false,
      group_introduction: '',
      group_name: '',
      membersList: '',
      group_introduction_edit: '',
      group_name_edit: '',
      membersList_edit: '',
      groupInfo: [],
      status: '',
    }
  },
  created () {
    this.pullData()
  },
  methods: {
    pullSingleData()
    {
      this.invitableList = []
      this.$axios.post('/teacher_get_single_in_project/',
        {
          'project_id': this.$props.project_id,
        }).then(res => {
          console.log(res)
          const tempList = res.data['Data']
          for (let i = 0; i < tempList.length; i++) {
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
    onClickInvite ()
    {
      if (this.toInviteList.length === 0) {
        alert('You are inviting air!')
      } else {
        console.log(this.toInviteList)
        for (let i = 0; i < this.toInviteList.length; i += 1) {
          const dataBlock = {'group_id': this.groupInfo['group_id'], 't_sid': this.toInviteList[i]}
          console.log(dataBlock)
          this.$axios.post('/send_mail_to_invite/', dataBlock).then(res => {
            console.log(res)
          }).catch(err => {
            console.log(err)
          })
        }
        this.pullData()
        console.log('You invited ' + this.toInviteList + '.')
      }
    },
    onClickEdit()
    {
      this.edit = true
      this.group_name = this.groupInfo.group_name
      this.group_introduction = this.groupInfo.group_introduction
    },
    onClickConfirmEdit()
    {
      this.$axios.post('/change_group/', {
        group_name: this.group_name,
        group_introduction: this.group_introduction,
        group_id: this.groupInfo.group_id,
      }).then(res => {
        console.log(res.data)
        this.edit = false
        this.pullData()
      }).catch(err => {
        console.log(err);
      });

    },
    pullData()
    {
      this.$axios.post('/student_gets_group_information_in_project/',
        {
          'project_id': this.$props.project_id
        }).
      then(res => {
        console.log(res)
        this.groupInfo = res.data;
        if (this.groupInfo == null) {
          this.status = 'You are not in a group!';
        }
        else if (this.groupInfo['StudentGetsGroupInformationInProject'] === 'no group') {
          this.status = 'You are not in a group!';
        }
        else if (this.groupInfo['StudentGetsGroupInformationInProject'] == null) {
          for (let i = 0; i < this.groupInfo['members'].length; i++) {
            this.membersList = this.membersList + this.groupInfo['members_name'][i] + '  ';
          }
          this.status = ''
        }
        else {
          this.status = 'unknown';
        }
        this.pullSingleData()
      }).
      catch(err => {
        console.log(err);
      });
    },
    onClickKick(index)
    {
      console.log(this.groupInfo.group_id, this.groupInfo.members[index])
      this.$axios.post('/captain_kick_member/', {
        "group_id": this.groupInfo.group_id,
        "t_sid": this.groupInfo.members[index],
        }).
      then(res => {
        console.log("djshvjksdbvbdb",res)
        this.pullData()
      }).
      catch(err => {
        console.log(err);
      });
    },
  },
  name: 'GroupInfo',
}
</script>

<style scoped>

</style>

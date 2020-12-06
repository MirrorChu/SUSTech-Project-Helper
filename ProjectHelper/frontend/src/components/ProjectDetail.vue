<template>
  <div style="background-color: #F7F8F8">
    <div v-if="this.displayControl.projectDetail" >
      <el-card class="details">
        <div>
          Course Name: {{ this.$props.projectDetail.course_name }}
        </div>
        <div>
          Project Name: {{ this.$props.projectDetail['project_name'] }}
        </div>
        <div>
          <GroupInfo v-if="this.$props.groupInfo.StudentGetsGroupInformationInProject == null"
                     v-bind:group-info="this.$props.groupInfo" v-bind:members-list="this.membersList"
                     v-bind:sid="this.$props.sid" v-bind:pswd="this.$props.pswd"></GroupInfo>
          <h1 v-if="!(this.$props.groupInfo.StudentGetsGroupInformationInProject == null)">You are not in any groups!</h1>
          <CreateOrJoinGroup v-if="!(this.$props.groupInfo.StudentGetsGroupInformationInProject == null)"
                             v-bind:sid="this.$props.sid" v-bind:pswd="this.$props.pswd"
                             v-bind:projectId="this.$props.groupInfo.project_id"></CreateOrJoinGroup>

          <el-form :inline="true" :model="target_user" class="querypersonalprofile">
            <el-form-item label="The profile you want to view">
              <el-input v-model="target_user.sid" placeholder="Input his or her sid"></el-input>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="onQueryPersonalProfile">Query</el-button>
            </el-form-item>
          </el-form>
        </div>
      </el-card>
      <!--      <el-button @click="onClickToPersonalProfile">TesttoProfile</el-button>-->
    </div>

    <div>
      <PersonalProfile v-if="this.displayControl.PersonalProfile" v-bind:sid="this.sid" v-bind:pswd="this.pswd"
                       v-bind:personalprofile="this.personalprofile" v-bind:tags="this.tags">
      </PersonalProfile>
      <el-button v-if="this.displayControl.PersonalProfile" @click="onClickBackToProjectDetail">Back to Projects
        Detail
      </el-button>
    </div>

    <div>
      <EventList v-bind:sid="this.$props.sid"
                 v-bind:pswd="this.$props.pswd"
                 v-bind:identity="this.$props.identity"
                 v-bind:projectId="this.groupInfo.project_id">
      </EventList>
    </div>

  </div>
</template>

<script>
import GroupInfo from './GroupInfo'
import CreateOrJoinGroup from './CreateOrJoinGroup'
import PersonalProfile from './PersonalProfile'
import EventList from './EventList'

export default {
  components: { EventList, Event, CreateOrJoinGroup, GroupInfo, PersonalProfile },
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
    projectDetail: {
      required: true,
    },
    groupInfo: {
      required: true,
    },
  },
  created () {
    //Use == instead of === here.
    if (this.$props.groupInfo == null) {
      this.status = 'You are not in a group!'
    } else if (this.$props.groupInfo.StudentGetsGroupInformationInProject === 'no group') {
      this.status = 'You are not in a group!'
    } else if (this.$props.groupInfo.StudentGetsGroupInformationInProject == null) {
      console.log('access group info success')
      console.log(this.$props.groupInfo['members'])
      for (let i = 0; i < this.$props.groupInfo['members'].length; i++) {
        this.membersList = this.membersList + this.$props.groupInfo['members'][i] + '  '
      }
    } else {
      this.status = 'unknown'
    }
  },
  data () {
    return {
      membersList: '',
      status: '',
      personalprofile: '',
      tags: '',
      displayControl: {
        projectDetail: true,
        PersonalProfile: false,
      },
      target_user: {
        sid: '',
      },
      eventList: [],
    }
  },
  methods: {
    controlDisplay (item) {
      for (const iter in this.displayControl) {
        this.displayControl[iter] = iter === item
      }
    },
    onClickBackToProjectDetail () {
      this.controlDisplay('projectDetail')
    },
    onClickToPersonalProfile () {
      this.controlDisplay('PersonalProfile')
    },
    onQueryPersonalProfile () {
      this.$axios.post('/student_gets_all_tags/', {
        sid: this.sid,
        pswd: this.pswd,
        sid_target: this.target_user.sid,
      }).then(res => {
        console.log('tags', res.data)
        this.tags = res.data
      }).catch(err => {
        console.log(err)
      })

      this.$axios.post('/show_other_personal_data/', {
        sid: this.sid,
        pswd: this.pswd,
        sid_target: this.target_user.sid,
      }).then(res => {
        console.log('PersonalProfile', res.data)
        console.log(res.data.ShowOtherPersonalDataCheck)
        console.log(res.data['ShowOtherPersonalDataCheck'])
        if (res.data.ShowOtherPersonalDataCheck === 'ShowPersonalData success!') {
          this.personalprofile = res.data
          this.controlDisplay('PersonalProfile')
        } else {
          alert('No such user!')
        }
      }).catch(err => {
        this.tags = null
        console.log(err)
      })
    },
  },
  name: 'ProjectDetail',
}
</script>

<style scoped>
.el-card{
  font-family: Verdana;
  background-color: #F7F8F8;
  border-color:whitesmoke;
  align-content: center;
  text-align: center;
  line-height: 50px;
}
</style>

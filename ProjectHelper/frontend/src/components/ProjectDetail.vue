<template>
  <div>
    <div v-if="this.displayControl.projectDetail">
      <div>
        Course Name: {{ this.$props.projectDetail['courseName'] }}
      </div>
      <div>
        Project Name: {{ this.$props.projectDetail['projectName'] }}
      </div>
      <div>
        <div v-if="this.identity !== 'teacher'">
          <GroupInfo v-if="this.$props.groupInfo.StudentGetsGroupInformationInProject == null"
                     v-bind:group-info="this.$props.groupInfo" v-bind:members-list="this.membersList"
                     v-bind:sid="this.$props.sid"></GroupInfo>
          <h1 v-if="!(this.$props.groupInfo.StudentGetsGroupInformationInProject == null)">You are not in any
            groups!</h1>
          <CreateOrJoinGroup
              v-if="!(this.$props.groupInfo.StudentGetsGroupInformationInProject == null)"
              v-bind:sid="this.$props.sid"
              v-bind:projectId="this.$props.projectDetail.project_id"></CreateOrJoinGroup>
        </div>


        <div>
          <el-form :inline="true" :model="target_user" class="querypersonalprofile">
            <el-form-item label="The profile you want to view">
              <el-input v-model="target_user.sid" placeholder="Input his or her sid"></el-input>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="onQueryPersonalProfile">Query</el-button>
            </el-form-item>
          </el-form>
        </div>

      </div>


    </div>

    <div>
      <PersonalProfile v-if="this.displayControl.PersonalProfile" v-bind:sid="this.sid"
                       v-bind:personalprofile="this.personalprofile">
      </PersonalProfile>
      <el-button v-if="this.displayControl.PersonalProfile" @click="onClickBackToProjectDetail">Back to Projects
        Detail
      </el-button>
    </div>

    <div>
      <el-dialog title="Profile" :visible.sync="dialogPersonalProfileVisible">
        <el-form ref="form" label-position="left" label-width="80px">
          <el-form-item label="SID">
            <el-row>{{ this.personalprofile.sid }}</el-row>
          </el-form-item>

          <el-form-item label="Name">
            <el-row>{{ this.personalprofile.realname }}</el-row>
          </el-form-item>

          <el-form-item label="Gender">
            <el-row>{{ this.personalprofile.gender }}</el-row>
          </el-form-item>

          <el-form-item label="E-Mail">
            <el-row>{{ this.personalprofile.email }}</el-row>
          </el-form-item>

          <el-form-item label="Mobile">
            <el-row>{{ this.personalprofile.mobile }}</el-row>
          </el-form-item>

          <el-form-item label="Address">
            <el-row>{{ this.personalprofile.address }}</el-row>
          </el-form-item>

          <el-form-item label="Tag">
            <li v-for="item in this.tags.Data">
              <el-badge :value="item.likes">
                <el-button @click="onClickLike(item.tag_id)">{{ item.tag_name }}</el-button>
              </el-badge>
            </li>
          </el-form-item>
        </el-form>
      </el-dialog>
    </div>

    <div>
      <h2>Advertisement</h2>
      <el-card>
        <el-collapse v-show="advertisementData !== ''">
          <el-collapse-item v-for="item in advertisementData" :title=item.titlee :name=item.id>
            <div>{{ item.content }}</div>
          </el-collapse-item>
        </el-collapse>
        <div v-show="advertisementData === ''">There is no advertisement!</div>
      </el-card>

      <el-card  v-if="this.identity !== 'teacher'">
        <div>
          <h3>Upload AD</h3>
          <el-form>
            <el-form-item label="Title">
              <el-input v-model="advertisement_title" placeholder="the title of advertisement"></el-input>
            </el-form-item>
            <el-form-item label="Content">
              <el-input type="textarea" :rows="3" placeholder="the content of advertisement"
                        v-model="advertisement_content"></el-input>
            </el-form-item>
            <el-form-item>
              <el-button @click="onClickUploadAdvertisement()">Upload Advertisement</el-button>
            </el-form-item>
          </el-form>
        </div>
      </el-card>
    </div>

    <div v-if="this.identity === 'teacher'">
      <el-card>
        <Grouping v-bind:project_id="this.$props.projectDetail.project_id"></Grouping>

      </el-card>
    </div>

    <div>
      <EventList v-bind:sid="this.$props.sid"
                 v-bind:projectId="this.$props.projectDetail.project_id">
      </EventList>
    </div>
  </div>
</template>

<script>
import GroupInfo from './GroupInfo'
import CreateOrJoinGroup from './CreateOrJoinGroup'
import PersonalProfile from './PersonalProfile'
import EventList from './EventList'
import Grouping from './Grouping'

export default {
  components: { Grouping, EventList, Event, CreateOrJoinGroup, GroupInfo, PersonalProfile },
  props: {
    sid: {
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
      dialogPersonalProfileVisible: false,
      advertisementData: '',
      eventList: [],
      advertisement_content: '',
      advertisement_title: '',
      identity: '',
    }
  },
  created () {
    this.$axios.post('/get_identity/', {}).then(res => {
      this.identity = res.data['identity']
    }).catch(err => {
      console.log('err', err)
    })
    this.sid = this.$props.sid
    this.pulladvertisementData()
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
  methods: {
    controlDisplay (item) {
      for (const iter in this.displayControl) {
        this.displayControl[iter] = iter === item
      }
    },
    onClickBackToProjectDetail () {
      this.controlDisplay('projectDetail')
    },
    onQueryPersonalProfile () {
      this.pulltagData()

      this.$axios.post('/show_other_personal_data/', {
        sid: this.sid,
        sid_target: this.target_user.sid,
      }).then(res => {
        console.log('PersonalProfile', res.data)
        console.log(res.data.ShowOtherPersonalDataCheck)
        console.log(res.data['ShowOtherPersonalDataCheck'])
        if (res.data.ShowOtherPersonalDataCheck === 'ShowPersonalData success!') {
          this.personalprofile = res.data
          // this.controlDisplay('PersonalProfile')
          this.dialogPersonalProfileVisible = true
        } else {
          alert('No such user!')
        }
      }).catch(err => {
        this.tags = null
        console.log(err)
      })
    },
    onClickLike (id) {
      console.log('hello')
      console.log(typeof id)
      this.$axios.post('/student_like_tag/', {
        sid: this.sid,
        tag_target: id,
      }).then(res => {

        if (res.data.StudentLikeTag === 'no like') {
          console.log('delike success')
        } else if (res.data.StudentLikeTag === 'like') {
          console.log('like success')
        } else {
          alert('failed')
        }
        this.pulltagData()
      }).catch(err => {
        console.log(err)
      })
    },
    pulltagData () {
      this.$axios.post('/student_gets_all_tags/', {
        sid: this.sid,
        sid_target: this.target_user.sid,
      }).then(res => {
        this.tags = res.data
        console.log('now this.tags', this.tags)
      }).catch(err => {
        console.log(err)
      })
    },
    pulladvertisementData () {
      this.$axios.post('/student_gets_all_ad/', {
        project_id: this.$props.projectDetail.project_id,
      }).then(res => {
        console.log('ad', res.data)
        if (res.data.StudentGetAllAd === 'success') {
          this.advertisementData = res.data.Data
        } else {
          this.advertisementData = ''
        }
      }).catch(err => {
        console.log(err)
      })
    },
    onClickUploadAdvertisement () {
      if (this.$props.groupInfo.StudentGetsGroupInformationInProject == null) {
        this.$axios.post('/student_publish_request/', {
          project_id: this.$props.projectDetail.project_id,
          content: this.advertisement_content,
          title: this.advertisement_title,
          group_id: this.$props.groupInfo.group_id,
        }).then(res => {
          console.log('up ad', res.data)
          this.pulladvertisementData()
        }).catch(err => {
          console.log(err)
        })
      } else {
        this.$axios.post('/student_publish_apply/', {
          project_id: this.$props.projectDetail.project_id,
          content: this.advertisement_content,
          title: this.advertisement_title,
        }).then(res => {
          console.log('up ad', res.data)
          this.pulladvertisementData()
        }).catch(err => {
          console.log(err)
        })
      }
    },
  },
  name: 'ProjectDetail',
}
</script>

<style scoped>

</style>

<template>
  <div class="project_detail">
    <el-row :gutter="2"><el-col :span="10" >
      <div v-if="this.displayControl.projectDetail">
        <h1 style="font-family: Verdana, serif;">Project Info</h1>
        <el-card>

          <div>
            Course Name: {{ this.projectDetail['courseName'] }}
          </div>

          <div v-if="!this.edit">
            <div>
              Project Name: {{ this.projectDetail['projectName'] }}
            </div>

            <div>
              Project Introduction: {{ this.projectDetail['projectIntroduction'] }}
            </div>

            <div>
              <div v-for="(value, key) in this.file_dict">
                <el-link :href="value" target="_blank" type="primary">{{ key }}</el-link>
              </div>
            </div>
          </div>
          <el-form v-else>
            <el-form-item label="Project Name">
              <el-input v-model="projectDetail['projectName']"></el-input>
            </el-form-item>

            <el-form-item label="Project Introduction">
              <el-input v-model="projectDetail['projectIntroduction']" type="textarea"></el-input>
            </el-form-item>

            <el-form-item label="Upload File">
              <el-upload
                drag
                action="/api/test"
                :headers="{'token': token, 'project_id': this.$props.projectId}"
                multiple>
                <i class="el-icon-upload"></i>
                <div class="el-upload__text">Drag the file here, or <em>click to upload</em>.</div>
              </el-upload>
            </el-form-item>
          </el-form>

          <div>
            <div v-if="this.privileges['teach'] !== 1">
              <GroupInfo v-if="this.groupInfo['StudentGetsGroupInformationInProject'] == null"
                         v-bind:group-info="this.groupInfo"
                         v-bind:members-list="this.membersList"
                         v-bind:project-id="this.projectId"
                         v-bind:sid="this.sid"></GroupInfo>
              <h1 v-if="!(this.groupInfo['StudentGetsGroupInformationInProject'] == null)">You are not in any
                groups!</h1>
              <CreateOrJoinGroup
                v-if="!(this.groupInfo['StudentGetsGroupInformationInProject'] == null)"
                v-bind:sid="this.sid"
                v-bind:projectId="this.$props.projectId"></CreateOrJoinGroup>
            </div>

            <div v-if="this.privileges['teach'] === 1">
              <el-button @click="onClickEdit">{{ editLiteral }}</el-button>
            </div>


            <div>
              <el-form :inline="true" :model="target_user" class="querypersonalprofile">
                <h2>Wanna know somebody?</h2>
                <el-form-item label="">
                  <el-input v-model="target_user.sid" placeholder="Input his or her sid"></el-input>
                </el-form-item>
                <el-form-item>
                  <el-button type="primary" @click="onQueryPersonalProfile" align="right">Query</el-button>
                </el-form-item>
              </el-form>
            </div>

          </div>
        </el-card>
      </div>
    </el-col>
      <el-col :span="12" :offset="2">
        <div>
          <EventList v-bind:sid="this.$props.sid"
                     v-bind:courseId="this.$props.courseId"
                     v-bind:projectId="this.$props.projectId">
          </EventList>
        </div>

        <div v-if="showAd">
          <h1 style="font-family: Verdana, serif;">Advertisement</h1>
          <el-card v-if="advertisementData !== []">
            <el-collapse v-if="advertisementData !== []">
              <el-collapse-item v-for="item in advertisementData" :title=item.titlee :name=item.id>

                <div>{{ item.content }}</div>

              </el-collapse-item>
            </el-collapse>

            <div v-show="advertisementData === ''">There is no advertisement!</div>
          </el-card>

          <el-card v-if="this.privileges['teach'] !== 1">
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
      </el-col>
    </el-row>

    <div>
      <PersonalProfile v-if="this.displayControl.PersonalProfile" v-bind:sid="this.sid"
                       v-bind:personalprofile="this.personalProfile">
      </PersonalProfile>
      <el-button v-if="this.displayControl.PersonalProfile" @click="onClickBackToProjectDetail">Back to Projects
        Detail
      </el-button>
    </div>

    <div>
      <el-dialog title="Profile" :visible.sync="dialogPersonalProfileVisible">
        <el-form ref="form" label-position="left" label-width="80px">
          <el-form-item label="SID">
            <el-row>{{ this.personalProfile.sid }}</el-row>
          </el-form-item>

          <el-form-item label="Name">
            <el-row>{{ this.personalProfile['realname'] }}</el-row>
          </el-form-item>

          <el-form-item label="Gender">
            <el-row>{{ this.personalProfile.gender }}</el-row>
          </el-form-item>

          <el-form-item label="E-Mail">
            <el-row>{{ this.personalProfile.email }}</el-row>
          </el-form-item>

          <el-form-item label="Mobile">
            <el-row>{{ this.personalProfile.mobile }}</el-row>
          </el-form-item>

          <el-form-item label="Address">
            <el-row>{{ this.personalProfile.address }}</el-row>
          </el-form-item>

          <el-form-item label="Tag">
            <li v-for="item in this.tags['Data']">
              <el-badge :value="item.likes">
                <el-button @click="onClickLike(item.tag_id)">{{ item.tag_name }}</el-button>
              </el-badge>
            </li>
          </el-form-item>
        </el-form>
      </el-dialog>
    </div>

<el-row><div v-if="this.privileges['teach'] === 1">
    <Grouping v-bind:project_id="this.$props.projectId"></Grouping>
</div>
  <h1 style="font-family: Verdana, serif;">Authority Management</h1>
  <div>
    <AuthorityManage   v-bind:project_id="this.$props.projectId"></AuthorityManage>
  </div>
</el-row>


  </div>
</template>

<script>
import GroupInfo from './GroupInfo';
import CreateOrJoinGroup from './CreateOrJoinGroup';
import PersonalProfile from './PersonalProfile';
import EventList from './EventList';
import Grouping from './Grouping';
import AuthorityManage from './AuthorityManage';

export default {
  components: {Grouping, EventList, Event, CreateOrJoinGroup, GroupInfo, PersonalProfile, AuthorityManage},
  props: {
    sid: {
      type: String,
      required: true,
    },
    courseId: {
      type: Number,
      required: true,
    },
    projectId: {
      type: Number,
      required: true,
    },
  },
  data() {
    return {
      token: '',
      membersList: '',
      status: '',
      personalProfile: '',
      tags: '',
      displayControl: {
        projectDetail: true,
        PersonalProfile: false,
      },
      target_user: {
        sid: '',
      },
      dialogPersonalProfileVisible: false,
      advertisementData: [],
      eventList: [],
      advertisement_content: '',
      advertisement_title: '',
      privileges: {},
      edit: false,
      editLiteral: 'Edit',
      projectDetail: {},
      groupInfo: '',
      showAd: true,
      file_dict: {},
    };
  },
  created() {
    this.token = localStorage.getItem('Authorization');
    this.file_dict = {};
    this.$axios.post('/student_gets_single_project_information/', {'projectId': this.$props.projectId}).then(res => {
      this.projectDetail = res.data;
      for (const key in this.projectDetail['files']) {
        this.file_dict[key] = 'http://127.0.0.1:8000/download_file?token='
            + localStorage.getItem('Authorization')
            + '&file_id='
            + this.projectDetail['files'][key];
      }
      // for (let i = 0; i < this.projectDetail['files'].keys().length; i += 1) {
      //   const key = this.projectDetail['files'].keys()[i];
      //   this.file_dict[key] = 'http://127.0.0.1:8000?token='
      //       + localStorage.getItem('Authorization')
      //       + '&file_id='
      //       + this.projectDetail['files'][key];
      // }
      this.$axios.post('/student_gets_group_information_in_project/', {'project_id': this.$props.projectId}).
          then(res => {
            console.log(res)
            this.groupInfo = res.data;
            this.$axios.post('/get_privilege_list/', {'course_id': this.courseId}).then(res => {
              this.privileges = res.data['Data'];
              this.sid = this.$props.sid;
              this.pullAdvertisementData();

              if (this.groupInfo == null) {
                this.status = 'You are not in a group!';
              }
              else if (this.groupInfo['StudentGetsGroupInformationInProject'] === 'no group') {
                this.status = 'You are not in a group!';
              }
              else if (this.groupInfo['StudentGetsGroupInformationInProject'] == null) {
                for (let i = 0; i < this.groupInfo['members'].length; i++) {
                  this.membersList = this.membersList + this.groupInfo['members'][i] + '  ';
                }
              }
              else {
                this.status = 'unknown';
              }
            }).catch(err => {
              console.log('/get_privilege_list/', err);
            });
          }).
          catch(err => {
            console.log(err);
          });
    }).catch(err => {
      console.log(err);
    });
  },

  methods: {
    onClickEdit() {
      this.edit = !this.edit;
      if (this.edit) {
        this.editLiteral = 'Cancel';
      }
      else {
        this.editLiteral = 'Edit';
      }
    },
    controlDisplay(item) {
      for (const iter in this.displayControl) {
        this.displayControl[iter] = iter === item;
      }
    },
    onClickBackToProjectDetail() {
      this.controlDisplay('projectDetail');
    },
    onQueryPersonalProfile() {
      this.pullTagData();

      this.$axios.post('/show_other_personal_data/', {
        sid: this.sid,
        sid_target: this.target_user.sid,
      }).then(res => {
        if (res.data['ShowOtherPersonalDataCheck'] === 'ShowPersonalData success!') {
          this.personalProfile = res.data;
          // this.controlDisplay('PersonalProfile')
          this.dialogPersonalProfileVisible = true;
        }
        else {
          alert('No such user!');
        }
      }).catch(err => {
        this.tags = null;
        console.log(err);
      });
    },
    onClickLike(id) {
      this.$axios.post('/student_like_tag/', {
        sid: this.sid,
        tag_target: id,
      }).then(res => {

        if (res.data['StudentLikeTag'] === 'no like') {
          console.log('delike success');
        }
        else if (res.data['StudentLikeTag'] === 'like') {
          console.log('like success');
        }
        else {
          alert('failed');
        }
        this.pullTagData();
      }).catch(err => {
        console.log(err);
      });
    },
    pullTagData() {
      this.$axios.post('/student_gets_all_tags/', {
        sid: this.sid,
        sid_target: this.target_user.sid,
      }).then(res => {
        this.tags = res.data;
        console.log('now this.tags', this.tags);
      }).catch(err => {
        console.log(err);
      });
    },
    pullAdvertisementData() {
      this.$axios.post('/student_gets_all_ad/', {
        'project_id': this.$props.projectId,
      }).then(res => {
        if (res.data['StudentGetAllAd'] === 'success') {
          this.advertisementData = res.data['Data'];
        }
        else {
          this.advertisementData = '';
        }
      }).catch(err => {
        console.log(err);
      });
    },
    onClickUploadAdvertisement() {
      if (this.groupInfo['StudentGetsGroupInformationInProject'] == null) {
        this.$axios.post('/student_publish_request/', {
          project_id: this.projectDetail.project_id,
          content: this.advertisement_content,
          title: this.advertisement_title,
          group_id: this.groupInfo.group_id,
        }).then(res => {
          console.log(res);
          this.pullAdvertisementData();
        }).catch(err => {
          console.log(err);
        });
      }
      else {
        this.$axios.post('/student_publish_apply/', {
          project_id: this.$props.projectDetail.project_id,
          content: this.advertisement_content,
          title: this.advertisement_title,
        }).then(res => {
          console.log('up ad', res.data);
          this.pullAdvertisementData();
        }).catch(err => {
          console.log(err);
        });
      }
    },
  },
  name: 'ProjectDetail',
};
</script>

<style scoped>
.project_detail {
  /*background-color: #F7F8F8;*/
}

.el-card {
  font-family: Verdana, serif;
  background-color: #F7F8F8;
  border-color: whitesmoke;
  align-content: center;
  /*text-align: center;*/
  line-height: 40px;
}

</style>

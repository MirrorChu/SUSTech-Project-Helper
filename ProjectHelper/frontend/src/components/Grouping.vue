<template>
  <div>
    <div id="single">
      <li v-for="item in this.singleData">{{ item.sid + ' ' + item.realname }}&nbsp</li>
    </div>

    <div>
      <el-table
          :data="groupData"
          stripe
          style="width: 100%">
        <el-table-column
            prop="group_id"
            label="GROUP ID">
        </el-table-column>
        <el-table-column
            prop="group_name"
            label="GROUP NAME">
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

      <el-button @click="semirandomgrouping"> Semi-random Grouping</el-button>
      <el-button @click="showCreateGroupDialog"> Create New Group for Students</el-button>
    </div>

    <div>
      <el-dialog title="Group Data" :visible.sync="dialogGroupDataVisible">
        <el-form ref="form">
          <el-form-item label="GROUP ID">
            <el-row>{{ groupInformation.group_id }}</el-row>
          </el-form-item>

          <el-form-item label="Captain">
            {{ groupInformation.captain_name }}
          </el-form-item>

          <el-form-item label="Member">
            <el-row v-for="(stu_sid,index) in groupInformation['member_sid']">
              {{ stu_sid + ' ' + groupInformation['member_name'][index] }}
              <el-button @click="onClickKick(stu_sid, groupInformation.group_id)">Kick</el-button>
            </el-row>
          </el-form-item>

          <!--          <el-form-item>-->
          <!--            <el-input v-model="sid_invite" placeholder="SID to Invite"></el-input>-->
          <!--            <el-button @click="onClickInvite(groupInformation.group_id)">Invite</el-button>-->
          <!--          </el-form-item>-->
        </el-form>

        <el-select v-model="stu_invite" multiple placeholder="">
          <el-option
              v-for="item in this.singleData"
              :key="item.sid"
              :label="item.realname"
              :value="item.sid">
            <span>{{ item.realname }}&nbsp{{ item.sid }}</span>
          </el-option>
        </el-select>
        <el-button @click="test(groupInformation.group_id)">Invite</el-button>
      </el-dialog>
    </div>

    <div>
      <el-dialog title="Create New Group for Studnets" :visible.sync="dialogCreateGroupVisible" @close='closeDialog'>
        <el-form ref="form">
          <el-form-item label="GROUP NAME">
            <el-input v-model="createGroupName" placeholder="Group Name" clearable></el-input>
          </el-form-item>

          <el-form-item label="Captain">
            <el-select v-model="captain_sid" clearable placeholder="" @change="captainselect">
              <el-option
                  v-for="item in this.singleDataCopy1"
                  :key="item.sid"
                  :label="item.realname"
                  :value="item.sid">
                <span>{{ item.realname }}&nbsp{{ item.sid }}</span>
              </el-option>
            </el-select>
          </el-form-item>

          <el-form-item label="Member">
            <el-select v-model="member_select" multiple placeholder="" @change="memberselect">
              <el-option
                  v-for="item in this.singleDataCopy2"
                  :key="item.sid"
                  :label="item.realname"
                  :value="item.sid">
                <span>{{ item.realname }}&nbsp{{ item.sid }}</span>
              </el-option>
            </el-select>
          </el-form-item>
        </el-form>

        <el-button @click="onClickCreateNewGroup()">Create</el-button>

      </el-dialog>
    </div>

  </div>
</template>

<script>
export default {
  name: 'Grouping',
  props: {
    project_id: {
      required: true,
    },
  },
  data() {
    return {
      groupData: [],
      dialogGroupDataVisible: false,
      dialogCreateGroupVisible: false,
      groupInformation: '',
      sid_invite: '',
      singleData: '',
      singleDataCopy1: '',
      singleDataCopy2: '',
      stu_invite: '',
      createGroupName: '',
      captain_sid: '',
      member_select: [],
    };
  },
  created() {
    this.pullGroupingData();
  },
  methods: {
    test(group_id) {
      for (const index in this.stu_invite) {
        this.$axios.post('/teacher_add_member/', {
          group_id: group_id,
          sid_invite: this.stu_invite[index],
        }).then(res => {
          console.log(res.data);
        }).catch(err => {
          console.log(err);
        });
      }
    },
    pullSingleData() {
      this.$axios.post('/teacher_get_single_in_project/', {
        project_id: this.$props.project_id,
      }).then(res => {
        console.log('pullSingleData', res.data);
        if (res.data['TeacherGetSingleInProject'] === 'success') {
          this.singleData = res.data['Data'];
          this.singleDataCopy1 = this.singleData.slice(0);
          this.singleDataCopy2 = this.singleData.slice(0);
        }
      }).catch(err => {
        console.log(err);
      });
    },
    pullGroupingData() {
      this.$axios.post('/teacher_get_situation_in_project/', {
        project_id: this.$props.project_id,
      }).then(res => {
        console.log('pullGroupingData', res.data);
        if (res.data['TeacherGetSituationInProject'] === 'success') {
          this.groupData = res.data['Data'];
          console.log('groupData', res.data['Data']);
        }
        this.pullSingleData();
      }).catch(err => {
        console.log(err);
      });
    },
    onClickShowGroupDetail(row) {
      this.dialogGroupDataVisible = true;
      this.groupInformation = row;
    },
    // onClickInvite(group_id)
    // {
    //   this.$axios.post('/', {
    //     group_id: group_id,
    //     sid_invite: this.sid_invite,
    //   }).then(res => {
    //     console.log(res.data)
    //   }).catch(err => {
    //     console.log(err)
    //   })
    // },
    onClickKick(sid, group_id) {
      this.$axios.post('/teacher_kick_member/', {
        group_id: group_id,
        sid_kick: sid,
      }).then(res => {
        console.log(res.data);
        this.pullSingleData();
      }).catch(err => {
        console.log(err);
      });
    },
    semirandomgrouping() {
      this.$axios.post('/semi_random/', {'project_id': this.$props.project_id}).then(res => {
        console.log(res)
      }).catch(err => {
        console.log(err)
      })
    },
    onClickCreateNewGroup() {
      this.$axios.post('/teacher_creates_group/', {
        project_id: this.$props.project_id,
        group_name: this.createGroupName,
        captain_sid: this.captain_sid,
        sid_list: this.member_select,
      }).then(res => {
        console.log('CreateNewGroup', res.data);
        this.pullGroupingData();
        this.createGroupName = '';
        this.captain_sid = '';
        this.member_select = [];
        this.dialogCreateGroupVisible = false;
      }).catch(err => {
        console.log(err);
      });
    },
    captainselect() {
      this.singleDataCopy2 = this.singleData.slice(0);
      let j = -1;
      for (let i = 0; i < this.singleDataCopy2.length; i++) {
        if (this.singleDataCopy2[i].sid === this.captain_sid) {
          j = i;
          break;
        }
      }
      if (j !== -1)
        this.singleDataCopy2.splice(j, 1);
    },
    showCreateGroupDialog() {
      this.dialogCreateGroupVisible = true;
    },
    memberselect() {
      this.singleDataCopy1 = this.singleData.slice(0);
      for (let k = 0; k < this.member_select.length; k++) {
        let j = -1;
        for (let i = 0; i < this.singleDataCopy1.length; i++) {
          if (this.singleDataCopy1[i].sid === this.member_select[k]) {
            j = i;
            break;
          }
        }
        if (j !== -1)
          this.singleDataCopy1.splice(j, 1);
      }
    },
    closeDialog() {
      this.pullSingleData();
    },
  },
};
</script>

<style scoped>
#single {
  display: flex;
  justify-content: flex-start;
}
</style>

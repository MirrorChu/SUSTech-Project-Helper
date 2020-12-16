<template>
  <div>
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

      <el-button @click="semirandomgrouping"> Semi-random Grouping </el-button>
    </div>

    <div>
      <el-dialog title="Group Data" :visible.sync="dialogGroupDataVisible">
        <el-form ref="form">
          <el-form-item label="GROUP ID">
            <el-row>{{ groupInformation.group_id }}</el-row>
          </el-form-item>

          <el-form-item label="Captain">
            {{  groupInformation.captain_name  }}
          </el-form-item>

          <el-form-item label="Member">
            <el-row v-for="(stu_sid,index) in groupInformation['member_sid']">
                {{ stu_sid+' '+ groupInformation['member_name'][index] }}
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
          <span>{{  item.realname  }}&nbsp{{  item.sid  }}</span>
        </el-option>
      </el-select>
        <el-button @click="test(stu_invite, groupInformation.group_id)">Invite</el-button>
      </el-dialog>
    </div>

  </div>
</template>

<script>
  export default {
    name: "Grouping",
    props: {
      project_id: {
        required: true,
      },
    },
    data() {
      return {
        groupData: [],
        dialogGroupDataVisible: false,
        groupInformation: '',
        sid_invite: '',
        singleData: '',
        stu_invite: '',
      }
    },
    created() {
      this.pullGroupingData()
    },
    methods: {
      test(sth, group_id)
      {
        console.log(sth)
        console.log(typeof sth)
        for (const item in sth)
        {
          this.$axios.post('/teacher_add_member/', {
            group_id: group_id,
            sid_invite: sth[item],
          }).then(res => {
            console.log(res.data)
          }).catch(err => {
            console.log(err)
          })
        }
      },
      pullSingleData ()
      {
        this.$axios.post('/teacher_get_single_in_project/', {
          project_id: this.$props.project_id,
        }).then(res => {
          console.log('pullSingleData', res.data)
          if (res.data['TeacherGetSingleInProject'] === 'success')
          {
            this.singleData = res.data['Data']
          }
        }).catch(err => {
          console.log(err)
        })
      },
      pullGroupingData ()
      {
        this.$axios.post('/teacher_get_situation_in_project/', {
          project_id: this.$props.project_id,
        }).then(res => {
          console.log('pullGroupingData', res.data)
          if (res.data['TeacherGetSituationInProject'] === 'success')
          {
            this.groupData = res.data['Data']
            console.log('groupData', res.data['Data'])
          }
          this.pullSingleData()
        }).catch(err => {
          console.log(err)
        })
      },
      onClickShowGroupDetail(row)
      {
        this.dialogGroupDataVisible = true
        this.groupInformation = row
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
      onClickKick(sid, group_id)
      {
        this.$axios.post('/teacher_kick_member/', {
          group_id: group_id,
          sid_kick: sid,
        }).then(res => {
          console.log(res.data)
          this.pullSingleData()
        }).catch(err => {
          console.log(err)
        })
      },
      semirandomgrouping()
      {
        // this.$axios.post('//', {
        //   project_id: this.$props.project_id,
        // }).then(res => {
        //   console.log(res.data)
        //   this.pullGroupingData()
        //   this.pullSingleData()
        // }).catch(err => {
        //   console.log(err)
        // })
      },
    },
  }
</script>

<style scoped>

</style>

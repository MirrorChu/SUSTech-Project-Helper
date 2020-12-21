<template>
  <div>
    <div>
      <el-table
        :data="this.AuthorityData"
        style="width: 100%">
  <!--      <el-table-column type="expand">-->
  <!--        <template slot-scope="props">-->
  <!--          <el-form label-position="left" inline class="demo-table-expand">-->
  <!--            <el-form-item v-for="authority in authoritylist" label={{authority}}>-->
  <!--              <span>{{props.row[authority]===1?'√':'×'}}</span>-->
  <!--            </el-form-item>-->
  <!--          </el-form>-->
  <!--        </template>-->
  <!--      </el-table-column>-->
        <span>No Authority Data</span>
        <el-table-column
          label="SID"
          prop="sid">
        </el-table-column>

        <el-table-column
          label="NAME"
          prop="name">
        </el-table-column>

        <el-table-column label="Project Grade" >
          <template slot-scope="scope">
  <!--          <span v-if="!scope.row.edit & scope.row.eventGrade === '1'" class="el-icon-success"></span>-->
  <!--          <span v-if="!scope.row.edit & scope.row.eventGrade === '0'" class="el-icon-circle-close"></span>-->
            <el-switch
              :disabled="!scope.row.edit"
              v-model="scope.row.projectGrade"
              active-color="#13ce66"
              inactive-color="#ff4949"
              active-value="1"
              inactive-value="0">
            </el-switch>
          </template>
        </el-table-column>

        <el-table-column label="Teach" >
          <template slot-scope="scope">
            <el-switch
              :disabled="!scope.row.edit"
              v-model="scope.row.teach"
              active-color="#13ce66"
              inactive-color="#ff4949"
              active-value="1"
              inactive-value="0">
            </el-switch>
          </template>
        </el-table-column>
        <el-table-column label="Project Edit" >
          <template slot-scope="scope">
            <el-switch
              :disabled="!scope.row.edit"
              v-model="scope.row.projectEdit"
              active-color="#13ce66"
              inactive-color="#ff4949"
              active-value="1"
              inactive-value="0">
            </el-switch>
          </template>
        </el-table-column>
        <el-table-column label="Event Edit" >
          <template slot-scope="scope">
            <el-switch
              :disabled="!scope.row.edit"
              v-model="scope.row.eventEdit"
              active-color="#13ce66"
              inactive-color="#ff4949"
              active-value="1"
              inactive-value="0">
            </el-switch>
          </template>
        </el-table-column>
        <el-table-column label="=Event Visible" >
          <template slot-scope="scope">
            <el-switch
              :disabled="!scope.row.edit"
              v-model="scope.row.eventVisible"
              active-color="#13ce66"
              inactive-color="#ff4949"
              active-value="1"
              inactive-value="0">
            </el-switch>
          </template>
        </el-table-column>
        <el-table-column label="Event Grade" >
          <template slot-scope="scope">
            <el-switch
              :disabled="!scope.row.edit"
              v-model="scope.row.eventGrade"
              active-color="#13ce66"
              inactive-color="#ff4949"
              active-value="1"
              inactive-value="0">
            </el-switch>
          </template>
        </el-table-column>
        <el-table-column label="Event Edit" >
          <template slot-scope="scope">
            <el-switch
              :disabled="!scope.row.edit"
              v-model="scope.row.eventEdit"
              active-color="#13ce66"
              inactive-color="#ff4949"
              active-value="1"
              inactive-value="0">
            </el-switch>
          </template>
        </el-table-column>
        <el-table-column label="Group" >
          <template slot-scope="scope">
            <el-switch
              :disabled="!scope.row.edit"
              v-model="scope.row.group"
              active-color="#13ce66"
              inactive-color="#ff4949"
              active-value="1"
              inactive-value="0">
            </el-switch>
          </template>
        </el-table-column>
        <el-table-column label="Authority Edit" >
          <template slot-scope="scope">
            <el-switch
              :disabled="!scope.row.edit"
              v-model="scope.row.authEdit"
              active-color="#13ce66"
              inactive-color="#ff4949"
              active-value="1"
              inactive-value="0">
            </el-switch>
          </template>
        </el-table-column>
        <el-table-column label="Group Valid" >
          <template slot-scope="scope">
            <el-switch
              :disabled="!scope.row.edit"
              v-model="scope.row.groupValid"
              active-color="#13ce66"
              inactive-color="#ff4949"
              active-value="1"
              inactive-value="0">
            </el-switch>
          </template>
        </el-table-column>
        <el-table-column label="Tag Edit" >
          <template slot-scope="scope">
            <el-switch
              :disabled="!scope.row.edit"
              v-model="scope.row.tagEdit"
              active-color="#13ce66"
              inactive-color="#ff4949"
              active-value="1"
              inactive-value="0">
            </el-switch>
          </template>
        </el-table-column>


        <el-table-column>
          <template slot-scope="scope">
            <el-button v-if="!scope.row.edit" @click="onClickEditAuthority(scope.$index)">Edit</el-button>
            <el-button v-else @click="onClickConfirmEdit(scope.$index)">Confirm Edit</el-button>
          </template>
        </el-table-column>

      </el-table>
    </div>

<!--  <div>-->
<!--    <el-dialog title="Edit Authority" :visible.sync="dialogEditAuthorityVisible">-->
<!--      <el-form ref="form" label-position="left" label-width="80px">-->
<!--        <el-form-item label="SID">-->
<!--          <el-row>{{ target_editauthority.sid }}</el-row>-->
<!--        </el-form-item>-->

<!--        <el-form-item label="Name">-->
<!--          <el-row>{{ target_editauthority.name }}</el-row>-->
<!--        </el-form-item>-->

<!--        <div v-for="aa in authoritylist">-->
<!--          <el-form-item label=aa>-->
<!--            {{this.target_editauthority[aa]===1?'√':'×'}}-->
<!--          </el-form-item>-->
<!--        </div>-->
<!--      </el-form>-->
<!--    </el-dialog>-->
<!--  </div>-->
  </div>
</template>

<script>
    export default {
        name: "AuthorityManage",
      data() {
        return {
          AuthorityData: [],
          edit_authority: false,
          target_editauthority: '',
          dialogEditAuthorityVisible: false,
          edit: [],
        }
      },
      props: {
        project_id: {
          // type: String,
          required: true,
        },
      },
      created() {
          this.pullAuthorityData()
      },
      methods: {
        pullAuthorityData ()
        {
          this.edit = []
          this.$axios.post('/get_all_privilege_list/', {
            project_id: this.$props.project_id,
          }).then(res => {
            console.log('AuthorityData',res.data)
            if (res.data.GetAllPrivilegeListCheck === 'success')
            {
              this.AuthorityData = res.data.Data
            }
            else if (res.data.GetAllPrivilegeListCheck === 'you have no auth')
            {
              alert("You don't have authority to edit")
            }
          }).catch(err => {
            console.log(err)
          })
        },
        onClickEditAuthority (index)
        {
          this.AuthorityData[index].edit = true
        },
        onClickConfirmEdit(index)
        {
          let list = ['teach', 'projectGrade',
          'projectEdit', 'eventValid', 'eventVisible',
          'eventGrade', 'eventEdit', 'group', 'authEdit',
          'groupValid', 'tagEdit']
          let dict = {}
          for (let i = 0; i < 11; i++)
          {
            let t1 = list[i]
            dict[t1] = this.AuthorityData[index][t1]
          }
          this.$axios.post('/change_privilege/', {
            project_id: this.project_id,
            t_sid: this.AuthorityData[index]['sid'],
            dict: dict,
          }).then(res => {
            console.log(res.data)
            this.AuthorityData[index].edit = false
          }).catch(err => {
            console.log(err)
            this.AuthorityData[index].edit = false
          })
        },
      }
    }
</script>

<style scoped>
  .el-icon-circle-close{
    font-size: 20px;
  }
  .el-icon-success{
    font-size: 20px;
  }
</style>

<template>

    <el-table
      :data="AuthorityData"
      style="width: 100%">
      <el-table-column type="expand">
        <template slot-scope="props">
          <el-form label-position="left" inline class="demo-table-expand">
            <el-form-item v-for="authority in authoritylist" label={{authority}}>
              <span>{{props.row[authority]===1?'√':'×'}}</span>
            </el-form-item>
          </el-form>
        </template>
      </el-table-column>
      <el-table-column
        label="SID"
        prop="sid">
      </el-table-column>
      <el-table-column
        label="NAME"
        prop="name">
      </el-table-column>
      <el-table-column
        label="ACTION">
        <template slot-scope="scope">
          <el-button @click="onClickEditAuthority(scope.row)">Edit</el-button>
        </template>
      </el-table-column>
    </el-table>

  <div>
    <el-dialog title="Edit Authority" :visible.sync="dialogEditAuthorityVisible">
      <el-form ref="form" label-position="left" label-width="80px">
        <el-form-item label="SID">
          <el-row>{{ target_editauthority.sid }}</el-row>
        </el-form-item>

        <el-form-item label="Name">
          <el-row>{{ target_editauthority.name }}</el-row>
        </el-form-item>

        <div v-for="aa in authoritylist">
          <el-form-item label=aa>
            {{this.target_editauthority[aa]===1?'√':'×'}}
          </el-form-item>
        </div>
      </el-form>
    </el-dialog>
  </div>

</template>

<script>
    export default {
        name: "AuthorityManage",
      data() {
        return {
          AuthorityData: '',
          authoritylist: ['', '', ''],
          edit_authority: false,
          target_editauthority: '',
          dialogEditAuthorityVisible: false,
        }
      },
      created() {
          this.pullAuthorityData()
      },
      methods: {
        pullAuthorityData ()
        {
          this.$axios.post('/', {
            project_id: this.project_id,
          }).then(res => {
            console.log(res.data)
            this.AuthorityData = res.data
          }).catch(err => {
            console.log(err)
          })
        },
        onClickEditAuthority (information)
        {
          this.edit_authority = true
          this.dialogEditAuthorityVisible = true
          this.target_editauthority = information
        },
        onClickConfirmEditAuthority ()
        {
          this.$axios.post('/', {
            project_id: this.project_id,
            // sid_target: ,
          }).then(res => {
            console.log(res.data)
          }).catch(err => {
            console.log(err)
          })
          this.edit_authority = false
          this.dialogEditAuthorityVisible = false
        },
      }
    }
</script>

<style scoped>

</style>

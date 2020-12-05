<template>
  <div>
<!--    <el-image style="width: 200px; height: 200px" :src="this.avatar" fit="cover"></el-image>-->

    <el-form ref="form" label-position="left" label-width="80px">
      <el-form-item label="SID">
      <el-row>{{ this.$props.personalprofile.sid }}</el-row>
      </el-form-item>

      <el-form-item label="Name">
      <el-row>{{ this.$props.personalprofile.realname }}</el-row>
      </el-form-item>

      <el-form-item label="Gender">
      <el-row>{{ this.$props.personalprofile.gender }}</el-row>
      </el-form-item>

      <el-form-item label="E-Mail">
      <el-row>{{ this.$props.personalprofile.email }}</el-row>
      </el-form-item>

      <el-form-item label="Mobile">
      <el-row>{{ this.$props.personalprofile.mobile }}</el-row>
      </el-form-item>

      <el-form-item label="Address">
      <el-row>{{ this.$props.personalprofile.address }}</el-row>
      </el-form-item>

      <el-form-item>
        <el-row>
          <el-table
            :data="tableData"
            style="width: 100%">
            <el-table-column
              prop="tag_id"
              label="Tag ID"
              width="180">
            </el-table-column>
            <el-table-column
              prop="type"
              label="Tag Type"
              width="180">
            </el-table-column>
            <el-table-column
              prop="tag_name"
              label="Tag">
            </el-table-column>
            <el-table-column
              prop="likes"
              label="Like">
            </el-table-column>
            <el-table-column
              prop="button">
              <template slot-scope="scope">
<!--                <el-badge :value="scope.row.likes" class="item">-->
                  <el-button @click="onClickLike(scope.$index)">Like</el-button>
<!--                </el-badge>-->
              </template>
            </el-table-column>
          </el-table>
        </el-row>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
    export default {
      name: "PersonalProfile",
      props: {
        sid: {
          type: String,
          required: true,
        },
        pswd: {
          type: String,
          required: true,
        },
        personalprofile: {
          required: true,
        },
        tags: {
          required: true,
        },
      },
      data() {
        return {
          tableData: [],
        }
      },
      created() {
        if (this.$props.tags.StudentGetsAllTags === 'success')
        {
          this.tableData = this.$props.tags.Data
        }
      },
      methods: {
        onClickLike(index)
        {

        },
      }
    }
</script>

<style scoped>
  .avatar-uploader .el-upload {
    border: 1px dashed #d9d9d9;
    border-radius: 6px;
    cursor: pointer;
    position: relative;
    overflow: hidden;
  }

  .avatar-uploader .el-upload:hover {
    border-color: #409EFF;
  }
</style>

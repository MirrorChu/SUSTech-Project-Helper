<template>
  <div>
    <h1>Profile</h1>

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

      <el-form-item label="Tag">
        <li v-for="item in this.tags.Data">
          <el-badge :value="item.likes">
            <button @click="onClickLike(item.tag_id)">{{ item.tag_name }}</button>
          </el-badge>
        </li>
      </el-form-item>

<!--      <el-form-item>-->
<!--        <el-row>-->
<!--          <el-table-->
<!--            :data="this.tags.Data"-->
<!--            style="width: 100%">-->
<!--            <el-table-column-->
<!--              prop="tag_id"-->
<!--              label="Tag ID"-->
<!--              width="180">-->
<!--            </el-table-column>-->
<!--            <el-table-column-->
<!--              prop="type"-->
<!--              label="Tag Type"-->
<!--              width="180">-->
<!--            </el-table-column>-->
<!--            <el-table-column-->
<!--              prop="tag_name"-->
<!--              label="Tag">-->
<!--            </el-table-column>-->
<!--            <el-table-column-->
<!--              prop="likes"-->
<!--              label="Like">-->
<!--            </el-table-column>-->
<!--            <el-table-column-->
<!--              prop="button">-->
<!--              <template slot-scope="scope">-->
<!--&lt;!&ndash;                <el-badge :value="scope.row.likes" class="item">&ndash;&gt;-->
<!--                  <el-button @click="onClickLike(scope.$index)">Like</el-button>-->
<!--&lt;!&ndash;                </el-badge>&ndash;&gt;-->
<!--              </template>-->
<!--            </el-table-column>-->
<!--          </el-table>-->
<!--        </el-row>-->
<!--      </el-form-item>-->
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
      },
      data() {
        return {
          tableData: [],
          tagData: [],
          tags: '',
        }
      },

      created() {
        console.log("created")
      },
      mounted() {
        console.log("mounted")
        this.sid = this.$props.sid
        this.pswd = this.$props.pswd
        this.pulltagData()
      },
      methods: {
        onClickLike(id)
        {
          console.log('hello')
          console.log(this.sid, this.pswd, id)
          this.$axios.post('/student_like_tag/', {
            sid: this.sid,
            pswd: this.pswd,
            tag_target: id,
          }).then(res => {
            this.pulltagData()
            if (res.data.StudentLikeTag === "no like")
            {
              console.log("delike success")
            }
            else if (res.data.StudentLikeTag === "like")
            {
              console.log("like success")
            }
            else
            {
              alert("failed")
            }
          }).catch(err => {
            console.log(err)
          })
        },
        pulltagData()
        {
          this.$axios.post('/student_gets_all_tags/', {
            sid: this.sid,
            pswd: this.pswd,
            sid_target: this.$props.personalprofile.sid,
          }).then(res => {
            this.tags = res.data
            console.log('now this.tags',this.tags)
          }).catch(err => {
            console.log(err)
          })
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

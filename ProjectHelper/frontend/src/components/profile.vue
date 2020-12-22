<!--TODO After refresh, everything is gone.-->
<template>
  <div id="profile">
    <el-card>
      <h1>Personal Profile</h1>
      <el-divider></el-divider>
    <el-col :span="16">
    <el-form ref="form" label-position="left" label-width="80px">
      <el-form-item label="SID">
        <el-input v-model="this.sid" v-if="false" :placeholder="this.sid" clearable>
        </el-input>

        <el-row>
          {{ this.sid }}
        </el-row>

      </el-form-item>

      <el-form-item label="NAME">
        <el-input v-model="this.name" v-if="false" :placeholder="this.name" clearable>
        </el-input>
        <el-row>
          {{ this.name }}
        </el-row>
      </el-form-item>

      <el-form-item label="GENDER">
        <el-input v-model="this.name" v-if="false" :placeholder="this.name" clearable>
        </el-input>
        <el-row>
          {{ this.gender }}
        </el-row>
      </el-form-item>

      <el-form-item label="EMAIL">
        <el-input v-model="email" v-if="this.edit" :placeholder="this.email" clearable>
        </el-input>

        <el-row v-if="!this.edit">
          {{ this.email }}
        </el-row>
      </el-form-item>


      <el-form-item label="MOBILE">
        <el-input v-model="mobile" v-if="this.edit" :placeholder="mobile" clearable>
        </el-input>

        <el-row v-if="!this.edit">
          {{ this.mobile }}
        </el-row>
      </el-form-item>

      <el-form-item label="ADDR">
        <el-input v-model="address" v-if="this.edit" :placeholder="address" clearable>
        </el-input>

        <el-row v-if="!this.edit">
          {{ this.address }}
        </el-row>
      </el-form-item>

      <el-form-item label="Tag">
        <div v-if="!this.edit">
          <span v-for="item in this.tags['Data']">
            <el-badge :value="item.likes">
              <el-button @click="onClickLike(item.tag_id)">{{ item.tag_name }}</el-button>
            </el-badge>
            &nbsp
          </span>
        </div>

        <div v-if="this.edit">
          <b>Have Selected:</b>
          <span v-for="item in this.tags['Data']">
            <el-button @click="onClickDeleteTag(item.tag_id, item.tag_name, item.IDofTag)">{{ item.tag_name }}</el-button>
            &nbsp
          </span>
          <br>
          <b>To be Selected:</b>
          <span v-for="item in addtags['Data']">
            <el-button @click="onClickAddTag(item.tag_id, item.tag_name)">{{ item.tag_name }}</el-button>
            &nbsp
          </span>
        </div>
      </el-form-item>

      <el-button v-if="!this.edit" @click="onEditClicked()">EDIT</el-button>
      <el-button v-if="this.edit" @click="onConfirmEditClicked()">CONFIRM EDIT</el-button>

    </el-form>

    <div>
      <el-divider></el-divider>
      <h3>Add Tag Library</h3>
      <el-input v-model="addingtag"></el-input>
      <el-button @click="onClickAddTagLibrary">ADD</el-button>
    </div>
    </el-col>

      <el-col :span="8">
        <el-image v-if="!this.edit" style="width: 200px; height: 200px"
                  :src="this.avatarUrl" :datafld="avatarUrl" fit="cover"></el-image>
        <el-upload v-if="this.edit"
                   class="avatar-uploader"
                   action="/api/change_head_image/"
                   :data="{sid: this.sid}"
                   :auto-upload="true"
                   :show-file-list="false"
                   :on-success="handleAvatarSuccess"
                   :before-upload="beforeAvatarUpload">
          <el-image v-if="imageUrl" :src="imageUrl" class="avatar" alt="avatar"></el-image>
          <i v-else class="el-icon-plus avatar-uploader-icon"></i>
        </el-upload>
      </el-col>
    </el-card>
  </div>
</template>

<script>


export default {
  name: 'profile',
  props: {},
  data () {
    return {
      sid: '',
      name: '',
      email: '',
      gender: '',
      mobile: '',
      address: '',
      imageUrl: '',
      dialogImageUrl: '',
      dialogVisible: '',
      edit: false,
      tags: '',
      addtags: '',
      avatarUrl: '',
      addingtag: '',
    }
  },
  created () {
    this.pullPersonalData()
  },
  methods: {
    pullPersonalData () {
      //TODO: Get avatar from backend.
      this.$axios.post('/show_personal_data/', {}).then(res => {
        if (res.data['attempt'] === 'failure') {
          this.$router.push('/login')
        } else {
          const token = localStorage.getItem('Authorization')
          this.token = token
          this.avatarUrl = 'http://127.0.0.1:8000/show_head_image?' + 'token=' + this.token  // request avatar
          const data = res.data
          this.sid = data['sid']
          this.name = data['realName']
          this.gender = data['gender']
          this.email = data['email']
          this.mobile = data['mobile']
          this.address = data['address']
          console.log('after pull info', this.sid)
          this.pulltagData()
        }
      }).catch(err => {
        console.log('err', err)
      })
    },
    //TODO: Add regex check for fields.
    onConfirmEditClicked () {
      this.$axios.post('/change_personal_data/', {
        sid: this.sid,
        email: this.email,
        gender: this.gender,
        mobile: this.mobile,
        address: this.address,
      }).then(res => {
        const data = res.data
        if (data['attempt'] === 'offline') {
          this.$router.push('/')
        } else if (data['attempt'] === 'failure') {
          alert('Failed to edit profile!')
        }
        this.pullPersonalData()
        this.edit = false
      }).catch(err => {
        console.log('err', err)
      })
    },
    onEditClicked () {
      this.edit = true
    },
    onClickNewPassword () {
      this.$router.push({ name: 'homepage_profile_newpassword', sid: this.$route.params.sid }).then(res => {
        console.log(res)
      }).catch(err => {
        console.log(err)
      })
    },
    handleAvatarSuccess (res, file) {
      console.log('raw', file.raw)
      console.log('raws', file.raws)
      console.log('success')
      console.log(res)
      console.log(file)
      // this.imageUrl = URL.createObjectURL(file.raw)
      this.imageUrl = ''
    },
    beforeAvatarUpload (file) {
      const isJPG = file.type === 'image/jpeg'
      const isLt2M = file.size / 1024 / 1024 < 2
      if (!isJPG) {
        this.$message.error('上传头像图片只能是 JPG 格式!')
      }
      if (!isLt2M) {
        this.$message.error('上传头像图片大小不能超过 2MB!')
      }
      return isJPG && isLt2M
    },
    pulltagData () {
      this.$axios.post('/student_gets_all_tags/', {
        sid: this.sid,
        sid_target: this.sid,
      }).then(res => {
        this.tags = res.data
        this.pulladdtagData()
      }).catch(err => {
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
    onClickDeleteTag (id, name, id2) {
      this.$axios.post('/unshow_tag/', {
        sid: this.sid,
        tag_target: id,
      }).then(res => {
        console.log(res.data)
        if (res.data.UnshowTag === 'success') {
          let len = this.tags.Data.length
          let j = 0
          for (let i = 0; i < len; i++) {
            if (this.tags.Data[i].tag_id === id) {
              j = i
              break
            }
          }
          this.tags.Data.splice(j, 1)
          this.addtags['Data'].push({ 'tag_id': id2, 'tag_name': name})
        }
      }).catch(err => {
        console.log(err)
      })
    },
    onClickAddTag (id, name) {
      let len = this.tags.Data.length
      if (len >= 10)
      {
        alert('You can not add tag anymore! or delete some first')
      }
      else
      {
        this.$axios.post('/add_tag/', {
          sid: this.sid,
          tag_target: id,
        }).then(res => {
          console.log('addtag', res.data)
          if (res.data.AddTag === 'success') {
            console.log(this.tags['Data'])
            let len = this.addtags.Data.length
            let j = 0
            for (let i = 0; i < len; i++) {
              if (this.addtags.Data[i].tag_id === id) {
                j = i
                break
              }
            }
            this.addtags.Data.splice(j, 1)
            this.tags['Data'].push({ 'tag_id': res.data.UserTagID, 'tag_name': name, 'like': res.data.like, 'likes': res.data.likes})
          }
        }).catch(err => {
          console.log(err)
        })
      }

    },
    pulladdtagData () {
      this.$axios.post('/student_gets_all_tags_can_add/', {
        sid: this.sid,
      }).then(res => {
        this.addtags = res.data
      }).catch(err => {
        console.log('err', err)
      })
    },
    onClickAddTagLibrary()
    {
      this.$axios.post('/add_new_tag/', {
        tag_name: this.addingtag,
      }).then(res => {
        console.log(res.data)
        this.addingtag = ''
      }).catch(err => {
        console.log('err', err)
      })
    }
  },
}
</script>

<style>
.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 200px;
  height: 200px;
  line-height: 200px;
  text-align: center;
}

.avatar {
  width: 178px;
  height: 178px;
  display: block;
}
</style>

<style scoped>
.el-card{
  font-family: Verdana, serif;
  background-color: #F7F8F8;
  border-color: whitesmoke;
  align-content: center;
  text-align: center;
  line-height: 50px;
}
</style>

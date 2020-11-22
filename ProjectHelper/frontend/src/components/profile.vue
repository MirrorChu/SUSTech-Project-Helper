<!--TODO After refresh, everything is gone.-->
<template>
  <div id="profile">
    <!--    <el-link href="https://127.0.0.1:8000/test/" target="_blank">默认链接</el-link>-->
    <!--    <el-button @click="testFileDownload">test file download</el-button>-->
    <!--    <el-avatar :size="60" :src="this.avatar"></el-avatar>-->

    <el-image v-if="!this.edit" style="width: 200px; height: 200px" :src="this.avatar" fit="cover"></el-image>
    <el-upload v-if="this.edit"
               class="avatar-uploader"
               action="/api/personaldata/"
               :sid="this.sid"
               :pswd="this.pswd"
               :auto-upload="true"
               :show-file-list="false"
               :on-success="handleAvatarSuccess"
               :before-upload="beforeAvatarUpload">
      <img v-if="imageUrl" :src="imageUrl" class="avatar">
      <i v-else class="el-icon-plus avatar-uploader-icon"></i>
    </el-upload>

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

      <el-button v-if="!this.edit" @click="onEditClicked()">EDIT</el-button>
      <el-button v-if="this.edit" @click="onConfirmEditClicked()">CONFIRM EDIT</el-button>

    </el-form>


    <!--    TODO: File upload. -->
    <!--    <el-upload-->
    <!--        class="upload-demo"-->
    <!--        drag-->
    <!--        action="/api/personaldata/"-->
    <!--        :name="this.sid"-->
    <!--        :multiple="true">-->
    <!--      <i class="el-icon-upload"></i>-->
    <!--    </el-upload>-->


  </div>
  <!--  <div>-->
  <!--  </div>-->
</template>

<script>


export default {
  name: 'profile',
  props: {
    sid: {
      type: String,
      required: true,
    },
    pswd: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      name: '',
      email: '',
      gender: '',
      mobile: '',
      address: '',
      imageUrl: '',
      dialogImageUrl: '',
      dialogVisible: '',
      avatar: null,
      edit: false,
    }
  },
  created() {
    console.log('profile created')
    console.log(this.sid)
    console.log(this.pswd)
    this.pullPersonalData()
    this.avatar = require('../assets/logo.png')
    // if (this.sid === '')
    // {
    //   this.sid = this.$route.params.sid
    //   this.name = this.$route.params.name
    // }
  },
  mounted() {
    console.log('profile mounted')
  },
  destroyed() {
    console.log('profile destroyed')
  },

  methods: {

    pullPersonalData() {
      this.$axios.post('/show_personal_data/', {sid: this.sid, pswd: this.pswd}).then(res => {
        const data = res.data
        console.log('res.data', data)
        //Remote quotes.
        console.log(data['email'])
        this.name = data['realname']
        this.gender = data['gender']
        this.email = data['email']
        this.mobile = data['mobile']
        this.address = data['address']
      }).catch(err => {
        console.log(err)
      })
    },

    //TODO: Add regex check for fields.
    onConfirmEditClicked() {
      this.$axios.post('/change_personal_data/', {
        sid: this.sid,
        pswd: this.pswd,
        email: this.email,
        gender: this.gender,
        mobile: this.mobile,
        address: this.address,
      }).then(res => {
        console.log('res', res)
      }).catch(err => {
        console.log('err', err)
      })

      this.pullPersonalData()

      this.edit = false
    },
    onEditClicked() {
      this.edit = true
    },

    saveFile(data, name) {
      try {
        data = new Blob([data])
        console.log(data)
        console.log(name)

        const blobUrl = window.URL.createObjectURL(data)
        const a = document.createElement('a')
        a.style.display = 'none'
        a.download = name
        a.href = blobUrl
        a.click()
        URL.revokeObjectURL(a.href)
      } catch (e) {
        alert('保存文件出错')
      }
    },
    testFileDownload() {
      this.$axios.post('/test/', {sid: this.sid}, {responseType: 'blob'}).then(res => {
        console.log('res', res)
        console.log(res.data.size)
        this.saveFile(res.data, '11811002.zip')
      }).catch(err => {
        console.log('err', err)
      })
    },
    onClickNewPassword() {
      this.$router.push({name: 'homepage_profile_newpassword', sid: this.$route.params.sid}).then(res => {
        console.log(res)
      }).catch(err => {
        console.log(err)
      })
    },

    handleAvatarSuccess(res, file) {
      console.log('raw', file.raw)
      console.log('raws', file.raws)
      console.log('success')
      console.log(res)
      console.log(file)
      this.imageUrl = URL.createObjectURL(file.raw)
    },
    beforeAvatarUpload(file) {
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
    handlePictureCardPreview(file) {
      console.log('preview')
      this.dialogImageUrl = file.url
      this.dialogVisible = true
    },
  },
}
</script>

<style>
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
</style>

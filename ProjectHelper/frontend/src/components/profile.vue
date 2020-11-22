<!--TODO After refresh, everything is gone.-->
<template>
  <div id="profile">
    <!--    <el-link href="https://127.0.0.1:8000/test/" target="_blank">默认链接</el-link>-->
    <!--    <el-button @click="testFileDownload">test file download</el-button>-->
    <el-avatar :size="60" :src="this.avatar"></el-avatar>
    <el-row>SID: {{ this.sid }}</el-row>
    <el-row>NAME: {{ this.name }}</el-row>
    <el-button @click="onClickNewPassword">New Password</el-button>
    <el-upload
        class="avatar-uploader"
        action="/api/personaldata/"
        :name="this.sid"
        :auto-upload="true"
        :show-file-list="false"
        :on-success="handleAvatarSuccess"
        :before-upload="beforeAvatarUpload">
      <img v-if="imageUrl" :src="imageUrl" class="avatar">
      <i v-else class="el-icon-plus avatar-uploader-icon"></i>
    </el-upload>
    <el-upload
        class="upload-demo"
        drag
        action="/api/personaldata/"
        :name="this.sid"
        :multiple="true">
      <i class="el-icon-upload"></i>
      <!--      <div class="el-upload__text">Drag file here, or <em>click to upload</em>.</div>-->
      <!--      <div class="el-upload__tip" slot="tip">.zip supported only</div>-->
    </el-upload>
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
  data ()
  {
    return {
      name: '',
      imageUrl: '',
      dialogImageUrl: '',
      dialogVisible: '',
      avatar: null,
    }
  },
  created ()
  {
    console.log('profile created')
    this.$axios.post('/personaldata/', { sid: this.sid, pswd: this.pswd }).then(res =>
    {
      console.log('res.data', res.data)
    }).catch(err =>
    {
      console.log(err)
    })
    this.avatar = require('../assets/logo.png')
    // if (this.sid === '')
    // {
    //   this.sid = this.$route.params.sid
    //   this.name = this.$route.params.name
    // }
  },
  mounted ()
  {
    console.log('profile mounted')
  },
  destroyed ()
  {
    console.log('profile destroyed')
  },

  methods: {
    saveFile (data, name)
    {
      try
      {
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
      } catch (e)
      {
        alert('保存文件出错')
      }
    },
    testFileDownload ()
    {
      this.$axios.post('/test/', { sid: this.sid }, { responseType: 'blob' }).then(res =>
      {
        console.log('res', res)
        console.log(res.data.size)
        this.saveFile(res.data, '11811002.zip')
      }).catch(err =>
      {
        console.log('err', err)
      })
    },
    onClickNewPassword ()
    {
      this.$router.push({ name: 'homepage_profile_newpassword', sid: this.$route.params.sid }).then(res =>
      {
        console.log(res)
      }).catch(err =>
      {
        console.log(err)
      })
    },

    handleAvatarSuccess (res, file)
    {
      console.log('raw', file.raw)
      console.log('raws', file.raws)
      console.log('success')
      console.log(res)
      console.log(file)
      this.imageUrl = URL.createObjectURL(file.raw)
    },
    beforeAvatarUpload (file)
    {
      const isJPG = file.type === 'image/jpeg'
      const isLt2M = file.size / 1024 / 1024 < 2
      if (!isJPG)
      {
        this.$message.error('上传头像图片只能是 JPG 格式!')
      }
      if (!isLt2M)
      {
        this.$message.error('上传头像图片大小不能超过 2MB!')
      }
      return isJPG && isLt2M
    },
    handlePictureCardPreview (file)
    {
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
  width: 178px;
  height: 178px;
  line-height: 178px;
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
© 2020 GitHub, Inc.
Terms
Privacy
Security
Status
Help
Contact GitHub
Pricing
API
Training
Blog
About

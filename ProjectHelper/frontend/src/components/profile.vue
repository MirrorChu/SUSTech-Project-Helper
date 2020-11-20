<!--TODO After refresh, everything is gone.-->
<template>
  <div id="profile">
    <el-avatar :size="48" :src="this.avatar"></el-avatar>
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
      <div class="el-upload__text">Drag file here, or <em>click to upload</em>.</div>
      <div class="el-upload__tip" slot="tip">.zip supported only</div>
    </el-upload>
  </div>
  <div>
    <el-button @click="testFileDownload">test file download</el-button>
  </div>
</template>

<script>
export default {
  name: 'profile',
  data ()
  {
    return {
      sid: '',
      imageUrl: '',
      dialogImageUrl: '',
      dialogVisible: '',
      avatar: null,
    }
  },
  created ()
  {
    console.log('before create')
    this.avatar = require('../assets/logo.png')
    if (this.sid === '')
    {
      this.sid = this.$route.params.sid
      this.name = this.$route.params.name
    }
  },
  methods: {
    testFileDownload ()
    {
      this.$axios.post('/login/', { sid: this.sid })
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

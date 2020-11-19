<!--TODO After refresh, everything is gone.-->
<template>
  <div id="profile">
    <el-row>Name: {{ this.$route.params.name }}</el-row>
    <el-row>SID: {{ this.$route.params.sid }}</el-row>
    <!--    <el-upload-->
    <!--      class="avatar-uploader"-->
    <!--      action=""-->
    <!--      list-type="picture"-->
    <!--      :on-preview="handlePictureCardPreview"-->
    <!--      :auto-upload="true"-->
    <!--      :show-file-list="false"-->
    <!--      :on-success="handleAvatarSuccess"-->
    <!--      :before-upload="beforeAvatarUpload">-->
    <!--      <img v-if="imageUrl" :src="imageUrl" class="avatar">-->
    <!--      <i v-else class="el-icon-plus avatar-uploader-icon"></i>-->
    <!--    </el-upload>-->
    <el-button @click="onClickNewPassword">New Password</el-button>
    <el-upload
      class="avatar-uploader"
      action="http://127.0.0.1:8000/personaldata"
      :auto-upload="true"
      :show-file-list="false"
      :on-success="handleAvatarSuccess"
      :before-upload="beforeAvatarUpload">
      <img v-if="imageUrl" :src="imageUrl" class="avatar">
      <i v-else class="el-icon-plus avatar-uploader-icon"></i>
    </el-upload>
  </div>
</template>

<script>
export default {
  name: 'profile',
  data ()
  {
    return {
      imageUrl: '',
      dialogImageUrl: '',
      dialogVisible: '',
    }
  },
  methods: {
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
    upload (file)
    {
      console.log(file)
      this.$axios.post('/profile/avatar', { file: file })
    },
    handleAvatarSuccess (res, file)
    {
      console.log('success')
      console.log(res)
      console.log(file)
      this.imageUrl = URL.createObjectURL(file.raw)
    },
    beforeAvatarUpload (file)
    {
      console.log('upload')
      console.log(file)
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

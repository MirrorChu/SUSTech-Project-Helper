<template>
  <div>
    <el-card>
      <h1>Change Password</h1>
      <el-form label-width="200px" class="demo-ruleForm">
        <el-form-item label="Old password">
          <el-input placeholder="old pswd" v-model="old_pswd" show-password clearable></el-input>
        </el-form-item>
        <el-form-item label="New password"> <el-input placeholder="new pswd" v-model="new_pswd" show-password clearable></el-input></el-form-item>
        <el-form-item label="Confirm new password"><el-input placeholder="repeat to confirm" v-model="repeat" show-password clearable></el-input></el-form-item>
        <el-button @click="onChangeClicked">change password</el-button>
      </el-form>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'NewPassword',
  data() {
    return {
      old_pswd: '',
      new_pswd: '',
      repeat: '',
    }
  },
  beforeDestroy() {
    this.old_pswd = ''
    this.new_pswd = ''
    this.repeat = ''
  },
  methods: {
    onChangeClicked() {
      if (this.new_pswd !== this.repeat) {
        this.$alert('New passwords input are not the same.')
        this.old_pswd = ''
        this.new_pswd = ''
        this.repeat = ''
      } else {
        this.$axios.post('/change_password/', {
          old: this.old_pswd,
          new: this.new_pswd
        }).then(res => {
          console.log(res)
          console.log(res.data)
          alert(res.data['ChangePasswordCheck'])
        }).catch(err => {
          console.log('err', err)
        })
        this.old_pswd = ''
        this.new_pswd = ''
        this.repeat = ''
      }
    },
  },
}
</script>

<style scoped>
.el-card{
  font-family: Verdana,serif;
  background-color: #F7F8F8;
  border-color:whitesmoke;
  align-content: center;
  text-align: center;
  line-height: 50px;
}
</style>

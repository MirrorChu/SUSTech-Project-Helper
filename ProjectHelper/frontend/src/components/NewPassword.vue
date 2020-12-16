<template>
  <div>
    <h1>Change Password</h1>
    <el-input placeholder="old pswd" v-model="old_pswd" show-password clearable></el-input>
    <el-input placeholder="new pswd" v-model="new_pswd" show-password clearable></el-input>
    <el-input placeholder="repeat to confirm" v-model="repeat" show-password clearable></el-input>
    <el-button @click="onChangeClicked">change password</el-button>
  </div>
</template>

<script>
export default {
  name: 'NewPassword',
  props: {
    sid: {
      type: String,
      required: true,
    },
  },
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
  //TODO: Add cookie.
  methods: {
    onChangeClicked() {
      if (this.new_pswd !== this.repeat) {
        this.$alert('New passwords input are not the same.')
        this.old_pswd = ''
        this.new_pswd = ''
        this.repeat = ''
      } else {
        this.$axios.post('/change_password/', {
          sid: this.$props.sid,
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

</style>

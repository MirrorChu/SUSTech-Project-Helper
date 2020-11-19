<template>
  <div>
    <el-input placeholder="old pswd" v-model="old_pswd" show-password clearable></el-input>
    <el-input placeholder="new pswd" v-model="new_pswd" show-password clearable></el-input>
    <el-input placeholder="confirm" v-model="confirm" show-password clearable></el-input>
    <el-button>change password</el-button>
  </div>
</template>

<script>
export default {
  name: 'new_password',
  props: {
    sid: {
      type: String,
    },
  },
  data ()
  {
    return {
      old_pswd: '',
      new_pswd: '',
      confirm: '',
    }
  },
  //TODO: Add cookie.
  methods: {
    onChangeClicked ()
    {
      if (this.new_pswd !== this.confirm)
      {
        this.$alert('New passwords input are not the same.')
        this.old_pswd = ''
        this.new_pswd = ''
        this.confirm = ''
      }
      else
      {
        this.$axios.post('/newpassword/', { sid: this.$props.sid, old: this.old_pswd, new: this.new_pswd }).then(res =>
        {
          console.log(res.data)
        }).catch(err =>
        {
          console.log('err', err)
        })
      }
    },
  },
}
</script>

<style scoped>

</style>

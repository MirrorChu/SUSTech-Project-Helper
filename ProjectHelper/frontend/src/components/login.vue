<template>
  <div class="login">
    <h1>LOGIN</h1>
    <el-input v-model="sid" placeholder="SID" clearable></el-input>
    <el-input v-model="pswd" show-password placeholder="PASSWORD" clearable></el-input>
    <el-button @click="onLoginClick()">LOGIN</el-button>
  </div>
</template>
<script>
export default {
  name: 'login',
  data ()
  {
    return {
      sid: '',
      pswd: '',
    }
  },
  methods: {
    onLoginClick ()
    {
      if (this.sid === '11813121' && this.pswd === '11813121')
      {
        this.$router.push(
          {
            name: 'homepage',
            params: {
              sid: this.sid,
              pswd: this.pswd,
            },
          })
      }
      else
      {
        this.sid = ''
        this.pswd = ''
        alert('WRONG SID OR PASSWORD')
      }
    },
  },
}
</script>

<!--<style scoped>-->

<!--</style>-->

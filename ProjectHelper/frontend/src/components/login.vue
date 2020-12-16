<template>
  <div class="login">
    <el-form :label-position="labelPosition" :label-width="labelWidth" class="input-box">
      <el-form-item label="Student ID">
        <el-input v-model="sid" placeholder="SID" clearable></el-input>
      </el-form-item>
      <el-form-item label="PASSWORD">
        <el-input v-model="pswd" show-password placeholder="PASSWORD" clearable></el-input>
      </el-form-item>
      <el-form-item>
        <el-button @click="onLoginClick()">LOGIN</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>
<script>
import axios from 'axios'

export default {
  name: 'login',
  data () {
    return {
      sid: '',
      pswd: '',
      labelPosition: 'left',
      labelWidth: '100px',
      identity: '',
    }
  },
  beforeCreate () {
    this.$axios.post('/login/', {}).then(res => {
      const status = res.data['loginCheck']
      if (status === 'student' || status === 'teacher') {
        this.$router.push({
          name: 'homepage',
          params: {
            sid: this.sid,
            identity: this.identity
          },
        })
      }
    }).catch(err => {
      console.log('err', err)
    })
  },
  methods: {
    onLoginClick () {
      //TODO Login request.
      axios.defaults.xsrfCookieName = 'csrftoken'
      axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN'
      let status = ''
      this.$axios.post('/login/', { sid: this.sid, pswd: this.pswd }).then(res => {
        status = res.data['loginCheck']
        this.identity = status
        if (this.identity === 'student' || this.identity === 'teacher') {
          console.log('zjs: res.data.Token', res.data.token)
          let token = res.data.token
          this.$store.commit('Login', { Authorization: token, sid: this.sid })
          this.$router.push({
            name: 'homepage',
            params: {
              sid: this.sid,
              pswd: this.pswd,
              identity: this.identity
            },
          })
        } else {
          this.sid = ''
          this.pswd = ''
          alert('WRONG SID OR PASSWORD')
        }
      }).catch(err => {
        console.log('err', err)
        alert(err)
      })
    },
  },
}
</script>

<style scoped>
.login {
  position: absolute;
  width: 400px;
  top: 42%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.input-box {
  border: 1px solid black;
  border-radius: 2px;
}

</style>

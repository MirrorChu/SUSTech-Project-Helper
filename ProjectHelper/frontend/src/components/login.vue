<template>
  <div class="login">
    <el-row :gutter="20">
      <!-- gutter 栅格间距 -->
      <el-col :span="8" :offset="8">
        <!-- span 栅格占的列数，offset是偏移列数 -->
        <div class="grid-content"></div>
      </el-col>
    </el-row>

    <el-row :gutter="20" >
      <!-- gutter 栅格间距 -->

      <el-col :span="8" :offset="8">
        <!-- span 栅格占的列数，offset是偏移列数 -->
        <el-card shadow="always" style="background-color:rgba(255,255,255,0.8)" >
          <h1 style="color: black;padding-left: 86px">Member login</h1>
          <h1 style="color: #898787;font-size: 16px;padding-left: 94px">Welcome to Project Hub.</h1>
          <el-divider></el-divider>

          <el-form :model="nameValidateForm" ref="nameValidateForm" label-width="100px" class="demo-ruleForm">
            <!-- 用户名 -->
            <el-form-item
              label="Username"
              prop="sid"
              :rules="[
                    { required: true, message: 'Username can not be empty.'},
                    ]"
            >
              <el-input placeholder="Username" type="text" v-model="nameValidateForm.sid" autocomplete="off">
                <!--              style="color: rgba(0,0,0,0.2);border-color:#333333;"-->
              </el-input>
            </el-form-item>

            <!-- 密码 -->
            <el-form-item
              label="Password"
              prop="pswd"
              :rules="[
                    { required: true, message: 'Password can not be empty.'},
                    ]"
            >
              <el-input placeholder="Password" v-model="nameValidateForm.pswd" show-password></el-input>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="onLoginClick()"
                         style="width:170px;height: 50px;">提交</el-button>
            </el-form-item>
          </el-form>

        </el-card>
      </el-col>

    </el-row>

  </div>
</template>

<script>
import { setCookie, getCookie } from '../assets/js/cookie.js'
import axios from 'axios'
export default {
  name: 'Login',
  data () {
    return {
      nameValidateForm:
        {
          sid: '',
          pswd: '',
          identity: '',
        }
    };
  },
  beforeCreate () {
    this.$axios.post('/login/', {}).then(res => {
      const status = res.data['loginCheck']
      if (status === 'student' || status === 'teacher') {
        this.$router.push({
          name: 'Homepage',
          params: {
            sid: this.nameValidateForm.sid,
            identity: this.nameValidateForm.identity
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
      this.$axios.post('/login/', { sid: this.nameValidateForm.sid, pswd: this.nameValidateForm.pswd }).then(res => {
        status = res.data['loginCheck']
        this.nameValidateForm.identity = status
        if (this.nameValidateForm.identity === 'student' || this.nameValidateForm.identity === 'teacher') {
          let token = res.data.token
          // setCookie('sid', this.sid, 1000 * 60)
          this.$store.commit('Login', { Authorization: token, sid: this.nameValidateForm.sid })
          this.$router.push({
            name: 'Homepage',
            params: {
              sid: this.nameValidateForm.sid,
              pswd: this.nameValidateForm.pswd,
              identity: this.nameValidateForm.identity
            },
          })
        } else {
          this.nameValidateForm.sid = ''
          this.nameValidateForm.pswd = ''
          alert('WRONG SID OR PASSWORD')
        }
      }).catch(err => {
        console.log('err', err)
        alert(err)
      })
    },

  }
}
</script>

<style>
.content{
  margin: 0 auto;
  background-color:whitesmoke;
}
.el-card{
  /*border: 1000px;*/
  border-color : whitesmoke;
  background-color:rgba(0,0,0,0.2)
  /*border-radius:30px;*/
  /* box-shadow: 0 2px 12px 0 rgb(243, 102, 102); */
  /* box-shadow: 0 2px 4px rgba(0, 0, 0, .12), 0 0 6px rgba(0, 0, 0, .04); */
}
.grid-content {
  /* background: rgb(14, 214, 131); */
  /*border-radius: 4px;*/
  min-height: 80px;
  /*background-color: #333333;*/
}
.el-row {
  margin-bottom: 20px;
}
/*.hello {*/
/*  !*background-color: black;*!*/
/*  background: url(../../assets/img/download.png) no-repeat 5px 5px;*/
/*  margin: -60px;*/
/*  padding: -60px;*/
/*  !*margin-right: -60px;*!*/
/*  border: black;*/
/*  height: 100vh;*/
/*}*/
.login{

  position:fixed;

  top: 0;

  left: 0;

  width:100%;

  height:100%;

  min-width: 1000px;

  z-index:-10;

  zoom: 1;

  background-color: #fff;

  background: url(pic2.jpg);

  background-repeat:no-repeat;

  background-size: cover;

  -webkit-background-size: cover;

  -o-background-size: cover;

  background-position: center 0;

}


</style>

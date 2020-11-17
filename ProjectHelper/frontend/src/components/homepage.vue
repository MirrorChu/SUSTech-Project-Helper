<template>
  <div class="homepage">
    <el-header>HOMEPAGE</el-header>
    <el-row>
      Hello, {{ name }}
    </el-row>
    <el-row>
      <el-button @click="onClickProfile">My Profile</el-button>
      <el-button @click="onClickNewPassword">New Password</el-button>
    </el-row>
    <profile id="my_profile" v-if="show_profile" v-bind:sid="this.sid" v-bind:name="this.name"></profile>
  </div>
</template>

<script>
import profile from './profile'

export default {
  name: 'homepage',
  components: { profile },
  data ()
  {
    return {
      sid: this.$route.params.sid,
      pswd: this.$route.params.pswd,
      name: '',
      show_profile: false,
    }
  },
  created ()
  {
    console.log('sid', this.sid)
    if (this.sid === '11813121' && this.pswd === '11813121')
    {
      this.name = 'Jiashu'
    }
    else
    {
      this.$router.push('login')
    }
  },
  methods: {
    onClickProfile ()
    {
      this.show_profile = !this.show_profile
    },
    onClickNewPassword ()
    {

    },
  },
}
</script>

<style scoped>

</style>

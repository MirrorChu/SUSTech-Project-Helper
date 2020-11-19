<template>
  <div id="profile">
    <el-row>Name: {{ this.name }}</el-row>
    <el-row>SID: {{ this.sid }}</el-row>
    <el-button @click="onClickNewPassword" v-if="!this.show_new_password">New Password</el-button>
    <new_password v-if="this.show_new_password"></new_password>
  </div>
</template>

<script>
import { updateCookie } from '../assets/js/cookie'
import New_password from './new_password'

export default {
  name: 'profile',
  components: { New_password },
  data ()
  {
    return {
      name: this.$route.params.name,
      sid: this.$route.params.sid,
      show_new_password: false,
    }
  },
  methods: {
    //TODO: New password request.
    onClickNewPassword ()
    {
      this.show_new_password = true
      updateCookie('sid', this.sid, 1000 * 60)
    },
  },
}

</script>

<style scoped>

</style>

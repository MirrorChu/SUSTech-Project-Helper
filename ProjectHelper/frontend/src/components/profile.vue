<template>
  <div id="profile">
    <el-row>Name: {{ this.name }}</el-row>
    <el-row>SID: {{ this.sid }}</el-row>
  </div>
</template>

<script>
export default {
  name: 'profile',
  props: {
    sid: {
      type: String,
    },
    name: {
      type: String,
    },
  },
  data ()
  {
    return {
      sid: this.props.sid,
      name: this.props.name,
    }
  },
}
</script>

<style scoped>

</style>

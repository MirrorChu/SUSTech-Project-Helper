<template>
  <div id="profile">
    <el-row>Name: {{ this.$props.name }}</el-row>
    <el-row>SID: {{ this.$props.sid }}</el-row>
  </div>
</template>

<script>
export default {
  name: 'profile',
  props: {
    name: {
      type: String,
    },
    sid: {
      type: String,
    },
  },
}

</script>

<style scoped>

</style>

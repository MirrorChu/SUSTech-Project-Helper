<template>
  <div id="profile">
    <el-row>Name: {{ this.$route.params.name }}</el-row>
    <el-row>SID: {{ this.$route.params.sid }}</el-row>
  </div>
</template>

<script>
export default {
  name: 'profile',
}

</script>

<style scoped>

</style>

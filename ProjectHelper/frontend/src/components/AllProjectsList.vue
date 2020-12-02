<template>

</template>

<script>
export default {
  props: {
    sid: {
      type: String,
      required: true
    },
    pswd: {
      type: String,
      required: true
    }
  },
  name: "AllProjectsList",
  created() {
    this.$axios.post('/student_gets_all_projects/', {sid: this.props.sid, pswd: this.props.pswd})
  }
}
</script>

<style scoped>

</style>

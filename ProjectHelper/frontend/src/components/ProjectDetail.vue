<template>
  <div>
    {{ this.sid }}
    {{ this.pswd }}
    {{ this.projectDetail }}
  </div>
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
    },
    projectDetail: {
      required: true
    },
  },
  data() {
    return {
      val1: 'val1',
      val2: 'val2',
      val3: 'val3',
      groupInfo: ''
    }
  },
  created() {

  },
  name: "ProjectDetail"
}
</script>

<style scoped>

</style>

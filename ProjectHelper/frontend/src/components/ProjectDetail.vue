<template>
  <div>
    {{ this.$props.projectDetail }}

    {{ this.groupInfo }}
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
  created() {
    //Use == instead of === here.
    if (this.$props.groupInfo == null) {
      this.groupInfo = 'You have not created or joined a group!'
    } else {
      this.groupInfo = 'unknown'
    }
  },
  data() {
    return {
      val1: 'val1',
      val2: 'val2',
      val3: 'val3',
      groupInfo: '',
    }
  },
  name: "ProjectDetail"

}
</script>

<style scoped>

</style>

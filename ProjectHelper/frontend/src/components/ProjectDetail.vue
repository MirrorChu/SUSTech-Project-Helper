<template>
  <div>
    Course Name: {{ this.$props.groupInfo.course_name }}
    <br>
    Project Name: {{ this.$props.groupInfo.project_name }}
    <br>
    Group Instruction: {{ this.$props.groupInfo.project_introduction }}
    <br>
    Group Name: {{ this.$props.groupInfo.group_name }}
    <br>
    Captain Name: {{ this.$props.groupInfo.captain_name }}
    <br>
    Members: {{ this.memberlist}}
    <br>
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
    groupInfo: {
      required: true
    },
  },
  created() {
    //Use == instead of === here.
    if (this.$props.groupInfo == null) {
      this.status = 'You have not in a group!'
    }
    else if(this.$props.groupInfo.StudentGetsGroupInformationInProject === "no group") {
      this.status = 'You have not in a group!'
    }
    else if(this.$props.groupInfo.StudentGetsGroupInformationInProject == null) {
      console.log('successs')
      this.memberlist = ''
      for(var i=0;i<this.$props.groupInfo.members.length;i++){
        this.memberlist = this.memberlist + this.$props.groupInfo.members[i] + '  '
      }
    }
    else {
      this.status = 'unknown'
    }
  },
  data() {
    return {
      val1: 'val1',
      val2: 'val2',
      val3: 'val3',
    }
  },
  name: "ProjectDetail",
  memberlist: '',
  status: '',
}
</script>

<style scoped>

</style>

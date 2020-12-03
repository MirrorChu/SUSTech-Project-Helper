<template>
  <div>
    Course Name: {{ this.$props.projectDetail.course_name }}
    <br>
    Project Name: {{ this.$props.projectDetail['project_name'] }}
    <br>
    <GroupInfo v-if="this.$props.groupInfo.StudentGetsGroupInformationInProject == null"
               v-bind:group-info="this.$props.groupInfo" v-bind:members-list="this.membersList"
               v-bind:sid="this.$props.sid" v-bind:pswd="this.$props.pswd"></GroupInfo>
    <h1 v-if="!(this.$props.groupInfo.StudentGetsGroupInformationInProject == null)">You are not in any groups!</h1>
    <CreateOrJoinGroup v-if="!(this.$props.groupInfo.StudentGetsGroupInformationInProject == null)"
                       v-bind:sid="this.$props.sid" v-bind:pswd="this.$props.pswd"
                       v-bind:projectId="this.$props.groupInfo.project_id"></CreateOrJoinGroup>
  </div>
</template>

<script>
import GroupInfo from './GroupInfo'
import CreateOrJoinGroup from './CreateOrJoinGroup'

export default {
  components: { CreateOrJoinGroup, GroupInfo },
  props: {
    sid: {
      type: String,
      required: true,
    },
    pswd: {
      type: String,
      required: true,
    },
    projectDetail: {
      required: true,
    },
    groupInfo: {
      required: true,
    },
  },
  created () {
    //Use == instead of === here.
    if (this.$props.groupInfo == null) {
      this.status = 'You are not in a group!'
    } else if (this.$props.groupInfo.StudentGetsGroupInformationInProject === 'no group') {
      this.status = 'You are not in a group!'
    } else if (this.$props.groupInfo.StudentGetsGroupInformationInProject == null) {
      console.log('access group info success')
      console.log(this.$props.groupInfo['members'])
      for (let i = 0; i < this.$props.groupInfo['members'].length; i++) {
        this.membersList = this.membersList + this.$props.groupInfo['members'][i] + '  '
      }
    } else {
      this.status = 'unknown'
    }
  },
  data () {
    return {
      membersList: '',
      status: '',
    }
  },
  name: 'ProjectDetail',
}
</script>

<style scoped>

</style>

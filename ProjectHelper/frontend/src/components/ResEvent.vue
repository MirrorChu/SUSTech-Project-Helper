<template>
  <div>
    <div v-if="eventJsonObj.type === 'AnnouncementComponent'">

    </div>
    <div v-else-if="eventJsonObj.type === 'SubmissionComponent'">
      <ResSubmission></ResSubmission>
    </div>
    <div v-else-if="eventJsonObj.type === 'PartitionComponent'">
      <ResPartition></ResPartition>
    </div>
    <div v-else-if="eventJsonObj.type === 'SelectionComponent'">
      <ResSelection></ResSelection>
    </div>
  </div>
</template>

<script>
import ResSubmission from './ResSubmission'
import ResPartition from './ResPartition'
import ResSelection from './ResSelection'

export default {
  name: 'ResEvent',
  components: { ResSelection, ResPartition, ResSubmission },
  props: {
    sid: {
      type: String,
      required: true,
    },
    pswd: {
      type: String,
      required: true,
    },
    
  },
  data () {
    return {
      eventJsonObj: {
        type: 'PartitionComponent',
      },
    }

  },
}
</script>

<style scoped>

</style>

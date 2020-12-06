<template>
  <div>
    <div><h3>New Event</h3></div>
    <div>
      <el-form>
        <el-form-item label="Event Type">
          <el-radio-group v-model="eventType">
            <el-radio :label="0">Announcement</el-radio>
            <el-radio :label="1">Selection</el-radio>
            <el-radio :label="2">Submission</el-radio>
            <el-radio :label="3">Partition</el-radio>
            <el-radio :label="4">Upload</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item v-if="eventType === 0">
          <NewAnnouncement></NewAnnouncement>
        </el-form-item>
        <el-form-item v-else-if="eventType === 1">
          <NewSelection></NewSelection>
        </el-form-item>
        <el-form-item v-else-if="eventType === 2">
          <NewSubmission></NewSubmission>
        </el-form-item>
        <el-form-item v-else-if="eventType === 3">
          <NewPartition></NewPartition>
        </el-form-item>
        <el-form-item v-else-if="eventType === 4">
          TODO
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script>
import NewAnnouncement from './NewAnnouncement'
import NewSelection from './NewSelection'
import NewSubmission from './NewSubmission'
import NewPartition from './NewPartition'

export default {
  name: 'NewEvent',
  components: { NewPartition, NewSubmission, NewSelection, NewAnnouncement },
  props: {
    sid: {
      type: String,
      required: true,
    },
    pswd: {
      type: String,
      required: true,
    },
    projectId: {
      type: Number,
      required: true,
    },
  },
  data () {
    return {
      eventType: 1,
    }
  },
}
</script>

<style scoped>

</style>

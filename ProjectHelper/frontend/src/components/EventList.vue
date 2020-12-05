<template>
  <div>
    <h1>{{ this.name }}</h1>
    <el-card v-for="componentObj in componentObjs">
      <component :is="componentObj.type" :data="componentObj.data">

      </component>
    </el-card>
  </div>
</template>

<script>
import AnnouncementComponent from './AnnouncementComponent'
import SelectionComponent from './SelectionComponent'
import SubmissionComponent from './SubmissionComponent'
import PartitionEvent from './PartitionEvent'

export default {
  name: 'EventList',
  components: { PartitionEvent, SubmissionComponent, SelectionComponent, AnnouncementComponent },
  props: {
    sid: {
      type: String,
      required: true,
    },
    pswd: {
      type: String,
      required: true,
    },
    identity: {
      type: String,
      required: true,
    },
  },
  data () {
    return {
      name: 'Events',
      componentsStr: '',
      componentObjs: [],
    }
  },
  created () {
    this.componentObjs = [
      {
        type: 'AnnouncementComponent',
        sid: this.$props.sid,
        pswd: this.$props.pswd,
        data: {
          title: 'Demo Title',
          content: 'This is a demo announcement.',
        },
      },
      {
        type: 'SelectionComponent',
        sid: this.$props.sid,
        pswd: this.$props.pswd,
        data: {
          title: 'Demo Selection',
          introduction: 'Choose your selection wisely.',
          selectionLimit: 2,
          options: [
            { label: 'label1', value: 'value1' },
            { label: 'label2', value: 'value2' },
            { label: 'label3', value: 'value3' }],
        },
      },
      {
        type: 'SubmissionComponent',
        sid: this.$props.sid,
        pswd: this.$props.pswd,
        data: {
          title: 'Demo Submission',
          introduction: 'This is a demo submission.',
          submissionType: 'file',
        },
      },
      {
        type: 'PartitionEvent',
        sid: this.$props.sid,
        pswd: this.$props.pswd,
        data: {
          title: 'Demo Partition',
          introduction: 'This is a demo partition.',
          selectionLimit: 1,
          options: [
            { label: 'label1', value: 'value1', limit: 5 },
            { label: 'label2', value: 'value2', limit: 5 },
            { label: 'label3', value: 'value3', limit: 5 },
          ],
        },
      }]
  },
}
</script>

<style scoped>

</style>

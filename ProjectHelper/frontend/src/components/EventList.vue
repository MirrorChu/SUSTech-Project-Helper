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

export default {
  name: 'EventList',
  components: { SubmissionComponent, SelectionComponent, AnnouncementComponent },
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
        data: { title: 'Demo Title', content: 'This is a demo announcement.' },
      },
      {
        type: 'SelectionComponent',
        data: {
          title: 'Demo Selection',
          introduction: 'Choose your selection wisely.',
          selectionLimit: 1,
          options: [
            { label: 'label1', value: 'value1' },
            { label: 'label2', value: 'value2' },
            { label: 'label3', value: 'value3' }],
        },
      },
      {
        type: 'SubmissionComponent',
        sid: '11810101',
        pswd: '11810101',
        data: {
          title: 'Demo Submission',
          introduction: 'This is a demo submission.',
          submissionType: 'file',
        },
      }]
  },
}
</script>

<style scoped>

</style>

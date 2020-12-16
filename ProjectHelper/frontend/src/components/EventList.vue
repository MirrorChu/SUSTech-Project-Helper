<template>
  <div>
    <h1 style="color:#003371;text-align: center">Event List</h1>
    <div v-if="this.identity === 'teacher'">
      <el-card>
        <NewEvent v-bind:sid="this.$props.sid"
                  v-bind:projectId="this.$props.projectId">
        </NewEvent>
      </el-card>
    </div>
    <div>
      <el-card v-for="(componentObj, index) in componentObjs">
        <component :is="componentObj.type" :data="componentObj.data">

        </component>

      </el-card>
    </div>
  </div>
</template>

<script>
import AnnouncementComponent from './AnnouncementComponent'
import SelectionComponent from './SelectionComponent'
import SubmissionComponent from './SubmissionComponent'
import PartitionEvent from './PartitionEvent'
import NewEvent from './NewEvent'
import ResEvent from './ResEvent'
import EventGrading from './EventGrading'

export default {
  name: 'EventList',
  components: {
    EventGrading,
    ResEvent,
    NewEvent,
    PartitionEvent,
    SubmissionComponent,
    SelectionComponent,
    AnnouncementComponent,
  },
  props: {
    sid: {
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
      name: 'Events',
      componentsStr: '',
      componentObjs: [],
      identity: '',
      expandNewEvent: false,
    }
  },
  created () {
    this.$axios.post('/get_identity/', {}).then(res => {
      this.identity = res.data['identity']
    }).catch(err => {
      console.log('err', err)
    })
    this.componentObjs = [
      {
        type: 'AnnouncementComponent',
        sid: this.$props.sid,
        pswd: this.$props.pswd,
        data: {
          type: 'AnnouncementComponent',
          title: 'Demo Announcement',
          introduction: 'This is a demo announcement.',
          due: (new Date()).getTime(),
        },
      },
      {
        type: 'SelectionComponent',
        sid: this.$props.sid,
        pswd: this.$props.pswd,
        data: {
          type: 'SelectionComponent',
          title: 'Demo Selection',
          introduction: 'Choose your selection wisely.',
          due: (new Date()).getTime(),
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
        due: (new Date()).getTime(),
        data: {
          type: 'SubmissionComponent',
          title: 'Demo Submission',
          introduction: 'This is a demo submission.',
          submissionType: 'file',
          due: (new Date()).getTime(),
        },
      },
      {
        type: 'PartitionEvent',
        sid: this.$props.sid,
        pswd: this.$props.pswd,
        due: (new Date()).getTime(),
        data: {
          type: 'PartitionEvent',
          title: 'Demo Partition',
          introduction: 'This is a demo partition.',
          selectionLimit: 1,
          options: [
            { label: 'label1', value: 'value1', limit: 5 },
            { label: 'label2', value: 'value2', limit: 5 },
            { label: 'label3', value: 'value3', limit: 5 },
          ],
          due: (new Date()).getTime(),
        },
      }]
  },
}
</script>

<style scoped>
.el-card{
  font-family: Verdana;
  background-color: #F7F8F8;
  border-color:whitesmoke;
  /*align-content:space-around;*/
  text-align: -webkit-left;
  line-height: 30px;
}
.el-card:hover{
  font-family: Verdana;
  background-color: #fffbf0;
  border-color:whitesmoke;
  /*align-content:space-around;*/
  text-align: -webkit-left;
  line-height: 30px;
}
</style>

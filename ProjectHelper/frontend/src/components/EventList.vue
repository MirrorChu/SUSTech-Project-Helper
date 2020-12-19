<template>
  <div>
    <h1 style="color:#003371;text-align: center">Event List</h1>
    <div v-if="this.privileges['teach'] === 1">
      <el-card>
        <NewEvent v-bind:sid="this.$props.sid"
                  v-bind:course-id="this.$props.courseId"
                  v-bind:projectId="this.$props.projectId">
        </NewEvent>
      </el-card>
    </div>
    <div>
      <el-card v-for="(componentObj) in componentObjs">

        <!--        <h2>{{componentObj['data']['title']}}</h2>-->

        <!--        <el-button-->
        <!--            @click="onClickExpandComponent(componentObj['id'])">-->
        <!--          {{ visible[componentObj['id']] ? 'Close' : 'Expand' }}-->
        <!--        </el-button>-->

        <!--        <div v-if="visible[componentObj['id']]">-->
        <div>
          <component :is="componentObj.type"
                     :data="componentObj.data"
                     :courseId="courseId"
                     :projectId="projectId"
                     :eventTitle="componentObj['data']['title']"
                     :eventId="componentObj['id']">
          </component>
        </div>

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
    courseId: {
      type: Number,
      required: true,
    },
  },
  data () {
    return {
      name: 'Events',
      componentsStr: '',
      componentObjs: [],
      expandNewEvent: false,
      privileges: {},
      eventObjList: [],
      visible: {},
    }
  },
  created () {
    this.courseId = this.$props.courseId
    this.projectId = this.$props.projectId
    this.$axios.post('/get_privilege_list/', { 'course_id': this.$props.courseId }).then(res => {
      this.privileges = res.data['Data']
      this.$axios.post('/get_event_list/', { 'project_id': this.$props.projectId }).then(res => {
        console.log('event list', res)
        const tempEventArray = res.data['Data']
        this.componentObjs = []
        for (let i = 0; i < tempEventArray.length; i += 1) {
          const eventEle = tempEventArray[i]
          const eventObj = {}
          const typeStr = eventEle['event_type']
          if (typeStr === 'partition') {
            eventObj['type'] = 'PartitionEvent'
            // eventObj['data'] = {}
            // eventObj['data']['type'] = 'PartitionEvent'
            // eventObj['data']['selectionLimit'] = eventEle['event_detail']['selectionLimit']
            // eventObj['partitionType'] = eventEle['event_detail']['partitionType']
            // eventObj['data']['options'] = []
            // for (let j = 0; j < eventEle['event_detail']['options'].length; j += 1) {
            //   const option = eventEle['event_detail']['options'][j]
            //   eventObj['data']['options'].push({'label': option[0], 'value': option[0], 'limit': option[1]})
            // }
          }
          eventObj['data'] = {}
          eventObj['data']['title'] = eventEle['event_title']
          // eventObj['data']['introduction'] = eventEle['introduction']
          // eventObj['data']['due'] = eventEle['event_detail']['due']
          // eventObj['publisher'] = eventEle['publisher']
          eventObj['id'] = eventEle['id']
          this.componentObjs.push(eventObj)
          this.visible[eventObj['id']] = false
        }
        console.log(this.componentObjs)
      }).catch(err => {
        console.log('/get_event_list err', err)
      })

      ////  ===***--- DO NOT DELETE THIS ---***=== ////
      // this.componentObjs = [
      //   {
      //     type: 'AnnouncementComponent',
      //     sid: this.$props.sid,
      //     pswd: this.$props.pswd,
      //     data:
      //     {
      //       type: 'AnnouncementComponent',
      //       title: 'Demo Announcement',
      //       introduction: 'This is a demo announcement.',
      //       due: (new Date()).getTime(),
      //     },
      //   },
      //   {
      //     type: 'SelectionComponent',
      //     sid: this.$props.sid,
      //     pswd: this.$props.pswd,
      //     data: {
      //       type: 'SelectionComponent',
      //       title: 'Demo Selection',
      //       introduction: 'Choose your selection wisely.',
      //       due: (new Date()).getTime(),
      //       selectionLimit: 2,
      //       options: [
      //         { label: 'label1', value: 'value1' },
      //         { label: 'label2', value: 'value2' },
      //         { label: 'label3', value: 'value3' }],
      //     },
      //   },
      //   {
      //     type: 'SubmissionComponent',
      //     sid: this.$props.sid,
      //     pswd: this.$props.pswd,
      //     due: (new Date()).getTime(),
      //     data: {
      //       type: 'SubmissionComponent',
      //       title: 'Demo Submission',
      //       introduction: 'This is a demo submission.',
      //       submissionType: 'file',
      //       due: (new Date()).getTime(),
      //     },
      //   },
      //   {
      //     type: 'PartitionEvent',
      //     sid: this.$props.sid,
      //     pswd: this.$props.pswd,
      //     due: (new Date()).getTime(),
      //     data: {
      //       type: 'PartitionEvent',
      //       title: 'Demo Partition',
      //       introduction: 'This is a demo partition.',
      //       selectionLimit: 1,
      //       options: [
      //         { label: 'label1', value: 'value1', limit: 5 },
      //         { label: 'label2', value: 'value2', limit: 5 },
      //         { label: 'label3', value: 'value3', limit: 5 },
      //       ],
      //       due: (new Date()).getTime(),
      //     },
      //   }]
    }).catch(err => {
      console.log('EventList /student_gets_all_projects/', err)
    })
  },
  methods: {
    // onClickExpandComponent(id) {
    //   this.visible[id] = !this.visible[id];
    //   console.log(this.visible[id])
    // },
  },
}
</script>

<style scoped>
.el-card {
  font-family: Verdana, serif;
  background-color: #F7F8F8;
  border-color: whitesmoke;
  /*align-content:space-around;*/
  text-align: -webkit-left;
  line-height: 30px;
}

.el-card:hover {
  font-family: Verdana, serif;
  background-color: #fffbf0;
  border-color: whitesmoke;
  /*align-content:space-around;*/
  text-align: -webkit-left;
  line-height: 30px;
}
</style>

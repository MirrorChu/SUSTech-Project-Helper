<template>
  <div>
    <h1 style="font-family: Verdana, serif;">Event List</h1>
    <div v-if="this.privileges['teach'] && this.privileges['teach'] === 1">
      <el-card>
        <NewEvent v-bind:sid="this.$props.sid"
                  v-bind:course-id="this.$props.courseId"
                  v-bind:projectId="this.$props.projectId">
        </NewEvent>
      </el-card>
    </div>
    <div>
      <el-card v-for="(componentObj) in componentObjs">
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
      <el-divider></el-divider>
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
    this.pullData()
  },
  methods: {
    // onClickExpandComponent(id) {
    //   this.visible[id] = !this.visible[id];
    //   console.log(this.visible[id])
    // },
    pullData () {
      this.courseId = this.$props.courseId
      this.projectId = this.$props.projectId
      this.$axios.post('/get_privilege_list/', { 'course_id': this.$props.courseId }).then(res => {
        console.log(res)
        this.privileges = res.data['Data']
        this.$axios.post('/get_event_list/', { 'project_id': this.$props.projectId }).then(res => {
          console.log(res)
          const tempEventArray = res.data['Data']
          this.componentObjs = []
          for (let i = 0; i < tempEventArray.length; i += 1) {
            const eventEle = tempEventArray[i]
            const eventObj = {}
            const typeStr = eventEle['event_type']
            if (typeStr === 'partition') {
              eventObj['type'] = 'PartitionEvent'
            } else if (typeStr === 'submission' || typeStr === 'SubmissionEvent') {
              eventObj['type'] = 'SubmissionComponent'
            } else if (typeStr === 'announcement' || typeStr === 'AnnouncementEvent' || typeStr ===
                'AnnouncementComponent') {
              eventObj['type'] = 'AnnouncementComponent'
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
          console.log(err)
        })
      }).catch(err => {
        console.log(err)
      })
    },
    testing () {
      this.pullData()
    },
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

/*.el-card:hover {*/
/*  font-family: Verdana, serif;*/
/*  background-color: #fffbf0;*/
/*  border-color: whitesmoke;*/
/*  !*align-content:space-around;*!*/
/*  text-align: -webkit-left;*/
/*  line-height: 30px;*/
/*}*/
</style>

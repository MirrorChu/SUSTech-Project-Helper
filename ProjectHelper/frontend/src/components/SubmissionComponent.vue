<template>
  <div>
    <div>
      <h3>{{ this.$props.data.title }}</h3>
    </div>
    <div v-if="!expand">
      <el-button @click="onClickExpand">Expand</el-button>
    </div>

    <div v-if="expand">
      <div>
        <el-button @click="onClickExpand">Close</el-button>
      </div>

      <div v-if="privileges['teach']">
        <el-button @click="edit = !edit">{{ edit ? 'Close' : 'Edit' }}</el-button>

        <div v-if="edit">
          <el-form>
            <el-form-item label="Introduction">
              <el-input type="textarea" v-model="this.eventObj['data']['introduction']"></el-input>
            </el-form-item>
          </el-form>
        </div>
      </div>

      <div v-if="!edit">
        <div>Introduction: {{ this.eventObj['data']['introduction'] }}</div>
        <div>Due: {{ new Date(this.eventObj.data.due) }}</div>
      </div>

      <div v-if="privileges['teach'] === 1">
        <div>
          <el-button @click="onClickDeleteEvent">Delete Event</el-button>
        </div>

        <div>
          <EventGrading
              v-bind:eventDetail="eventDetail"
              v-bind:eventId="this.$props.eventId"
              v-bind:submissionDetail="submissionDetail">
          </EventGrading>
        </div>

      </div>
      <div v-else>
        <el-upload
            drag
            action="http://127.0.0.1:8000/submit_event/"
            :data="dataBlock"
            :on-success="onSuccess"
            multiple>
          <i class="el-icon-upload"></i>
          <div class="el-upload__text">Drag files here, or <em>click to upload</em>.</div>
        </el-upload>
      </div>

    </div>


  </div>
</template>

<script>
import EventGrading from './EventGrading'

export default {
  name: 'SubmissionComponent',
  components: { EventGrading },
  props: {
    data: {
      required: true,
    },
    courseId: {
      required: true,
    },
    eventId: {
      required: true,
    },
  },
  data () {
    return {
      submissionText: '',
      fileList: [],
      expand: false,
      eventDetail: {},
      edit: false,
      eventObj: {},
      submissionDetail: [],
      privileges: {},
      dataBlock: {},
    }
  },
  created () {
    this.token = localStorage.getItem('Authorization')
    this.edit = false
    this.$axios.post('/get_event_detail/', { 'event_id': this.$props.eventId }).then(res => {
      console.log(res)
      this.submissionDetail = res.data['Data']['data']
      this.eventDetail = res.data
      const eventEle = res.data['Data']
      const typeStr = eventEle['event_type']
      if (typeStr === 'submission' || typeStr === 'SubmissionEvent') {
        this.eventObj['type'] = 'SubmissionComponent'
        this.eventObj['data'] = {}
        this.eventObj['data']['type'] = 'SubmissionComponent'
        this.eventObj['partitionType'] = eventEle['event_detail']['partitionType']
      }
      this.eventObj['data']['title'] = eventEle['event_title']
      this.eventObj['data']['introduction'] = eventEle['introduction']
      this.eventObj['data']['due'] = eventEle['event_detail']['due']
      this.eventObj['publisher'] = eventEle['publisher']
      this.eventObj['id'] = this.$props.eventId

      this.$axios.post('/get_privilege_list/', { 'course_id': this.$props.courseId }).then(res => {
        this.privileges = res.data['Data']
      }).catch(err => {
        console.log(err)
      })
      this.dataBlock['token'] = localStorage.getItem('Authorization')
      this.dataBlock['event_id'] = this.$props.eventId
    }).catch(err => {
      console.log(err)
    })
  },
  methods: {
    onClickDeleteEvent () {
      this.$axios.post('/delete_event/', { 'event_id': this.eventObj['id'] }).then(res => {
        alert('Delete Event ' + res.data['DeleteEvent'])
      }).catch(err => {
        console.log(err)
      })
    },
    onClickSubmit () {
      //  TODO: Implement submit.
    },
    handleFileChange () {

    },
    handleFileRemove () {

    },
    onClickExpand () {
      this.expand = !this.expand
    },
    onSuccess(response, file, fileList) {
      console.log(response)
    },
  },
}
</script>

<style scoped>

</style>

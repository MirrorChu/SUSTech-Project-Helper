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
      <div>
        {{ this.$props.data.introduction }}
      </div>
      <div>Due: {{ new Date(this.$props.data.due) }}</div>
      <div v-if="this.$props.data.submissionType === 'text'">
        <el-input v-model="this.submissionText" clearable type="textarea"
                  placeholder="Input your submission."></el-input>
      </div>
      <div v-if="this.$props.data.submissionType === 'file'">
        <el-upload
            class="upload-demo"
            ref="upload"
            :data="{sid: this.$props.sid, pswd: this.$props.pswd}"
            action="/api/test/"
            multiple :file-list="fileList" :auto-upload="false"
            :on-change="handleFileChange" :on-remove="handleFileRemove">
          <el-button slot="trigger" size="small" type="primary">Select File</el-button>
        </el-upload>
      </div>
      <el-button @click="onClickSubmit">Submit</el-button>

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
      if (typeStr === 'submission') {
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
  },
}
</script>

<style scoped>

</style>

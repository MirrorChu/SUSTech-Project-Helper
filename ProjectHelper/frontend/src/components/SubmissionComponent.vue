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

      <div v-if="identity === 'teacher'">
        <EventGrading>

        </EventGrading>
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
    }
  },
  data () {
    return {
      submissionText: '',
      fileList: [],
      expand: false,
      identity: 'teacher',
    }
  },
  methods: {
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

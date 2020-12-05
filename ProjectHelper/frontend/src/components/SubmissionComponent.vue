<template>
  <div>
    <div>
      <h1>{{ this.$props.data.title }}</h1>
    </div>
    <div>
      {{ this.$props.data.introduction }}
    </div>
    <div>Due: {{ new Date(this.$props.data.due) }}</div>
    <div v-if="this.$props.data.submissionType === 'text'">
      <el-input v-model="this.submissionText" clearable type="textarea" placeholder="Input your submission."></el-input>
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
  </div>
</template>

<script>
export default {
  name: 'SubmissionComponent',
  props: {
    data: {
      required: true,
    },
  },
  data () {
    return {
      submissionText: '',
      fileList: [],
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
  },
}
</script>

<style scoped>

</style>

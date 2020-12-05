<template>
  <el-form>
    <el-form-item label="Title">
      <el-input clearable placeholder="Input your title."></el-input>
    </el-form-item>
    <el-form-item label="Introduction">
      <el-input clearable type="textarea" placeholder="Input your content."></el-input>
    </el-form-item>
    <el-form-item label="Due">
      <el-date-picker
        v-model="due"
        type="datetime"
        placeholder="Due Datetime">
      </el-date-picker>
    </el-form-item>
    <el-form-item label="Submission Type">
      <el-radio-group v-model="submissionType">
        <el-radio label="text">Text</el-radio>
        <el-radio label="file">File</el-radio>
      </el-radio-group>
    </el-form-item>
    <el-form-item>
      <el-button @click="onClickSubmit">Submit</el-button>
    </el-form-item>
  </el-form>
</template>

<script>
export default {
  name: 'NewSubmission',
  data () {
    return {
      title: '',
      introduction: '',
      due: '',
      submissionType: '',
    }
  },
  methods: {
    onClickSubmit () {
      //TODO: Implement submit.
    },
  },
}
</script>

<style scoped>

</style>

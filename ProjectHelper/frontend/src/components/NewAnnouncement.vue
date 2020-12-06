<template>
  <div>
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
    </el-form>
    <el-button>Submit</el-button>
  </div>
</template>

<script>
export default {
  name: 'NewAnnouncement',
  data () {
    return {
      type: '',
      title: '',
      introduction: '',
      due: '',
    }
  },
  methods: {
    onClickSubmit () {
      //  TODO: Implement submission.
    },
  },
  toJson () {
    const event = {}
    event.type = this.type
    event.title = this.title
    event.introduction = this.introduction
    event.due = this.due
    return event
  },
}
</script>

<style scoped>

</style>

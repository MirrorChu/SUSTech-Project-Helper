<template>
  <div>
    <el-form>
      <el-form-item label="Title">
        <el-input clearable
                  placeholder="Input your title."
                  v-model="title">
        </el-input>
      </el-form-item>
      <el-form-item label="Introduction">
        <el-input clearable
                  type="textarea"
                  placeholder="Input your content."
                  v-model="introduction">
        </el-input>
      </el-form-item>
      <el-form-item label="Due">
        <el-date-picker
          v-model="due"
          type="datetime"
          placeholder="Due Datetime">
        </el-date-picker>
      </el-form-item>
    </el-form>
    <el-button @click="onClickSubmit">Submit</el-button>
  </div>
</template>

<script>
export default {
  name: 'NewAnnouncement',
  data () {
    return {
      type: 'Announcement',
      title: '',
      introduction: '',
      due: '',
    }
  },
  methods: {
    onClickSubmit () {
      console.log(this.toJson())
      this.$axios.post('/test/', {jsonObj: this.toJson()}).then(res => {
        console.log('res', res)
      }).catch(err => {
        console.log('err', err)
      })
    },
    toJson () {
      const event = {}
      event.type = 'Announcement'
      event.title = this.title
      event.introduction = this.introduction
      event.due = this.due.getTime()
      return event
    },
  },

}
</script>

<style scoped>

</style>

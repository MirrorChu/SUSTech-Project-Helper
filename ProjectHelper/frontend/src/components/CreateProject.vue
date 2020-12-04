<!--TODO: Change API of file upload. Add data.-->
<template>
  <div>
    <el-form>
      <el-form-item label="Course">
        <el-select v-model="this.newProjectCourse" placeholder="Course">
          <el-option v-for="course in newProjectCourseList" :key="course.value" :label="course.label"
                     :value="course.value"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="Project Name">
        <el-input v-model="newProjectName" placeholer="Project Name" clearable></el-input>
      </el-form-item>
      <el-form-item label="Description">
        <el-input v-model="newProjectDescription" placeholer="Description." clearable type="textarea"></el-input>
      </el-form-item>
      <el-form-item label="Grouping Minimum Number">
        <el-input-number :min="1" label="Min" v-model="minNum"></el-input-number>
      </el-form-item>
      <el-form-item label="Grouping Maximum Number">
        <el-input-number :min="1" label="Max" v-model="maxNum"></el-input-number>
      </el-form-item>
      <el-form-item label="Grouping Deadline">
        <el-date-picker
          v-model="groupingDeadline"
          type="datetime"
          placeholder="选择日期时间"
          align="right"
          :picker-options="pickerOptions">
        </el-date-picker>
      </el-form-item>
      <el-form-item label="Attachment">
        <el-upload
          class="upload-demo"
          ref="upload"
          :data="this.dataBlock"
          action="https://jsonplaceholder.typicode.com/posts/"
          multiple :file-list="fileList" :auto-upload="false"
          :on-change="handleFileChange" :on-remove="handleFileRemove">
          <el-button slot="trigger" size="small" type="primary">Select File</el-button>
        </el-upload>
      </el-form-item>
      <el-button @click="onClickConfirmCreateProject">Create</el-button>
    </el-form>
  </div>
</template>

<script>
export default {
  name: 'CreateProject',
  props: {
    sid: {
      type: String,
      required: true,
    },
    pswd: {
      type: String,
      required: true,
    },
  },
  created () {

  },
  data () {
    return {
      newProjectCourse: '',
      newProjectCourseList: [],
      newProjectName: '',
      newProjectDescription: '',
      minNum: 1,
      maxNum: 2,
      groupingDeadline: '',
      pickerOptions: {
        shortcuts: [
          {
            text: 'Now',
            onClick (picker) {
              picker.$emit('pick', new Date())
            },
          }, {
            text: 'Tomorrow',
            onClick (picker) {
              picker.$emit('pick', new Date + 3600 * 1000 * 24)
            },
          }, {
            text: 'A Week Later',
            onClick (picker) {
              const date = new Date()
              date.setTime(date.getTime() + 3600 * 1000 * 24 * 7)
              picker.$emit('pick', date)
            },
          },
        ],
      },
      fileList: [],
      dataBlock: {},
    }
  },
  methods: {
    onClickConfirmCreateProject () {
      this.dataBlock = {
        'sid': this.sid,
        'pswd': this.pswd,
        'newProjectCourse': this.newProjectCourse,
        'newProjectName': this.newProjectName,
        'newProjectDescription': this.newProjectDescription,
        'groupingMaximum': this.maxNum,
        'groupingMinimum': this.minNum,
        'groupingDeadline': this.groupingDeadline.getTime(),
      }
      console.log('dataBlock', this.dataBlock)
      this.submitUpload()
    },
    submitUpload () {
      this.$refs.upload.submit()
    },
    handleFileChange () {

    },
    handleFileRemove (file) {

    },
  },
}
</script>

<style scoped>

</style>

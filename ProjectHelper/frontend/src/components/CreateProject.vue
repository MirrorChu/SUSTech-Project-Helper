<!--TODO: Change API of file upload. Add data.-->
<!--TODO: Here, file upload is necessary. Otherwise, nothing would be uploaded.-->
<template>
  <div>
    <el-form>
      <el-form-item label="Course">
        <el-select v-model="newProjectCourse" placeholder="Course">
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
      <el-form-item label="Grouping Start">
        <el-date-picker
          v-model="groupingStart"
          type="datetime"
          placeholder="Choose Date and Time"
          :picker-options="pickerOptions">
        </el-date-picker>
      </el-form-item>
      <el-form-item label="Grouping Deadline">
        <el-date-picker
          v-model="groupingDeadline"
          type="datetime"
          placeholder="Choose Date and Time"
          :picker-options="pickerOptions">
        </el-date-picker>
      </el-form-item>
      <el-form-item label="Attachment">
        <el-upload
          class="upload-demo"
          ref="upload"
          :data="this.dataBlock"
          action="/api/test/"
          multiple :file-list="fileList" :auto-upload="false"
          :on-change="handleFileChange" :on-remove="handleFileRemove">
          <el-button slot="trigger" size="small" type="primary">Select File</el-button>
        </el-upload>
      </el-form-item>
      <el-form-item label="Students">
        <el-button @click="onClickLoadStudent">{{ loadStudentsLiteral }}</el-button>

        <el-button @click="onClickSelectAll" v-if="this.showSelect">Select All</el-button>
        <el-input clearable placeholer="Manually Search" v-model="this.manuallySearchSid"
                  v-if="this.showSelect"></el-input>
        <el-button v-model="this.showSelect" v-if="this.showSelect">Add</el-button>
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
  },
  created () {

    this.pullCoursesData()
  },
  data () {
    return {
      newProjectCourse: '',
      newProjectCourseList: [],
      newProjectName: '',
      newProjectDescription: '',
      minNum: 1,
      maxNum: 2,
      groupingStart: '',
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
      loadStudentsLiteral: 'Load Students',
      showSelect: false,
      allStudentInCourse: [],
      selectedStudents: [],
      manuallySearchSid: '',
    }
  },
  methods: {
    onClickAdd () {
      //  TODO: Test if manuallySearchSid is valid.
      this.allStudentInCourse.push({value: this.manuallySearchSid, label: this.manuallySearchSid})
    },
    onClickSelectAll () {
      for (const item in this.allStudentInCourse) {
        this.selectedStudents.push({ value: item, label: item })
      }
    },
    onClickLoadStudent () {
      //  TODO: Update the list of all students in course.
      this.showSelect = !this.showSelect
      if (this.showSelect) {

      }
      if (this.showSelect) {
        this.loadStudentsLiteral = 'Cancel'
      } else {
        this.loadStudentsLiteral = 'Load Students'
      }
    },
    onClickConfirmCreateProject () {
      this.dataBlock = {
        'sid': this.sid,
        'newProjectCourse': this.newProjectCourse,
        'newProjectName': this.newProjectName,
        'newProjectDescription': this.newProjectDescription,
        'groupingMaximum': this.maxNum,
        'groupingMinimum': this.minNum,
        'groupingStart': this.groupingStart.getTime(),
        'groupingDeadline': this.groupingDeadline.getTime(),
      }
      console.log('dataBlock', this.dataBlock)
      // this.$refs.upload.submit()
      this.submitUpload()
    },
    submitUpload () {
      this.$refs.upload.submit()
    },
    handleFileChange () {

    },
    handleFileRemove (file) {

    },
    pullCoursesData()
    {
      this.$axios.post('/teacher_get_courses/', {}).then(res => {
        console.log(res.data)
        for (const item in res.data['Data']) {
          const newCourse = {value: res.data['Data'][item], label: res.data['Data'][item]}
          this.newProjectCourseList.push(newCourse)
        }
        console.log(this.newProjectCourseList)
      }).catch(err => {
        console.log('err', err)
      })
    }
  },
}
</script>

<style scoped>

</style>

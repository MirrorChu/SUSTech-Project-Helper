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
            :data="this.dataforfile"
            action="http://127.0.0.1:8080/api/submit_project_file/"
            multiple
            :file-list="fileList"
            :auto-upload="false"
            :on-change="handleFileChange">
          <el-button slot="trigger" size="small" type="primary">Select File</el-button>
        </el-upload>
      </el-form-item>
      <el-form-item label="Students">
        <div>
          <el-button @click="onClickLoadStudent">{{ loadStudentsLiteral }}</el-button>
        </div>
        <div>
          <el-select v-model="selectedStudents" multiple v-if="loadStudentsLiteral === 'Cancel'">
            <el-option v-for="item in allStudentInCourse"
                       :key="item.value"
                       :value="item.value"
                       :label="item.label">
            </el-option>
          </el-select>
          <el-button @click="onClickSelectAll" v-if="this.showSelect">Select All</el-button>
        </div>
        <div>
          <el-input clearable placeholer="Manually Search" v-model="manuallySearchSid"
                    v-if="this.showSelect"></el-input>
          <el-button v-model="this.showSelect" v-if="this.showSelect">Add</el-button>
        </div>
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
      dataBlock: { 'sid': '',
        'newProjectCourse': '',
        'newProjectName': '',
        'newProjectDescription': '',
        'groupingMaximum': '',
        'groupingMinimum': '',
        'groupingStart': '',
        'groupingDeadline': '',
        'idx': '',
      },
      loadStudentsLiteral: 'Show Students',
      showSelect: false,
      allStudentInCourse: [],
      selectedStudents: [],
      manuallySearchSid: '',
      fileCount: 0,
      project_id: '',
      dataforfile: {'project_id': '', 'token': ''},
    }
  },
  methods: {
    onClickAdd () {
      this.allStudentInCourse.push({ value: this.manuallySearchSid, label: this.manuallySearchSid })
    },
    onClickSelectAll () {
      for (const item in this.allStudentInCourse) {
        let duplicate = false
        const toSelect = this.allStudentInCourse[item]['value']
        for (const selectedKey in this.selectedStudents) {
          const selected = this.selectedStudents[selectedKey]
          if (selected === toSelect) {
            duplicate = true
            break
          }
        }
        if (duplicate) {
          continue
        }
        this.selectedStudents.push(toSelect)
      }
    },
    onClickLoadStudent () {
      //  TODO: Update the list of all students in course.
      this.showSelect = !this.showSelect
      this.allStudentInCourse = []
      if (this.showSelect) {
        const dataGram = { course: parseInt(this.newProjectCourse) }
        this.$axios.post('/teacher_get_students_in_course/', dataGram).then(res => {
          console.log('res', res)
          for (const item in res.data['Data']) {
            this.allStudentInCourse.push({ label: item, value: item })
          }
        }).catch(err => {
          console.log('err', err)
        })
      }
      if (this.showSelect) {
        this.loadStudentsLiteral = 'Cancel'
      } else {
        this.loadStudentsLiteral = 'Show Students'
      }
    },
    onClickConfirmCreateProject () {
      this.$axios.post('/send_key/', { 'course': this.newProjectCourse }).then(res => {
        console.log(res)
        const idx = res.data['SendKey']
        const startDate = new Date(this.groupingStart)
        const endDate = new Date(this.groupingDeadline)
        this.dataBlock['sid'] = this.sid
        this.dataBlock['newProjectCourse'] = this.newProjectCourse
        this.dataBlock['newProjectName'] = this.newProjectName
        this.dataBlock['newProjectDescription'] = this.newProjectDescription
        this.dataBlock['groupingMaximum'] = this.maxNum
        this.dataBlock['groupingMinimum'] = this.minNum
        this.dataBlock['groupingStart'] =  startDate.getTime()
        this.dataBlock['groupingDeadline'] =  endDate.getTime()
        this.dataBlock['idx'] = idx
        this.dataBlock['selectedStudents'] = this.selectedStudents
        this.submitUpload()
      }).catch(err => {
        console.log(err, 'err')
      })
    },
    submitUpload () {
      if (this.fileList.length === 0) {
        this.$axios.post('/teacher_create_project/', this.dataBlock).then(res => {
          console.log(res)
        }).catch(err => {
          console.log('err', err)
        })
      }
      else {
        this.dataBlock['token'] = localStorage.getItem('Authorization')
        console.log('create project with files', this.dataBlock)
        this.$axios.post('/teacher_create_project/', this.dataBlock).then(res => {
          console.log(res)
          if (res.data['TeacherCreateProject'] === 'success')
          {
            this.dataforfile['project_id'] = res.data.project_id
            this.dataforfile['token'] = localStorage.getItem('Authorization')
            this.$refs.upload.submit()
          }
        }).catch(err => {
          console.log('err', err)
        })
      }
    },
    handleFileChange (file, fileList) {
      this.fileList = fileList
    },
    handleFileRemove () {
      this.fileCount -= 1
    },
    pullCoursesData () {
      this.$axios.post('/teacher_get_courses/', {}).then(res => {
        console.log(res.data)
        for (const item in res.data['Data']) {
          const newCourse = { value: item, label: res.data['Data'][item] }
          this.newProjectCourseList.push(newCourse)
        }
        console.log(this.newProjectCourseList)
      }).catch(err => {
        console.log('err', err)
      })
    },
    loadstudnetdata()
    {
      // TODO: Update the list of all students in course.
      if (this.newProjectCourse)
      {
        const dataGram = { course: parseInt(this.newProjectCourse) }
        this.$axios.post('/teacher_get_students_in_course/', dataGram).then(res => {
          console.log('res', res)
          for (const item in res.data['Data']) {
            this.allStudentInCourse.push({ label: item, value: item })
          }
        }).catch(err => {
          console.log('err', err)
        })
      }
      else
      {
        this.allStudentInCourse = []
      }
    }
  },
}
</script>

<style scoped>

</style>

<template>
  <el-form>
    <el-form-item label="Title">
      <el-input
          clearable
          v-model="title"
          placeholder="Input your title.">
      </el-input>
    </el-form-item>
    <el-form-item label="Introduction">
      <el-input
          clearable
          type="textarea"
          v-model="introduction"
          placeholder="Input your content."></el-input>
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
<!--        <el-radio label="text">Text</el-radio>-->
        <el-radio label="file">File</el-radio>
      </el-radio-group>
    </el-form-item>


    <el-form-item label="Select Partition">
      <el-select v-model="selectedPartitionList"
                 multiple placeholder="Select Partitions"
                 @change="onSelectPartition">
        <el-option
            v-for="item in partitionList"
            :key="item.value"
            :label="item.label"
            :value="item.value">
        </el-option>
      </el-select>
    </el-form-item>

    <el-form-item label="Select Group">
      <el-select v-model="selectedGroupList" multiple placeholder="Select Partitions">
        <el-option
            v-for="item in groupList"
            :key="item.value"
            :label="item.label"
            :value="item.value">
        </el-option>
      </el-select>
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
      type: '',
      title: '',
      introduction: '',
      due: '',
      submissionType: 'file',
      partitionList: [],
      groupList: [],
      selectedPartitionList: [],
      selectedGroupList: [],
    }
  },
  props: {
    projectId: {
      type: Number,
      required: true,
    },
    courseId: {
      type: Number,
      required: true,
    }
  },
  methods: {
    onClickSubmit () {
      this.$axios.post('/send_key/', {'course': this.courseId}).then(res => {
        console.log(res)
        const event = this.toJson()
        console.log(event)
        const data = {}
        data.project_id = this.$props.projectId
        data.event_title = event.title
        data.event_type = event.eventType
        data.event_detail = event
        console.log('NewSubmission onClickSubmit data', data)
        this.$axios.post('/create_event/', data).then(res => {
          console.log(res)
        }).catch(err => {
          console.log(err)
        })
      }).catch(err => {
        console.log(err)
      })
    },
    toJson () {
      const event = {}
      event.title = this.title
      event.introduction = this.introduction
      event.due = this.due.getTime()
      event.eventType = 'submission'
      event.submissionType = this.submissionType
      // event.selectedPartitionList = this.selectedPartitionList
      event.selectedGroupList = this.selectedGroupList

      // if (this.selectionType === 0 || this.selectionType === '0') {
      //   event.partitionType = 'normal'
      //   for (let idx = 0; idx < this.dynamicValidateForm.domains.length; idx += 1) {
      //     const item = this.dynamicValidateForm.domains[idx]
      //     options.push([item.value, item.volume])
      //   }
      // } else {
      //   event.partitionType = 'timeSlot'
      //   const domains = this.dynamicValidateFormTimeSlot.domains
      //   for (let i = 0; i < domains.length; i += 1) {
      //     let startTime = domains[i].timeSlotSelectionStart.getTime()
      //     const endTime = domains[i].timeSlotSelectionEnd.getTime()
      //     const num = domains[i].timeSlotNum
      //     const length = Math.floor((endTime - startTime) / num)
      //     for (let idx = 0; idx < num; idx += 1) {
      //       options.push([startTime, startTime + length - 1, num])
      //       startTime += length
      //     }
      //   }
      // }

      return event
    },
    onSelectPartition (selected) {
      //TODO: Partition influences selected group.
      console.log(selected)
    },
  },
}
</script>

<style scoped>

</style>

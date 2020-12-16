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
        <el-radio label="text">Text</el-radio>
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
      submissionType: '',
      partitionList: [],
      groupList: [],
      selectedPartitionList: [],
      selectedGroupList: [],
    }
  },
  methods: {
    onClickSubmit () {
      console.log(this.toJson())
      //TODO: Implement submit.
    },
    toJson () {
      const event = {}
      event.type = this.type
      event.title = this.title
      event.introduction = this.introduction
      event.due = this.due.getTime()
      event.submissionType = this.submissionType
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

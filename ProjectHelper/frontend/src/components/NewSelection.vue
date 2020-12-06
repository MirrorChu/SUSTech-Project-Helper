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
      <el-form-item label="Selection Type">
        <el-radio-group v-model="selectionType">
          <el-radio label="0">Normal</el-radio>
          <el-radio label="1">Timeslot</el-radio>
        </el-radio-group>
      </el-form-item>
      <el-form-item v-if="selectionType === 0 || selectionType === '0'">
        <el-form :model="dynamicValidateForm" ref="dynamicValidateForm">
          <el-form-item
            v-for="(value, index) in dynamicValidateForm.domains"
            :label="'Option ' + index"
            :key="value.key"
            :prop="'domains.' + index + '.value'">
            <el-input v-model="value.value"></el-input>
            <el-button @click.prevent="removeDomain(value)">Remove</el-button>
          </el-form-item>
          <el-form-item>
            <el-button @click="addDomain">New Option</el-button>
            <el-button @click="resetForm('dynamicValidateForm')">Reset</el-button>
          </el-form-item>
        </el-form>
      </el-form-item>
      <el-form-item v-else-if="selectionType === 1 || selectionType === '1'">
        <el-form>
          <el-form-item label="Start">
            <el-date-picker
              v-model="timeSlotSelectionStart"
              type="datetime"
              placeholder="Due Datetime">
            </el-date-picker>
          </el-form-item>
          <el-form-item label="End">
            <el-date-picker
              v-model="timeSlotSelectionEnd"
              type="datetime"
              placeholder="Due Datetime">
            </el-date-picker>
          </el-form-item>
          <el-form-item label="Number">
            <el-input-number v-model="timeSlotNum" :min="1" label="number"></el-input-number>
          </el-form-item>
        </el-form>
      </el-form-item>
      <el-form-item>
        <el-button @click="onClickSubmit">Submit</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
export default {
  name: 'NewSelection',
  data () {
    return {
      type: '',
      title: '',
      introduction: '',
      due: '',
      selectionType: 0,
      selectionLimit: 1,
      options: [],
      newOption: '',
      dynamicValidateForm: {
        domains: [
          {
            value: '',
          }],
        email: '',
      },
      timeSlotSelectionStart: '',
      timeSlotSelectionEnd: '',
      timeSlotNum: 0,
    }
  },
  methods: {
    onClickSubmit () {
      //TODO: Implement submit.
    },
    submitForm (formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          alert('submit!')
        } else {
          console.log('error submit!!')
          return false
        }
      })
    },
    resetForm (formName) {
      this.$refs[formName].resetFields()
    },
    removeDomain (item) {
      const index = this.dynamicValidateForm.domains.indexOf(item)
      if (index !== -1) {
        this.dynamicValidateForm.domains.splice(index, 1)
      }
    },
    addDomain () {
      this.dynamicValidateForm.domains.push({
        value: '',
        key: Date.now(),
      })
    },
    toJson () {
      const event = {}
      event.type = this.type
      event.title = this.title
      event.introduction = this.introduction
      event.due = this.due
      event.selectionType = this.selectionType
      event.selectionLimit = this.selectionLimit
      event.options = this.options
      return event
    },
  },
}
</script>

<style scoped>

</style>

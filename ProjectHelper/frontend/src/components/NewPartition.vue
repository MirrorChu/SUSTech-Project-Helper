<template>
  <div>
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
            <el-input-number v-model="value.volume" :min="1" label="Volume"></el-input-number>
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

          <el-form-item label="Slot Volume">
            <el-input-number v-model="timeSlotVolume" label="slot volume"></el-input-number>
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
  name: 'NewPartition',
  data () {
    return {
      type: '',
      title: '',
      introduction: '',
      due: '',
      selectionLimit: 1,
      options: [],
      selectionType: 0,
      newOption: '',
      dynamicValidateForm: {
        domains: [
          {
            value: '',
            volume: 1,
          }],
        email: '',
      },
      timeSlotSelectionStart: '',
      timeSlotSelectionEnd: '',
      timeSlotNum: 0,
      timeSlotVolume: 0,
    }
  },
  methods: {
    onClickSubmit () {
      console.log(this.toJson())
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
      const options = []
      const event = {}
      if (this.selectionType === 0 || this.selectionType === '0') {
        let idx = 0
        while (idx < this.dynamicValidateForm.domains.length) {
          const item = this.dynamicValidateForm.domains[idx]
          options.push([item.value, item.volume])
          idx += 1
        }
      }
      else {
        let startTime = this.timeSlotSelectionStart.getTime();
        const endTime = this.timeSlotSelectionEnd.getTime();
        const num = this.timeSlotNum;
        const length = Math.floor((endTime - startTime) / num)
        let idx = 0
        while (idx < length) {
          options.push([startTime, startTime + length - 1])
          startTime += length
          idx += 1
        }
        event.timeSlotLength = length
        event.timeSlotVolume = this.timeSlotVolume
      }
      event.type = 'Selection'
      event.title = this.title
      event.introduction = this.introduction
      event.due = this.due.getTime()
      event.selectionType = this.selectionType
      event.selectionLimit = this.selectionLimit
      event.options = options
      return event
    },
  },
}
</script>

<style scoped>

</style>

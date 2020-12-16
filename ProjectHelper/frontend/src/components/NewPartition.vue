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

      <el-form-item label="Partition Type">
        <el-radio-group v-model="selectionType">
          <el-radio label="0">Normal</el-radio>
          <el-radio label="1">Timeslot</el-radio>
        </el-radio-group>
      </el-form-item>

      <!--      normal partition.-->
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

      <!--      timeSlot partition.-->
      <el-form-item v-else-if="selectionType === 1 || selectionType === '1'">
        <el-form :model="dynamicValidateFormTimeSlot" ref="dynamicValidateForm">

          <el-form-item
              v-for="(value, index) in dynamicValidateFormTimeSlot.domains"
              :label="'Time Interval ' + index"
              :key="value.key"
              :prop="'domains.' + index + '.value'">

            <div>Start</div>
            <el-date-picker
                v-model="value.timeSlotSelectionStart"
                type="datetime"
                placeholder="Due Datetime">
            </el-date-picker>

            <div>End</div>
            <el-date-picker
                v-model="value.timeSlotSelectionEnd"
                type="datetime"
                placeholder="Due Datetime">
            </el-date-picker>

            <div>Number</div>
            <el-input-number v-model="value.timeSlotNum" :min="1" label="number"></el-input-number>

            <div>Slot Volume</div>
            <el-input-number v-model="value.timeSlotVolume" label="slot volume"></el-input-number>

            <el-button @click.prevent="removeDomain(value)">Remove</el-button>


          </el-form-item>

          <!--          <el-form-item label="Start">-->
          <!--            <el-date-picker-->
          <!--                v-model="timeSlotSelectionStart"-->
          <!--                type="datetime"-->
          <!--                placeholder="Due Datetime">-->
          <!--            </el-date-picker>-->
          <!--          </el-form-item>-->

          <!--          <el-form-item label="End">-->
          <!--            <el-date-picker-->
          <!--                v-model="timeSlotSelectionEnd"-->
          <!--                type="datetime"-->
          <!--                placeholder="Due Datetime">-->
          <!--            </el-date-picker>-->
          <!--          </el-form-item>-->

          <!--          <el-form-item label="Number">-->
          <!--            <el-input-number v-model="timeSlotNum" :min="1" label="number"></el-input-number>-->
          <!--          </el-form-item>-->

          <!--          <el-form-item label="Slot Volume">-->
          <!--            <el-input-number v-model="timeSlotVolume" label="slot volume"></el-input-number>-->
          <!--          </el-form-item>-->

          <el-form-item>
            <el-button @click="addDomain">New Option</el-button>
            <el-button @click="resetForm">Reset</el-button>
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
        domains: [],
      },
      dynamicValidateFormTimeSlot: {
        domains: [],
      },
      timeSlotSelectionStart: '',
      timeSlotSelectionEnd: '',
      timeSlotNum: 0,
      timeSlotVolume: 0,
    }
  },
  props: {
    projectId: {
      type: Number,
      required: true,
    },
  },
  methods: {
    //Why is this not working?
    onClickPartitionType () {
      console.log('onClickPartitionType')
      this.dynamicValidateForm.domains = []
      this.dynamicValidateFormTimeSlot.domains = []
    },
    onClickSubmit () {
      const event = this.toJson()
      console.log(event)
      const data = {}
      data.project_id = this.$props.projectId
      data.event_title = event.title
      data.event_type = event.eventType
      data.event_detail = event
      console.log('NewPartition onClickSubmit data', data)
      this.$axios.post('/create_event/', data).then(res => {
        console.log('NewPartition onClickSubmit /create_event/ res', res)
      }).catch(err => {
        console.log('NewPartition onClickSubmit /create_event/ err', err)
      })
    },
    resetForm () {
      this.dynamicValidateForm.domains = []
      this.dynamicValidateFormTimeSlot.domains = []
    },
    removeDomain (item) {
      if (this.selectionType === 0 || this.selectionType === '0') {
        const index = this.dynamicValidateForm.domains.indexOf(item)
        if (index !== -1) {
          this.dynamicValidateForm.domains.splice(index, 1)
        }
      }
      else {
        const index = this.dynamicValidateFormTimeSlot.domains.indexOf(item)
        if (index !== -1) {
          this.dynamicValidateFormTimeSlot.domains.splice(index, 1)
        }
      }

    },
    addDomain () {
      console.log(this.selectionType)
      if (this.selectionType === 0 || this.selectionType === '0') {
        this.dynamicValidateForm.domains.push({
          value: '',
          key: Date.now(),
        })
      }
      else {
        this.dynamicValidateFormTimeSlot.domains.push({
          value: '',
          key: Date.now(),
        })
      }
    },
    toJson () {
      const options = []
      const event = {}
      event.eventType = 'partition'
      if (this.selectionType === 0 || this.selectionType === '0') {
        event.partitionType = 'normal'
        for (let idx = 0; idx < this.dynamicValidateForm.domains.length; idx += 1) {
          const item = this.dynamicValidateForm.domains[idx]
          options.push([item.value, item.volume])
        }
      } else {
        event.partitionType = 'timeSlot'
        const domains = this.dynamicValidateFormTimeSlot.domains
        for (let i = 0; i < domains.length; i += 1) {
          let startTime = domains[i].timeSlotSelectionStart.getTime()
          const endTime = domains[i].timeSlotSelectionEnd.getTime()
          const num = domains[i].timeSlotNum
          const length = Math.floor((endTime - startTime) / num)
          for (let idx = 0; idx < num; idx += 1) {
            options.push([startTime, startTime + length - 1, num])
            startTime += length
          }
        }
      }
      event.title = this.title
      event.introduction = this.introduction
      event.due = this.due.getTime()
      event.selectionLimit = this.selectionLimit
      event.options = options
      return event
    },
  },
}
</script>

<style scoped>

</style>

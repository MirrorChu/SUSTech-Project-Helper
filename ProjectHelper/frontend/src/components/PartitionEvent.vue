<template>
  <div>
    <div>
      <div><h3>{{ this.$props.eventTitle }}</h3></div>
      <div v-if="!expand">
        <el-button @click="onClickExpand">Expand</el-button>
      </div>

      <div v-if="expand">
        <div>
          <el-button @click="onClickExpand">Close</el-button>
        </div>
        <div>{{ this.eventObj['data']['introduction'] }}</div>
        <div>Due: {{ new Date(this.$props.data.due) }}</div>
        <div>Limit of Selections: {{this.eventObj.data.selectionLimit}}</div>
        <div>
          <el-select v-model="selected"
                     :multiple="this.eventObj.data.selectionLimit > 1"
                     :multiple-limit="this.eventObj.data.selectionLimit"
                     placeholder="Please select.">
            <el-option v-for="(item, index) in this.eventObj.data.options" :key="item.value"
                       :label="getLabelAndNumberFromItem(item)" :value="index">
            </el-option>
          </el-select>
        </div>
        <el-button @click="onClickSubmit">Submit</el-button>

        <div v-if="privileges['teach'] === 1">
          <div>
            <el-button @click="onClickDeleteEvent">Delete Event</el-button>
          </div>

          <div>
            <EventGrading v-bind:submissionDetail="submissionDetail"></EventGrading>
          </div>

        </div>

      </div>

    </div>
  </div>
</template>

<script>
import EventGrading from './EventGrading'

export default {
  name: 'PartitionEvent',
  components: { EventGrading },
  props: {
    data: {
      required: true,
    },
    courseId: {
      required: true,
    },
    eventId: {
      required: true,
    },
    eventTitle: {
      required: true,
    }
  },
  data () {
    return {
      selected: [],
      expand: false,
      identity: 'teacher',
      privileges: {},
      eventObj: {},
      submissionDetail: [],
    }
  },
  created () {
    this.$axios.post('/get_event_detail/', {'event_id': this.$props.eventId}).then(res => {
      console.log('get event detail', res.data)
      this.submissionDetail = res.data['Data']['data']
      const eventEle = res.data['Data']
      const typeStr = eventEle['event_type']
      if (typeStr === 'partition') {
        this.eventObj['type'] = 'PartitionEvent'
        this.eventObj['data'] = {}
        this.eventObj['data']['type'] = 'PartitionEvent'
        this.eventObj['data']['selectionLimit'] = eventEle['event_detail']['selectionLimit']
        this.eventObj['partitionType'] = eventEle['event_detail']['partitionType']
        this.eventObj['data']['partitionType'] = eventEle['event_detail']['partitionType']
        this.eventObj['data']['options'] = []
        if (this.eventObj['data']['partitionType'] === 'normal') {
          for (let j = 0; j < eventEle['event_detail']['options'].length; j += 1) {
            const option = eventEle['event_detail']['options'][j]
            this.eventObj['data']['options'].push({'label': option[0], 'value': j, 'limit': option[1]})
          }
        }
        else {
          for (let j = 0; j < eventEle['event_detail']['options'].length; j += 1) {
            const option = eventEle['event_detail']['options'][j]
            this.eventObj['data']['options'].push(this.generateTimeSlotPartitionOptions(option))
          }
        }
      }
      this.eventObj['data']['title'] = eventEle['event_title']
      this.eventObj['data']['introduction'] = eventEle['introduction']
      this.eventObj['data']['due'] = eventEle['event_detail']['due']
      this.eventObj['publisher'] = eventEle['publisher']
      this.eventObj['id'] = this.$props.eventId

      this.$axios.post('/get_privilege_list/', {'course_id': this.$props.courseId}).then(res => {
        this.privileges = res.data['Data']
      }).catch(err => {
        console.log(err)
      })
    }).catch(err => {
      console.log(err)
    })
  },
  methods: {
    generateTimeSlotPartitionOptions(option) {
      const label = new Date(option[0]) + ' to ' + new Date(option[1])
      const value = label
      const limit = option[2]
      return {'label': label, 'value': value, 'limit': limit}
    },
    onClickDeleteEvent() {
      this.$axios.post('/delete_event/', {'event_id': this.eventObj['id']}).then(res => {
        alert('Delete Event ' + res.data['DeleteEvent'])
      }).catch(err => {
        console.log(err)
      })
    },
    onClickSubmit () {
      //  TODO: Implement submission.
      const selected = this.selected
      this.$axios.post('/submit_event/', {'event_id': this.$props.eventId, 'selected': selected}).then(res => {
        console.log(res)
      }).catch(err => {
        console.log(err)
      })
    },
    getLabelAndNumberFromItem (item) {
      return item.label + ': ' + item.limit + ' remaining'
    },
    onClickExpand () {
      this.expand = !this.expand
    },
  },
}
</script>

<style scoped>

</style>

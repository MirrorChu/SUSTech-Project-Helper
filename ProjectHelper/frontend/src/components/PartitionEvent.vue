<template>
  <div>
    <div>
      <div><h3>{{ this.$props.data.title }}</h3></div>
      <div v-if="!expand">
        <el-button @click="onClickExpand">Expand</el-button>
      </div>

      <div v-if="expand">
        <div>
          <el-button @click="onClickExpand">Close</el-button>
        </div>
        <div>{{ this.$props.data.introduction }}</div>
        <div>Due: {{ new Date(this.$props.data.due) }}</div>
        <div>
          <el-select v-model="selected" :multiple="this.$props.data.selectionLimit > 1" placeholder="Please select.">
            <el-option v-for="item in this.$props.data.options" :key="item.value"
                       :label="getLabelAndNumberFromItem(item)" :value="item.value">
            </el-option>
          </el-select>
        </div>
        <el-button @click="onClickSubmit">Submit</el-button>

        <div v-if="privileges['teach'] === 1">
          <div>
            <el-button @click="onClickDeleteEvent">Delete Event</el-button>
          </div>

          <div>
            <EventGrading></EventGrading>
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
    }
  },
  data () {
    return {
      selected: [],
      expand: false,
      identity: 'teacher',
      privileges: {},
      eventDetail: {},
    }
  },
  created () {
    this.$axios.post('/get_privilege_list/', {'course_id': this.$props.courseId}).then(res => {
      this.privileges = res.data['Data']
    }).catch(err => {
      console.log(err)
    })
  },
  methods: {
    onClickDeleteEvent() {
      // this.$axios.post('/delete_event/', {'event_id': })
    },
    onClickSubmit () {
      //  TODO: Implement submission.
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

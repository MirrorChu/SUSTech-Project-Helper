<template>
  <div>
    <div>
      <h3>{{ this.$props.data.title }}</h3>
      <div v-if="!expand">
        <el-button @click="onClickExpand">Expand</el-button>
      </div>
    </div>

    <div v-if="expand">
      <div>
        <el-button @click="onClickExpand">Close</el-button>
      </div>
      <div>{{ this.$props.data.introduction }}</div>

      <div>Due: {{ new Date(this.$props.data.due) }}</div>

      <div>
        <el-select v-model="selected" :multiple="this.$props.data.selectionLimit > 1"
                   :multiple-limit="this.$props.data.selectionLimit" placeholder="Please select.">
          <el-option v-for="item in this.$props.data.options" :key="item.value" :label="item.label" :value="item.value">
          </el-option>
        </el-select>
      </div>
      <el-button @click="onClickSubmit">Submit</el-button>

      <div v-if="identity === 'teacher'">
        <EventGrading>

        </EventGrading>
      </div>

    </div>

  </div>
</template>

<script>
import EventGrading from './EventGrading'

export default {
  name: 'SelectionComponent',
  components: {EventGrading},
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
    }
  },
  methods: {
    getResult () {
      return this.selected
    },
    onClickSubmit () {
      //TODO: Implement event submission.
    },
    onClickExpand () {
      this.expand = !this.expand
    },
  },
}
</script>

<style scoped>

</style>

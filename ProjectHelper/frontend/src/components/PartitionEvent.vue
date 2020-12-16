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

        <div v-if="identity === 'teacher'">
          <EventGrading>

          </EventGrading>
        </div>

      </div>

    </div>
  </div>
</template>

<script>
export default {
  name: 'PartitionEvent',
  props: {
    data: {
      required: true,
    },
  },
  data () {
    return {
      selected: [],
      expand: false,
      identity: 'teacher',
    }
  },
  methods: {
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

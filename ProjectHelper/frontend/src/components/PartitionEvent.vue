<template>
  <div>
    <div>
      <div><h1>{{ this.$props.data.title }}</h1></div>
      <div>{{ this.$props.data.introduction }}</div>
      <div>
        <el-select v-model="selected" :multiple="this.$props.data.selectionLimit > 1" placeholder="Please select.">
          <el-option v-for="item in this.$props.data.options" :key="item.value"
                     :label="getLabelAndNumberFromItem(item)" :value="item.value">
          </el-option>
        </el-select>
      </div>
      <el-button @click="onClickSubmit">Submit</el-button>
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
    }
  },
  methods: {
    onClickSubmit () {
      //  TODO: Implement submission.
    },
    getLabelAndNumberFromItem (item) {
      return item.label + ': ' + item.limit + ' remaining'
    },
  },
}
</script>

<style scoped>

</style>

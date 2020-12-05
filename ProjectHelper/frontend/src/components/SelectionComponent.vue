<template>
  <div>
    <div><h3>{{ this.$props.data.title }}</h3></div>
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
  </div>
</template>

<script>
export default {
  name: 'SelectionComponent',
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
    getResult () {
      return this.selected
    },
    onClickSubmit () {
      //TODO: Implement event submission.
    },
  },
}
</script>

<style scoped>

</style>

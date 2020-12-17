<template>
  <div>
    <div>
      <h3>
        {{ this.$props.data.title }}
      </h3>
      <div v-if="!expand">
        <el-button @click="onClickExpand">Expand</el-button>
      </div>
    </div>
    <div v-if="expand">
      <div>
        <el-button @click="onClickExpand">Close</el-button>
      </div>
      {{ this.$props.data.introduction }}
      <div>Due: {{ new Date(this.$props.data.due) }}</div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AnnouncementComponent',
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
      expand: false,
      eventDetail: {},
    }
  },
  methods: {
    getResult () {
      return null
    },
    onClickExpand () {
      this.expand = !this.expand
    },
  },
}
</script>

<style scoped>

</style>

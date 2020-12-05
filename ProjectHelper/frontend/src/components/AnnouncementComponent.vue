<template>
  <div>
    <div>
      {{ this.$props.data.title }}
    </div>
    <div>
      {{ this.$props.data.introduction }}
    </div>
    <div>Due: {{ new Date(this.$props.data.due) }}</div>
  </div>
</template>

<script>
export default {
  name: 'AnnouncementComponent',
  props: {
    data: {
      required: true,
    },
  },
  methods: {
    getResult () {
      return null
    },
  },
}
</script>

<style scoped>

</style>

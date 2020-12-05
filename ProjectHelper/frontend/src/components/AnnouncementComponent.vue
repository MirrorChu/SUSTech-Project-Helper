<template>
  <div>
    <div>
      <h3>
        {{ this.$props.data.title }}
      </h3>
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

<template>
  <div>
    <h1>
      {{ this.$props.data.title }}
    </h1>
    {{ this.$props.data.content }}
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

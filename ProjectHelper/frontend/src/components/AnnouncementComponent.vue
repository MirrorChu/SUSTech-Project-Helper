<template>
  <div>
    <div>
      <h3>
        {{ this.title }}
      </h3>

      <div>
        <el-button @click="onClickExpand">{{this.mi}}</el-button>
      </div>
    </div>

    <div v-if="expand">

      {{ this.introduction }}<br>
      <div>Due: {{ new Date(this.due) }}</div>

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
      introduction: '',
      due: '',
      title: '',
      mi: 'Expand',
    }
  },
  created() {
    this.$axios.post('/get_event_detail/', {'event_id': this.$props.eventId}).then(res => {
      console.log(res);
      this.title = res.data['Data']['event_detail']['title']
      this.due = res.data['Data']['event_detail']['due']
      this.introduction = res.data.Data['introduction']
    }).catch(err => {
      console.log(err);
    });
  },
  methods: {
    getResult () {
      return null
    },
    onClickExpand () {
      if (this.expand)
      {
        this.mi = 'Expand'
      }
      else
      {
        this.mi = 'Close'
      }
      this.expand = !this.expand
    },
  },
}
</script>

<style scoped>

</style>

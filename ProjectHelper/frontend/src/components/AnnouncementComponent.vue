<template>
  <div>
    <div>
      <h3>
        {{ this.title }}
      </h3>

      <div>
        <el-button @click="onClickExpand">{{this.expand ? "Close" : "Expand"}}</el-button>
      </div>
    </div>

    <div v-if="expand">

      {{ this.introduction }}<br>
      <div>Due: {{ new Date(this.due) }}</div>
      <div><el-button @click="onClickDeleteEvent">Delete Event</el-button></div>
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
      this.expand = !this.expand
    },
    onClickDeleteEvent() {
      this.$axios.post('/delete_event/', {
        'event_id': this.$props.eventId
      }).then(res => {
        alert('Delete Event ' + res.data['DeleteEvent']);
        this.$parent.$parent.pullData()
      }).catch(err => {
        console.log(err);
      });
    },
  },
}
</script>

<style scoped>

</style>

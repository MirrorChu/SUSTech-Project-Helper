<template>
  <div>
    <div>
      <h3>
        {{ this.title }}
      </h3>

      <div>
        <el-button @click="onClickExpand">{{ this.expand ? 'Close' : 'Expand' }}</el-button>
      </div>
    </div>

    <div v-if="expand">
      <el-button @click="edit = !edit">{{ edit ? 'Cancel' : 'edit' }}</el-button>
      <div v-if="!edit">
        {{ this.introduction }}<br>
        <div>Due: {{ new Date(this.due) }}</div>
        <div v-for="(item, index) in eventDetail['file_name']">
          <el-link :href="generateFileUrl(eventDetail['file_id'][index])">{{ item }}</el-link>
        </div>
        <div>
          <el-button @click="onClickDeleteEvent">Delete Event</el-button>
        </div>
      </div>
      <div v-else>
        <el-form>
          <el-form-item label="introduction">
            <el-input v-model="introduction" type="textarea"></el-input>
          </el-form-item>
          <el-form-item label="Due">
            <br>
            <el-date-picker
                v-model="this.dueDatetime"
                type="datetime"
                placeholder="Due Datetime">
            </el-date-picker>
          </el-form-item>
          <div>
            <el-button @click="onClickUpdateEvent">Update</el-button>
          </div>

          <el-form-item label="File List">
            <br>
            <div v-for="(item, index) in eventDetail['file_name']">
              <el-link :href="generateFileUrl(eventDetail['file_id'][index])">{{ item }}</el-link>
              <el-button icon="el-icon-delete" @click="onClickDeleteEventFile(eventDetail['file_id'][index])">
              </el-button>
            </div>
          </el-form-item>
          <el-form-item label="Attachment">
            <el-upload
                class="upload-demo"
                drag
                :data="this.announcementData"
                ref="upload"
                :auto-upload="true"
                :on-success="onUploadFileSuccess"
                action="http://127.0.0.1:8000/submit_event_file/">
              <i class="el-icon-upload"></i>
              <div class="el-upload__text">Drag file here, or <em>click to upload</em>.</div>
            </el-upload>
          </el-form-item>
        </el-form>
      </div>

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
    },
  },
  data() {
    return {
      expand: false,
      eventDetail: {},
      introduction: '',
      due: '',
      title: '',
      edit: false,
      dueDatetime: new Date(),
      announcementData: {},
    };
  },
  created() {
    this.edit = false;
    this.announcementData['event_id'] = this.eventId;
    this.announcementData['token'] = localStorage.getItem('Authorization');
    this.pullData();
  },
  methods: {
    getResult() {
      return null;
    },
    pullData() {
      this.$axios.post('/get_event_detail/', {'event_id': this.$props.eventId}).then(res => {
        console.log(res);
        this.eventDetail = res.data['Data'];
        this.title = res.data['Data']['event_detail']['title'];
        this.due = res.data['Data']['event_detail']['due'];
        this.introduction = res.data.Data['introduction'];
      }).catch(err => {
        console.log(err);
      });
    },
    onClickExpand() {
      this.expand = !this.expand;
      this.edit = false;
    },
    onClickDeleteEvent() {
      this.$axios.post('/delete_event/', {
        'event_id': this.$props.eventId,
      }).then(res => {
        alert('Delete Event ' + res.data['DeleteEvent']);
        this.$parent.$parent.pullData();
      }).catch(err => {
        console.log(err);
      });
    },
    generateFileUrl(id) {
      return 'http://127.0.0.1:8000/download_event_file?token='
          + localStorage.getItem('Authorization')
          + '&file_id='
          + id.toString();
    },
    onClickDeleteEventFile(id) {
      this.$axios.post('/delete_event_file/', {'file_id': id}).then(res => {
        console.log(res);
        this.$parent.$parent.pullData();
        this.pullData();
      }).catch(err => {
        console.log(err);
      });
    },
    onUploadFileSuccess(response, file, fileList) {
      console.log('upload success');
      console.log(response);
      this.$parent.$parent.pullData();
      this.pullData();
    },
    onClickUpdateEvent() {
      const data = {
        'introduction': this.introduction,
        'due': this.dueDatetime.getTime(),
        'event_id': this.eventId,
      };
      this.$axios.post('/change_event/', data).then(res => {
        console.log(res);
        this.$parent.$parent.pullData();
        this.pullData();
      }).catch(err => {
        console.log(err);
      });
    },
  },
};
</script>

<style scoped>

</style>

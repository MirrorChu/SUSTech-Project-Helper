<template>
  <div>
    <div>
      <h2 align="center">
        {{ this.title }}
      </h2>

      <div>
        <div style="float: left;margin-left: 175px"><el-button @click="onClickExpand">{{ this.expand ? 'Close' : 'Expand' }}</el-button></div>
        <div v-if="this.privileges && this.privileges['eventEdit']" style="float: left;padding-left: 15px;padding-bottom: 20px">
        <el-button @click="onClickDeleteEvent">Delete Event</el-button>
      </div>
      </div>
    </div>
    <br>
    <div v-if="expand">
      <div v-if="!edit">
        <el-row></el-row>
        <h3 style="font-family: Verdana, serif;">Introduction: </h3>
        <div>{{ this.introduction }}</div>
        <h3 style="font-family: Verdana, serif;">Due time: </h3>
        <div>{{ new Date(this.due) }}</div>
        <h3 style="font-family: Verdana, serif;">Attachments: </h3>
        <div v-if="this.eventDetail['file_name'] && this.eventDetail['file_name'].length !== 0">
          <div v-for="(item, index) in eventDetail['file_name']">
            <el-link :href="generateFileUrl(eventDetail['file_id'][index])">{{ item }}</el-link>
          </div>
        </div>
        <div v-else>No Attachment</div>
      </div>
      <div v-else>
        <el-form>
          <el-row></el-row>
          <h3 style="font-family: Verdana, serif;">Introduction: </h3>
          <el-form-item label="">
            <el-input v-model="introduction" type="textarea"></el-input>
          </el-form-item>
          <h3 style="font-family: Verdana, serif;">Due time: </h3>
          <el-form-item label="">
            <el-date-picker
                v-model="this.dueDatetime"
                type="datetime"
                placeholder="Due Datetime">
            </el-date-picker>
          </el-form-item>
          <div>
            <el-button @click="onClickUpdateEvent">Update</el-button>
          </div>
          <h3 style="font-family: Verdana, serif;">File List: </h3>
          <el-form-item label="">
            <div v-if="this.eventDetail['file_name'] && this.eventDetail['file_name'].length !== 0">
              <div v-for="(item, index) in eventDetail['file_name']">
                <el-link :href="generateFileUrl(eventDetail['file_id'][index])">{{ item }}</el-link>
                <el-button icon="el-icon-delete" @click="onClickDeleteEventFile(eventDetail['file_id'][index])">
                </el-button>
              </div>
            </div>
            <div v-else>No file</div>
          </el-form-item>
          <h3 style="font-family: Verdana, serif;">Attachment: </h3>
          <el-form-item label="">
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
        <el-button @click="edit = !edit">{{ edit ? 'Cancel' : 'Edit' }}</el-button>
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
      privileges: {},
    };
  },
  created() {
    this.edit = false;
    this.announcementData['event_id'] = this.eventId;
    this.announcementData['token'] = localStorage.getItem('Authorization');
    this.$axios.post('/get_privilege_list/', {'course_id': this.$props.courseId}).then(res => {
      console.log(res)
      this.privileges = res.data['Data'];
      this.pullData();
    }).catch(err => {
      console.log(err)
    })
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
        this.$message.success('Delete Event ' + res.data['DeleteEvent']);
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

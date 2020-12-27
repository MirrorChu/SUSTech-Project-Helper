<template>
  <div>
    <div>
      <el-form>
        <el-form-item label="Title">
          <el-input clearable
                    placeholder="Input your title."
                    v-model="title">
          </el-input>
        </el-form-item>

        <el-form-item label="Introduction">
          <el-input clearable
                    type="textarea"
                    placeholder="Input your content."
                    v-model="introduction">
          </el-input>
        </el-form-item>

        <el-form-item label="Due">
          <el-row style="margin:0px"></el-row>
          <el-date-picker
              v-model="due"
              type="datetime"
              placeholder="Due Datetime">
          </el-date-picker>
        </el-form-item>

        <el-form-item label="Attachment"><br/>
          <el-upload
              class="upload-demo"
              drag
              multiple
              :data="this.announcementData"
              ref="upload"
              action="http://127.0.0.1:8000/submit_event_file/"
              :file-list="fileList"
              :auto-upload="false"
              :on-change="handleFileChange">
            <i class="el-icon-upload"></i>
            <div class="el-upload__text">Drag file here, or <em>click to upload</em>.</div>
          </el-upload>
        </el-form-item>

        <el-form-item label="Select Partition">
          <el-row style="margin:0px"></el-row>
          <el-select v-model="selectedPartitionList"
                     multiple placeholder="Select Partitions">
            <el-option
                v-for="item in this.$props.partitionList"
                :key="item.key"
                :label="item.label"
                :value="item.value">
            </el-option>
          </el-select>
        </el-form-item>

      </el-form>
    </div>
    <el-row></el-row>
    <el-button @click="onClickSubmit">Submit</el-button>
  </div>
</template>

<script>
export default {
  name: 'NewAnnouncement',
  props: {
    partitionList: {
      required: true,
    },
    courseId: {
      type: Number,
      required: true,
    },
    projectId: {
      type: Number,
      required: true,
    },
  },
  data() {
    return {
      type: 'Announcement',
      title: '',
      introduction: '',
      due: '',
      eventId: '',
      groupList: [],
      selectedPartitionList: [],
      selectedGroupList: [],
      fileList: [],
      announcementData: {'token': '', 'event_id': ''},
    };
  },
  created() {

  },
  methods: {
    handleFileChange(file, fileList) {
      this.fileList = fileList;
    },
    onClickSubmit() {
      this.$axios.post('/send_key/', {'course': this.$props.courseId}).then(res => {
        console.log(res);
        const event = this.toJson();
        const data = {};
        data.project_id = this.$props.projectId;
        data.event_title = event.title;
        data.event_type = event.eventType;
        data.event_detail = event;
        data.key = res.data['SendKey'];
        this.$axios.post('/create_event/', data).then(res => {
          console.log('res', res);
          if (res.data['CreateEvent'] === 'success' && this.fileList.length !== 0) {
            this.announcementData['event_id'] = res.data.Event_id;
            this.announcementData['token'] = localStorage.getItem('Authorization');
            this.$refs.upload.submit();
          }
          this.$parent.$parent.$parent.$parent.$parent.pullData();
          this.$parent.$parent.$parent.expand = false;
          this.$message.success('Create success')
        }).catch(err => {
          console.log('err', err);
        });
      }).catch(err => {
        console.log(err);
      });
    },
    toJson() {
      const event = {};
      event.eventType = 'AnnouncementComponent';
      event.title = this.title;
      event.introduction = this.introduction;
      event.due = this.due.getTime();
      event.selectedPartitionList = this.selectedPartitionList;
      return event;
    },
    // onSelectPartition(selected) {
    //   //TODO: Partition influences selected group.
    //   console.log(selected);
    // },
  },

};
</script>

<style scoped>
.el-form {
  line-height: 30px;
}
</style>

<template>
  <el-form>
    <el-form-item label="Title">
      <el-input
          clearable
          v-model="title"
          placeholder="Input your title.">
      </el-input>
    </el-form-item>
    <el-form-item label="Introduction">
      <el-input
          clearable
          type="textarea"
          v-model="introduction"
          placeholder="Input your content."></el-input>
    </el-form-item>
    <el-form-item label="Due">
      <el-row style="margin:0px"></el-row>
      <el-date-picker
          v-model="due"
          type="datetime"
          placeholder="Due Datetime">
      </el-date-picker>
    </el-form-item>
    <el-form-item label="Submission Type">
      <el-radio-group v-model="submissionType">
        <!--        <el-radio label="text">Text</el-radio>-->
        <el-radio label="file">File</el-radio>
      </el-radio-group>
    </el-form-item>

    <el-form-item label="Attachment">
      <el-upload
          class="upload-demo"
          drag
          multiple
          :data="this.submissionData"
          ref="upload"
          action="http://127.0.0.1:8080/api/submit_event_file/"
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

    <el-form-item>
      <el-row></el-row>
      <el-button @click="onClickSubmit">Submit</el-button>
    </el-form-item>
  </el-form>
</template>

<script>
export default {
  name: 'NewSubmission',
  data() {
    return {
      type: '',
      title: '',
      introduction: '',
      due: '',
      submissionType: 'file',
      groupList: [],
      selectedPartitionList: [],
      selectedGroupList: [],
      fileList: [],
      submissionData: {'token': '', 'event_id': ''},
    };
  },
  props: {
    projectId: {
      type: Number,
      required: true,
    },
    courseId: {
      type: Number,
      required: true,
    },
    partitionList: {
      required: true,
    }
  },
  created() {
    this.$axios.post('/get_all_partition/', {'project_id': this.$props.projectId}).then(res => {
      console.log(res);
    }).catch(err => {
      console.log(err);
    });
  },
  methods: {
    handleFileChange (file, fileList) {
      this.fileList = fileList
    },
    onClickSubmit() {
      this.$axios.post('/send_key/', {'course': this.courseId}).then(res => {
        console.log(res);
        const event = this.toJson();
        const data = {};
        data.project_id = this.$props.projectId;
        data.event_title = event.title;
        data.event_type = event.eventType;
        data.event_detail = event;
        data.key = res.data['SendKey'];
        data.partitionList = this.selectedPartitionList
        this.$axios.post('/create_event/', data).then(res => {
          console.log(res);
          if (res.data['CreateEvent'] === 'success' && this.fileList.length !== 0)
          {
            this.submissionData['event_id'] =res.data.Event_id
            this.submissionData['token'] = localStorage.getItem('Authorization')
            this.$refs.upload.submit()
          }
        }).catch(err => {
          console.log(err);
        });
      }).catch(err => {
        console.log(err);
      });
    },
    toJson() {
      const event = {};
      event.title = this.title;
      event.introduction = this.introduction;
      event.due = this.due.getTime();
      event.eventType = 'SubmissionEvent';
      event.submissionType = this.submissionType;
      event.selectedPartitionList = this.selectedPartitionList
      // event.selectedGroupList = this.selectedGroupList;
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

</style>

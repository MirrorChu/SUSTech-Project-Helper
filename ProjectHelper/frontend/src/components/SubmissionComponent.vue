<template>
  <div>
    <div>
      <h2 align="center">{{ this.$props.data.title }}</h2>
    </div>
    <div align="center"><el-button @click="onClickExpand">{{ this.expand ? 'Close' : 'Expand'}}</el-button>
      <el-button @click="onClickDeleteEvent">Delete Event</el-button></div>

    <div v-if="expand">
      <div v-if="privileges && privileges['teach'] === 1">

        <div v-if="edit">
          <el-form>
            <h3 style="font-family: Verdana, serif;">Introduction: </h3>
            <el-form-item label="">
              <el-input type="textarea" v-model="eventObj['data']['introduction']"></el-input>

            </el-form-item>
            <h3 style="font-family: Verdana, serif;">File List: </h3>
            <el-form-item label="">
              <div v-if="this.eventDetail['file_name'] && this.eventDetail['file_name'].length !== 0">
                <div v-for="(item, index) in eventDetail['file_name']">
                  <el-link :href="generateFileUrl(eventDetail['file_id'][index])">{{ item }}</el-link>
                </div>
              </div>
              <div v-else>No Attachment</div>
            </el-form-item>
            <h3 style="font-family: Verdana, serif;">Upload file: </h3>
            <el-form-item label="">
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
          </el-form>
          <el-button @click="onClickConfirmEdit">Confirm Edit</el-button>
        </div>
      </div>

      <div v-if="!edit">
        <el-form>
          <h3 style="font-family: Verdana, serif;">Introduction: </h3>
          <el-form-item label="">
            <div>{{ this.eventObj['data']['introduction'] }}</div>
          </el-form-item>
          <h3 style="font-family: Verdana, serif;">Due time: </h3>
          <el-form-item label="">
            {{ new Date(this.eventObj.data.due) }}
          </el-form-item>
          <h3 style="font-family: Verdana, serif;">File List: </h3>
          <el-form-item label="">
            <div v-if="this.eventDetail['file_name'] && this.eventDetail['file_name'].length !== 0">
              <div v-for="(item, index) in eventDetail['file_name']">
                <el-link :href="generateFileUrl(eventDetail['file_id'][index])">{{ item }}</el-link>
              </div>
            </div>
            <div v-else>No Attachment</div>
          </el-form-item>
          <el-button @click="edit = !edit">{{ edit ? 'Cancel' : 'Edit' }}</el-button>
        </el-form>

      </div>

      <div v-if="privileges && privileges['eventGrade'] === 1">
        <div v-if="privileges && privileges['eventGrade']">
          <EventGrading
              v-bind:eventDetail="this.eventDetai"
              v-bind:eventId="this.$props.eventId"
              v-bind:submissionDetail="submissionDetail">
          </EventGrading>
        </div>
      </div>
      <div v-if="!privileges || privileges['eventGrade'] !== 1">
        <el-upload
            drag
            action="http://127.0.0.1:8000/submit_event/"
            :data="dataBlock"
            :on-success="onSuccess"
            multiple>
          <i class="el-icon-upload"></i>
          <div class="el-upload__text">Drag files here, or <em>click to upload</em>.</div>
        </el-upload>
      </div>

      <div v-if="privileges && privileges['teach'] !== 1">
        <div v-if="eventDetail['data']['file_id']">
          <h3>My Submission</h3>
          <div v-for="(item, index) in eventDetail['data']['file_name']">
            <el-link :href="generateFileUrl(eventDetail['data']['file_id'][index])">
              {{ item }}
            </el-link>
            <el-button class="el-icon-delete" @click="onClickDelete(index)"></el-button>
          </div>
        </div>

        <div v-if="eventDetail['data']['group_score']">
          <div>
            <h3>Group Score: {{ eventDetail['data']['group_score'] }}</h3>
          </div>
        </div>

        <div v-if="eventDetail['data']['student_score']">
          <div>
            <h3>My Score: {{ eventDetail['data']['student_score'] }}</h3>
          </div>
        </div>

        <div v-if="eventDetail['data']['comment']">
          <h3>Comment</h3>
          {{ eventDetail['data']['comment'] }}
        </div>
      </div>

      <div v-if="privileges && privileges['eventEdit'] === 1">
        <br/>
      </div>
    </div>
  </div>
</template>

<script>
import EventGrading from './EventGrading';

export default {
  name: 'SubmissionComponent',
  components: {EventGrading},
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
      submissionText: '',
      fileList: [],
      expand: false,
      eventDetail: {},
      eventDetai: {},
      edit: false,
      eventObj: {},
      submissionDetail: [],
      privileges: {},
      dataBlock: {},
      submissionData: {'token': '', 'event_id': ''},
    };
  },
  created() {
    this.token = localStorage.getItem('Authorization');
    this.submissionData['token'] = localStorage.getItem('Authorization')
    this.submissionData['event_id'] = this.$props.eventId
    this.edit = false;
    this.pullData()
  },
  methods: {
    pullData()
    {
      this.$axios.post('/get_event_detail/', {'event_id': this.$props.eventId}).then(res => {
        console.log('===debug===', res);
        this.submissionDetail = res.data['Data']['data'];
        this.eventDetai = res.data;
        this.eventDetail = res.data['Data'];
        let eventEle = res.data['Data'];
        let typeStr = eventEle['event_type'];
        if (typeStr === 'submission' || typeStr === 'SubmissionEvent') {
          this.eventObj['type'] = 'SubmissionComponent';
          this.eventObj['data'] = {};
          this.eventObj['data']['type'] = 'SubmissionComponent';
          this.eventObj['partitionType'] = eventEle['event_detail']['partitionType'];
        }
        this.eventObj['data']['title'] = eventEle['event_title'];
        this.eventObj['data']['introduction'] = 'hello world!'
        this.eventObj['data']['introduction'] = eventEle['introduction'];
        this.eventObj['data']['due'] = eventEle['event_detail']['due'];
        this.eventObj['publisher'] = eventEle['publisher'];
        this.eventObj['id'] = this.$props.eventId;

        this.$axios.post('/get_privilege_list/', {'course_id': this.$props.courseId}).then(res => {
          this.privileges = res.data['Data'];
        }).catch(err => {
          console.log(err);
        });
        this.dataBlock['token'] = localStorage.getItem('Authorization');
        this.dataBlock['event_id'] = this.$props.eventId;
      }).catch(err => {
        console.log(err);
      });
    },
    onClickDeleteEvent() {
      this.$axios.post('/delete_event/', {'event_id': this.eventObj['id']}).then(res => {
        this.$message.warning('Delete Event ' + res.data['DeleteEvent']);
        this.$parent.$parent.pullData()
      }).catch(err => {
        console.log(err);
      });
    },
    handleFileChange(file, fileList) {
      this.fileList = fileList
    },
    handleFileRemove() {

    },
    onClickExpand() {
      this.expand = !this.expand;
    },
    onSuccess(response, file, fileList) {
      console.log(response);
      this.$parent.$parent.pullData()
      this.pullData()
    },
    generateFileUrl(id) {
      return 'http://127.0.0.1:8000/download_event_file?token='
          + localStorage.getItem('Authorization')
          + '&file_id='
          + id.toString();
    },
    onClickDelete(index) {
      this.$axios.post('/delete_event_file/', {
        'file_id': this.eventDetail['data']['file_id'][index]
      }).then(res => {
        this.$message.warning('Delete File ' + this.eventDetail['data']['file_name'][index]);
        this.$parent.$parent.pullData()
      }).catch(err => {
        console.log(err);
      });
    },
    onClickConfirmEdit()
    {
      this.$axios.post('/change_event/', {
        'event_id': this.$props.eventId,
        'introduction': this.eventObj['data']['introduction'],
      }).then(res => {
        console.log(res);
        this.edit = false
        if (this.fileList && this.fileList.length !== 0)
        {
          this.$refs.upload.submit()
        }
        this.$parent.$parent.pullData()
      }).catch(err => {
        console.log(err);
      });
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
  },
};
</script>

<style scoped>

</style>

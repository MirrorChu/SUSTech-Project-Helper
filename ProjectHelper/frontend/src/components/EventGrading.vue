<template>
  <div>
    <div>
      <h4>
        Submission Condition
      </h4>
    </div>
    <el-table
        :data="groupList"
        style="width: 100%">
      <el-table-column
          prop="group_id"
          label="Group ID"
          width="180">
      </el-table-column>
      <el-table-column
          prop="group_name"
          label="Group Name"
          width="180">
      </el-table-column>
      <el-table-column label="Detail">
        <el-button slot-scope="scope" @click="onClickDetail(scope)">Detail</el-button>
      </el-table-column>
    </el-table>

    <div v-if="idx < 0">
      <el-link :href="this.downloadAllUrl">Download All Submission</el-link>
    </div>

    <div v-if="idx < 0">
      <el-link :href="this.downloadGradingTemplate">Download Grading Template</el-link>
    </div>

    <el-upload
        v-if="idx < 0"
        class="upload-demo"
        action="https://jsonplaceholder.typicode.com/posts/">
      <el-button>Upload Grading File</el-button>
    </el-upload>


    <h4 v-if="idx >= 0">
      Group Submission Detail
    </h4>
    <el-card v-if="idx >= 0">
      <el-button @click="idx = -1">Close</el-button>

      <el-form>
        <el-form-item label="Submission Detail">
          <div v-if="eventDetail['Data']['event_type'] === 'partition'">
            {{ eventDetail }}
            <div>
              <h3>
                Selected Options
              </h3>
            </div>
            <div v-for="literal in selectedChoiceLiteral">
              {{ literal }}
            </div>
          </div>
          <div v-else-if="eventDetail['Data']['event_type'] === 'submission' ||
          eventDetail['Data']['event_type'] === 'SubmissionEvent'">
            {{ eventDetail }}
            <div>
              <h3>
                Submission
              </h3>
              <el-link v-for="(item, index) in eventDetail['Data']['data']"
                       :href="generateFileUrl(item['file_id'][index])">
                {{ item['file_name'][index] }}
              </el-link>
            </div>
          </div>

          <div>
            <h3>
              Submission Datetime
            </h3>
            {{ new Date(this.submission_datetime) }}
          </div>

          <div v-if="eventDetail['Data']['data'][this.idx]['group_score']">
            <div>
              <h3>Group Score: {{ eventDetail['Data']['data'][this.idx]['group_score'] }}</h3>
            </div>
            <div v-for="item in eventDetail['Data']['data'][this.idx]['memberList']">
              {{ item['student_id'] + ' ' + item['real_name'] + ': ' + item['score'] }}
            </div>
          </div>

          <div v-if="eventDetail['Data']['data'][this.idx]['comment']">
            <h3>Comment</h3>
            {{ eventDetail['Data']['data'][this.idx]['comment'] }}
          </div>
        </el-form-item>

        <el-form-item label="Group Score">
          <el-input-number v-model="groupScore"></el-input-number>
        </el-form-item>

        <el-form-item v-for="(value, key) in memberLiterals"
                      :label="value">
          <el-input-number v-model="memberScores[key]"></el-input-number>
        </el-form-item>

        <el-form-item label="Feedback">
          <el-input type="textarea" v-model="feedback"></el-input>
        </el-form-item>

      </el-form>

      <el-button @click="onClickGrade">Grade</el-button>
    </el-card>

  </div>
</template>

<script>
export default {
  name: 'EventGrading',
  props: {
    submissionDetail: {
      required: true,
    },
    eventDetail: {
      required: true,
    },
    eventId: {
      type: Number,
      required: true,
    },
  }
  ,
  data() {
    return {
      pageSize: 1,
      groupList: [],
      idx: -1,
      selectedChoiceLiteral: [],
      groupScore: 0,
      memberScores: {},
      memberLiterals: {},
      feedback: '',
      groupId: 0,
      submission_datetime: 0,
      downloadAllUrl: '',
      downloadGradingTemplate: '',
    };
  }
  ,
  created() {
    this.groupList = this.$props.submissionDetail;
    this.downloadAllUrl = this.downloadAllSubmissionUrl();
    this.downloadGradingTemplate = 'http://127.0.0.1:8000/get_model_for_event?token=' +
        localStorage.getItem('Authorization') + '&event_id=' + this.eventId;
  }
  ,
  methods: {
    onClickDetail(scope) {
      this.idx = scope.$index;
      this.groupId = this.groupList[this.idx]['group_id'];
      const eventType = this.$props.eventDetail['Data']['event_type'];
      this.submission_datetime = this.$props.eventDetail['Data']['data'][this.idx]['submission_datetime'];
      //Grading partition event, which is not needed. This is just a trial.
      if (eventType === 'partition') {
        const partitionType = this.eventDetail['Data']['event_detail']['partitionType'];
        for (let i = 0; i < this.$props.eventDetail['Data']['data'][this.idx]['memberList'].length; i += 1) {
          const member = this.$props.eventDetail['Data']['data'][this.idx]['memberList'][i];
          this.memberLiterals[member['student_id']] = member['student_id'] + ' ' + member['real_name'];
          this.memberScores[member['student_id']] = 0;
        }
        if (partitionType === 'timeSlot') {
          for (let i = 0; i < this.$props.eventDetail['Data']['data'][this.idx]['choice'].length; i += 1) {
            const option = this.$props.eventDetail['Data']['data'][this.idx]['choice'][i];
            this.selectedChoiceLiteral.push('option ' + this.$props.eventDetail['Data']['data'][this.idx]['index'][i] +
                ': ' + (new Date(option[0])) + ' to ' + (new Date(option[1])));
          }
        }
        else {
          for (let i = 0; i < this.$props.eventDetail['Data']['data'][this.idx]['choice'].length; i += 1) {
            const option = this.$props.eventDetail['Data']['data'][this.idx]['choice'][i];
            console.log(option);
            this.selectedChoiceLiteral.push('option' + this.$props.eventDetail['Data']['data'][this.idx]['index'][i] +
                ': ' + option[0]);
          }
        }
      }
      //TODO
      else if (eventType === 'Submission' || eventType === 'SubmissionEvent') {
        for (let i = 0; i < this.$props.eventDetail['Data']['data'][this.idx]['memberList'].length; i += 1) {
          const member = this.$props.eventDetail['Data']['data'][this.idx]['memberList'][i];
          this.memberLiterals[member['student_id']] = member['student_id'] + ' ' + member['real_name'];
          this.memberScores[member['student_id']] = 0;
        }
      }
      //TODO
      else if (eventType === 'Selection' || eventType === 'SelectionEvent') {
        for (let i = 0; i < this.$props.eventDetail['Data']['data'][this.idx]['memberList'].length; i += 1) {
          const member = this.$props.eventDetail['Data']['data'][this.idx]['memberList'][i];
          this.memberLiterals[member['student_id']] = member['student_id'] + ' ' + member['real_name'];
          this.memberScores[member['student_id']] = 0;
        }
      }

    },
    onClickGrade() {
      const dataBlock = {
        'comment': this.feedback,
        'score': this.memberScores,
        'group_score': this.groupScore,
        'group_id': this.groupId,
        'event_id': this.$props.eventId,
      };
      this.$axios.post('/mark_event/', dataBlock).then(res => {
        console.log(res);
      }).then(err => {
        console.log(err);
      });
    },
    generateFileUrl(id) {
      return 'http://127.0.0.1:8000/download_event_file?token='
          + localStorage.getItem('Authorization')
          + '&file_id='
          + id.toString();
    },
    downloadAllSubmissionUrl() {
      const tokenStr = 'token=' + localStorage.getItem('Authorization');
      const eventIdStr = 'event_id=' + this.eventId;
      return 'http://127.0.0.1:8000/download_event_submission' + '?' + tokenStr + '&' + eventIdStr;
    },
  },
};
</script>

<style scoped>
</style>

<template>
  <div>
    <div>
      <h4>
        Submission Condition
      </h4>
    </div>
    <el-card>
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

      <el-button v-if="idx < 0">
        Download Grading Template
      </el-button>

      <el-upload
          v-if="idx < 0"
          class="upload-demo"
          action="https://jsonplaceholder.typicode.com/posts/">
        <el-button>Upload Grading File</el-button>
      </el-upload>

    </el-card>

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
          <div>
            <h3>
              Submission Datetime
            </h3>
            Please include submission datetime here.
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
  data () {
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
    }
  }
  ,
  created () {
    this.groupList = this.$props.submissionDetail
  }
  ,
  methods: {
    onClickDetail (scope) {
      this.idx = scope.$index
      this.groupId = this.groupList[this.idx]['group_id']
      const partitionType = this.eventDetail['Data']['event_detail']['partitionType']
      for (let i = 0; i < this.$props.eventDetail['Data']['data'][this.idx]['memberList'].length; i += 1) {
        const member = this.$props.eventDetail['Data']['data'][this.idx]['memberList'][i]
        this.memberLiterals[member['student_id']] = member['student_id'] + ' ' + member['real_name']
        this.memberScores[member['student_id']] = 0
      }
      if (partitionType === 'timeSlot') {
        for (let i = 0; i < this.$props.eventDetail['Data']['data'][this.idx]['choice'].length; i += 1) {
          const option = this.$props.eventDetail['Data']['data'][this.idx]['choice'][i]
          this.selectedChoiceLiteral.push('option ' + this.$props.eventDetail['Data']['data'][this.idx]['index'][i] +
              ': ' + (new Date(option[0])) + ' to ' + (new Date(option[1])))
        }
      }
    },
    onClickGrade () {
      const dataBlock = {
        'comment': this.feedback,
        'score': this.memberScores,
        'group_score': this.groupScore,
        'group_id': this.groupId,
        'event_id': this.$props.eventId,
      }
      this.$axios.post('/mark_event/', dataBlock).then(res => {
        console.log(res)
      }).then(err => {
        console.log(err)
      })
    },
  },
}
</script>

<style scoped>

</style>

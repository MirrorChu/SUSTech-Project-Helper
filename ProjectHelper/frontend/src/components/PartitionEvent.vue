<template>
  <div>
    <div>
      <div><h3>{{ this.$props.eventTitle }}</h3></div>
      <div>
        <el-button @click="onClickExpand">{{ this.expand ? 'Close' : 'Expand'}}</el-button>
      </div>

      <div v-if="expand">
        <div v-if="privileges && privileges['teach'] === 1">
          <div><el-button @click="edit = !edit">{{ edit ? 'Close' : 'Edit' }}</el-button></div>
          <div>Introduction: {{ this.eventObj['data']['introduction'] }}</div>
          <div>Due: {{ new Date(this.eventObj.data.due) }}</div>
          <div>Limit of Selections: {{ this.eventObj.data.selectionLimit }}</div>
          <div v-if="this.eventDetail['file_name'] && this.eventDetail['file_name'].length !== 0">
            <div v-for="(item, index) in eventDetail['file_name']">
              <el-link :href="generateFileUrl(eventDetail['file_id'][index])">{{ item }}</el-link>
              <el-button icon="el-icon-delete" @click="onClickDeleteEventFile(eventDetail['file_id'][index])">
              </el-button>
            </div>
          </div>
          <div v-else>No file</div>
          <div >
            <el-select v-model="selected"
                       :multiple="this.eventObj.data.selectionLimit > 1"
                       :multiple-limit="this.eventObj.data.selectionLimit"
                       placeholder="Please select.">
              <el-option v-for="(item, index) in this.eventObj.data.options" :key="item.value"
                         :label="getLabelAndNumberFromItem(item)" :value="index">
              </el-option>
            </el-select>
          </div>
          <div v-if="this.edit">
            <el-form>
              <el-form-item label="Introduction">
                <el-input v-model="eventObj['data']['introduction']"></el-input>
              </el-form-item>
              <el-form-item label="Due">
                <el-date-picker
                  v-model="this.due"
                  type="datetime"
                  placeholder="Due Datetime">
                </el-date-picker>
              </el-form-item>
              <div v-if="this.eventDetail['file_name'] && this.eventDetail['file_name'].length !== 0">
                <div v-for="(item, index) in eventDetail['file_name']">
                  <el-link :href="generateFileUrl(eventDetail['file_id'][index])">{{ item }}</el-link>
                  <el-button icon="el-icon-delete" @click="onClickDeleteEventFile(eventDetail['file_id'][index])">
                  </el-button>
                </div>
              </div>
              <div v-else>No file</div>
              <el-form-item label="Upload File">
                <el-upload
                  class="upload-demo"
                  drag
                  multiple
                  :data="this.partitionData"
                  ref="upload"
                  action="http://127.0.0.1:8080/api/submit_event_file/"
                  :file-list="fileList"
                  :auto-upload="false"
                  :on-change="handleFileChange">
                  <i class="el-icon-upload"></i>
                  <div class="el-upload__text">Drag file here, or <em>click to upload</em>.</div>
                </el-upload>
              </el-form-item>
              <el-form-item><el-button @click="onClickConfirmEdit">Confirm Edit</el-button></el-form-item>
            </el-form>
          </div>
          <div><el-button @click="onClickDeleteEvent">Delete Event</el-button></div>
        </div>

        <div v-if="privileges && privileges['teach'] === 0">
          <div>Introduction: {{ this.eventObj['data']['introduction'] }}</div>
          <div>Due: {{ new Date(this.eventObj.data.due) }}</div>
          <div>Limit of Selections: {{ this.eventObj.data.selectionLimit }}</div>
          <div v-if="this.eventDetail['file_name'] && this.eventDetail['file_name'].length !== 0">
            <div v-for="(item, index) in eventDetail['file_name']">
              <el-link :href="generateFileUrl(eventDetail['file_id'][index])">{{ item }}</el-link>
            </div>
          </div>
          <div v-else>No Attachment</div>
          <div v-if="eventDetail['data']['choice']">
            <h3>Selected Options</h3>
            <div v-for="item in eventDetail['data']['choice']">
              {{ generateTimeSlotChoiceLiteral(item) }}
            </div>
          </div>
          <div v-else>
            <el-select v-model="selected"
                       :multiple="this.eventObj.data.selectionLimit > 1"
                       :multiple-limit="this.eventObj.data.selectionLimit"
                       placeholder="Please select.">
              <el-option v-for="(item, index) in this.eventObj.data.options" :key="item.value"
                         :label="getLabelAndNumberFromItem(item)" :value="index">
              </el-option>
            </el-select>
            <br>
            <el-button @click="onClickSubmit">Submit</el-button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import EventGrading from './EventGrading';

export default {
  name: 'PartitionEvent',
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
    eventTitle: {
      required: true,
    },
  },
  data() {
    return {
      selected: [],
      expand: false,
      privileges: {},
      eventObj: {},
      submissionDetail: [],
      edit: false,
      token: '',
      eventDetail: {},
      partitionData: {'token': '', 'event_id': ''},
      fileList: [],
      due: new Date(),
    };
  },
  created() {
    this.token = localStorage.getItem('Authorization');
    this.partitionData['token'] = localStorage.getItem('Authorization')
    this.partitionData['event_id'] = this.$props.eventId
    this.edit = false;
    this.pullData()
  },
  methods: {
    pullData()
    {
      this.$axios.post('/get_event_detail/', {'event_id': this.$props.eventId}).then(res => {
        console.log(res);
        this.submissionDetail = res.data['Data']['data'];
        this.eventDetail = res.data;
        const eventEle = res.data['Data'];
        const typeStr = eventEle['event_type'];
        if (typeStr === 'partition') {
          this.eventObj['type'] = 'PartitionEvent';
          this.eventObj['data'] = {};
          this.eventObj['data']['type'] = 'PartitionEvent';
          this.eventObj['data']['selectionLimit'] = eventEle['event_detail']['selectionLimit'];
          this.eventObj['partitionType'] = eventEle['event_detail']['partitionType'];
          this.eventObj['data']['partitionType'] = eventEle['event_detail']['partitionType'];
          this.eventObj['data']['options'] = [];
          if (this.eventObj['data']['partitionType'] === 'normal') {
            for (let j = 0; j < eventEle['event_detail']['options'].length; j += 1) {
              const option = eventEle['event_detail']['options'][j];
              this.eventObj['data']['options'].push({'label': option[0], 'value': j, 'limit': option[1]});
            }
          }
          else {
            for (let j = 0; j < eventEle['event_detail']['options'].length; j += 1) {
              const option = eventEle['event_detail']['options'][j];
              this.eventObj['data']['options'].push(this.generateTimeSlotPartitionOptions(option));
            }
          }
        }
        this.eventObj['data']['title'] = eventEle['event_title'];
        this.eventObj['data']['introduction'] = eventEle['introduction'];
        this.eventObj['data']['due'] = eventEle['event_detail']['due'];
        this.eventObj['publisher'] = eventEle['publisher'];
        this.eventObj['id'] = this.$props.eventId;

        this.$axios.post('/get_privilege_list/', {'course_id': this.$props.courseId}).then(res => {
          this.privileges = res.data['Data'];
        }).catch(err => {
          console.log(err);
        });
        this.eventDetail = res.data['Data'];
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
    handleFileChange (file, fileList) {
      this.fileList = fileList
    },
    generateTimeSlotPartitionOptions(option) {
      const label = new Date(option[0]) + ' to ' + new Date(option[1]);
      const value = label;
      const limit = option[2];
      return {'label': label, 'value': value, 'limit': limit};
    },
    onClickDeleteEvent() {
      this.$axios.post('/delete_event/', {'event_id': this.eventObj['id']}).then(res => {
        this.$message.success('Delete Event ' + res.data['DeleteEvent']);
        this.$parent.$parent.pullData()
      }).catch(err => {
        console.log(err);
      });
    },
    onClickSubmit() {
      const selected = this.selected;
      this.$axios.post('/submit_event/', {'event_id': this.$props.eventId, 'selected': selected}).then(res => {
        console.log(res);
        this.pullData()
      }).catch(err => {
        console.log(err);
      });
    },
    getLabelAndNumberFromItem(item) {
      return item.label + ': ' + item.limit + ' remaining';
    },
    onClickExpand() {
      this.expand = !this.expand;
    },
    generateTimeSlotChoiceLiteral(choice) {
      if (choice.length === 3) {
        return new Date(choice[0]) + ' to ' + new Date(choice[1]);
      }
      else {
        return choice[0];
      }
    },
    onClickConfirmEdit()
    {
      this.$axios.post('/change_event/', {
        'event_id': this.$props.eventId,
        'introduction': this.eventObj['data']['introduction'],
        'due': this.due.getTime()
      }).then(res => {
        console.log(res);
        if (this.fileList && this.fileList.length !== 0)
        {
          this.$refs.upload.submit()
        }
        this.edit = false
        this.$parent.$parent.pullData()
        this.pullData()
      }).catch(err => {
        console.log(err);
      });
    }
  },
};
</script>

<style scoped>

</style>

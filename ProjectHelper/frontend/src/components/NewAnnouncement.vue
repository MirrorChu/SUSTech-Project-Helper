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
          <el-date-picker
              v-model="due"
              type="datetime"
              placeholder="Due Datetime">
          </el-date-picker>
        </el-form-item>

        <el-form-item label="Attachment">
          TODO
          <el-upload
              class="upload-demo"
              drag
              action="https://jsonplaceholder.typicode.com/posts/"
              multiple>
            <i class="el-icon-upload"></i>
            <div class="el-upload__text">Drag file here, or <em>click to upload</em>.</div>
          </el-upload>
        </el-form-item>

        <el-form-item label="Select Partition">
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

        <!--        <el-form-item label="Select Group">-->
        <!--          <el-select v-model="selectedGroupList" multiple placeholder="Select Partitions">-->
        <!--            <el-option-->
        <!--                v-for="item in groupList"-->
        <!--                :key="item.value"-->
        <!--                :label="item.label"-->
        <!--                :value="item.value">-->
        <!--            </el-option>-->
        <!--          </el-select>-->
        <!--        </el-form-item>-->

      </el-form>
    </div>

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
    };
  },
  created() {

  },
  methods: {
    onClickSubmit() {
      this.$axios.post('/send_key/', {'course': this.$props.courseId}).then(res => {
        console.log(res)
        const event = this.toJson()
        const data = {}
        data.project_id = this.$props.projectId
        data.event_title = event.title
        data.event_type = event.eventType
        data.event_detail = event
        data.key = res.data['SendKey']
        this.$axios.post('/create_event/', data).then(res => {
          console.log('res', res);
        }).catch(err => {
          console.log('err', err);
        });
      }).catch(err => {
        console.log(err)
      })
    },
    toJson() {
      const event = {};
      event.eventType = 'announcement';
      event.title = this.title;
      event.introduction = this.introduction;
      event.due = this.due.getTime();
      event.partitionList = this.selectedPartitionList;
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

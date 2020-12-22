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
          <el-row style="margin:0px"></el-row>
          <el-select v-model="selectedPartitionList"
                     multiple placeholder="Select Partitions"
                     @change="onSelectPartition">
            <el-option
                v-for="item in partitionList"
                :key="item.value"
                :label="item.label"
                :value="item.value">
            </el-option>
          </el-select>
        </el-form-item>

        <el-form-item label="Select Group">
          <el-row style="margin:0px"></el-row>
          <el-select v-model="selectedGroupList" multiple placeholder="Select Partitions">
            <el-option
                v-for="item in groupList"
                :key="item.value"
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
  data() {
    return {
      type: 'Announcement',
      title: '',
      introduction: '',
      due: '',
      eventId: '',
      partitionList: [],
      groupList: [],
      selectedPartitionList: [],
      selectedGroupList: [],
    };
  },
  created() {

  },
  methods: {
    onClickSubmit() {
      console.log(this.toJson());
      this.$axios.post('/test/', {jsonObj: this.toJson()}).then(res => {
        console.log('res', res);
      }).catch(err => {
        console.log('err', err);
      });
    },
    toJson() {
      const event = {};
      event.type = 'Announcement';
      event.title = this.title;
      event.introduction = this.introduction;
      event.due = this.due.getTime();
      event.selectedGroupList = this.selectedGroupList;
      return event;
    },
    onSelectPartition(selected) {
      //TODO: Partition influences selected group.
      console.log(selected);
    },
    getAllPartitions() {

    },
  },

};
</script>

<style scoped>
.el-form{
  line-height: 30px;
}
</style>

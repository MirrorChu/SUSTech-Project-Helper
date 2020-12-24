<template>
  <div>
    <div><h3>New Event</h3></div>
<!--    <el-button @click="parentFunc">TESTING</el-button>-->
    <div v-if="expand">
      <div>
        <el-button @click="onClickExpand">Close</el-button>
      </div>
      <el-form>
        <el-form-item label="Event Type">
          <el-radio-group v-model="eventType">
            <el-radio :label="0">Announcement</el-radio>
            <!--            <el-radio :label="1">Selection</el-radio>-->
            <el-radio :label="2">Submission</el-radio>
            <el-radio :label="3">Partition</el-radio>
            <!--            <el-radio :label="4">Upload</el-radio>-->
          </el-radio-group>
        </el-form-item>

        <el-form-item v-if="eventType === 0">
          <NewAnnouncement
              v-bind:courseId="courseId"
              v-bind:projectId="projectId"
              v-bind:partitionList="partitionList">
          </NewAnnouncement>
        </el-form-item>

        <!--        <el-form-item v-else-if="eventType === 1">-->
        <!--          <NewSelection></NewSelection>-->
        <!--        </el-form-item>-->

        <el-form-item v-else-if="eventType === 2">
          <NewSubmission v-bind:projectId="this.$props.projectId"
                         v-bind:partitionList="this.partitionList"
                         v-bind:courseId="this.$props.courseId">
          </NewSubmission>
        </el-form-item>

        <el-form-item v-else-if="eventType === 3">
          <NewPartition
              v-bind:course-id="courseId"
              v-bind:projectId="projectId">
          </NewPartition>
        </el-form-item>
      </el-form>
    </div>

    <div v-if="!expand">
      <el-button @click="onClickExpand">Expand</el-button>
    </div>
  </div>
</template>

<script>
import NewAnnouncement from './NewAnnouncement'
import NewSelection from './NewSelection'
import NewSubmission from './NewSubmission'
import NewPartition from './NewPartition'

export default {
  name: 'NewEvent',
  components: { NewPartition, NewSubmission, NewSelection, NewAnnouncement },
  props: {
    sid: {
      type: String,
      required: true,
    },
    projectId: {
      type: Number,
      required: true,
    },
    courseId: {
      type: Number,
      required: true,
    },
  },
  data () {
    return {
      eventType: 1,
      expand: false,
      partitionList: [],
    }
  },
  created () {
    this.$axios.post('/get_all_partition/', { 'project_id': this.projectId }).then(res => {
      console.log(res)
      for (let i = 0; i < res.data['Data'].length; i += 1) {
        //TODO: timeSlot and normal
        const partition = res.data['Data'][i]
        const option = {}
        if (typeof partition['option_name'] === typeof Number) {
          const start = new Date(partition['option_name'][0])
          const end = new Date(partition['option_name'][1])
          option['label'] = partition['partition_name'] + start + ' to ' + end
        } else {
          option['label'] = partition['partition_name'] + ': ' + partition['option_name']
        }
        const item = {
          'partition_id': partition['partition_id'],
          'option_id': partition['option_id'],
        }
        option['value'] = JSON.stringify(item)
        // option['value'] = '{' + '\\"partition_id\\"' + ':' + partition['partition_id'] + ',' +
        //     '\\"option_id\\"' + ':' + partition['option_id'] + '}';
        option['key'] = i
        this.partitionList.push(option)
      }
    }).catch(err => {
      console.log(err)
    })
  },
  methods: {
    onClickExpand () {
      this.expand = !this.expand
    },
    parentFunc () {
      this.$parent.$parent.testing()
    },
  },
}
</script>

<style scoped>

</style>

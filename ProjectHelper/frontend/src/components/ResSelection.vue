<template>
  <div>

    <div>
      <el-form>
        <el-form-item label="Project ID">
          {{ this.$props.projectId }}
        </el-form-item>
        <el-form-item label="Group ID">
          {{ this.$props.groupId }}
        </el-form-item>
        <el-form-item label="Selected">
          {{ res.selected }}
        </el-form-item>
      </el-form>
    </div>

    <div>
      <el-form>
        <el-form-item v-for="member in membersList" :label="member">
          <el-input clearable placeholder="Grade" v-model="gradesDict[member]"></el-input>
        </el-form-item>
      </el-form>
      <el-form-item label="feedback">
        <el-input clearable type="textarea" v-model="feedback"></el-input>
      </el-form-item>
      <el-button @click="onClickSubmit">Submit</el-button>
    </div>

  </div>

</template>

<script>
export default {
  name: 'ResSelection',
  props: {
    sid: {
      type: String,
      required: true,
    },
    pswd: {
      type: String,
      required: true,
    },
    identity: {
      type: String,
      required: true,
    },
    projectId: {
      type: Number,
      required: true,
    },
    groupId: {
      type: Number,
      required: true,
    },
    eventId: {
      type: String,
      required: true,
    },
  },
  data () {
    return {
      res: {},
      membersList: [],
      gradesDict: {},
      feedback: '',
    }
  },
  created () {
    //TODO: Get members list and selection result from projectId and groupId.
    this.res = {
      selected: ['A'],
    }
    this.membersList = ['11810101', '11810102', '11810103']
    for (const member in this.membersList) {
      this.gradesDict[member] = -1
    }
  },
  methods: {
    onClickSubmit () {
      //Check if all members are graded legally.
      //Grades only allow non-negative numbers.
      //If a member is not graded, his or her grade would be -1.
      for (const member in this.membersList) {
        if (this.gradesDict[member] < 0) {
          this.$message.warning('Wrong grades. Did you grade all members?')
          return
        }
      }
      //TODO: Implement submission.
    },
  },

}
</script>

<style scoped>

</style>

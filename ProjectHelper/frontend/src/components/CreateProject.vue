<template>
  <div>
    <el-form>
      <el-form-item label="Course">
        <el-select v-model="this.newProjectCourse" placeholder="Course">
          <el-option v-for="course in newProjectCourseList" :key="course.value" :label="course.label"
                     :value="course.value"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="Project Name">
        <el-input v-model="newProjectName" placeholer="Project Name" clearable></el-input>
      </el-form-item>
      <el-form-item label="Description">
        <el-input v-model="newProjectDescription" placeholer="Description." clearable type="textarea"></el-input>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
export default {
  name: 'CreateProject',
  props: {
    sid: {
      type: String,
      required: true,
    },
    pswd: {
      type: String,
      required: true,
    },
  },
  created () {

  },
  data () {
    return {
      newProjectCourse: '',
      newProjectCourseList: [],
      newProjectName: '',
      newProjectDescription: '',
    }
  },
}
</script>

<style scoped>

</style>

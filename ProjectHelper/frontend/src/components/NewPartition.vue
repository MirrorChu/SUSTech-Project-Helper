<template>
  <div>
    <el-form>
      <el-form-item label="Title">
        <el-input clearable placeholder="Input your title."></el-input>
      </el-form-item>
      <el-form-item label="Introduction">
        <el-input clearable type="textarea" placeholder="Input your content."></el-input>
      </el-form-item>
      <el-form-item label="Due">
        <el-date-picker
          v-model="due"
          type="datetime"
          placeholder="Due Datetime">
        </el-date-picker>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
export default {
  name: 'NewPartition',
  data () {
    return {
      title: '',
      introduction: '',
      due: '',
      selectionLimit: 1,

    }
  },
}
</script>

<style scoped>

</style>

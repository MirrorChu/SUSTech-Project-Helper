<template>
  <div>
    <el-pagination
      layout="prev, pager, next"
      :total="groupsList.length"
      :page-size="pageSize"
      background
      @current-change="handleCurrentChange">
    </el-pagination>
    {{ groupsList[idx] }}
  </div>
</template>

<script>
export default {
  name: 'EventGrading',
  data () {
    return {
      pageSize: 1,
      groupsList: [
        { groupId: 1, membersList: ['11810101', '11810102'] },
        { groupId: 2, membersList: ['11810103', '11810104'] },
      ],
      idx: 0,
    }
  },
  methods: {
    handleCurrentChange (val) {
      console.log(val)
      this.idx = val - 1
    },
  },
}
</script>

<style scoped>

</style>

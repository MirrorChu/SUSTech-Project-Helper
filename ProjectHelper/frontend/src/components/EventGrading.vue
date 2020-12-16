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
            prop="groupId"
            label="Group ID"
            width="180">
        </el-table-column>
        <el-table-column
            prop="memberList"
            label="Members"
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
          <div>
            This is the detail of submission. It relies on v-if to distinguish between submission and seleciton.
          </div>
        </el-form-item>

        <el-form-item label="Group Score">
          <el-input></el-input>
        </el-form-item>

        <el-form-item v-if="idx >= 0" v-for="item in groupList[idx]['memberList']" :label="item + ' Score'">
          <el-input>
          </el-input>
        </el-form-item>

        <el-form-item label="Feedback">
          <el-input type="textarea"></el-input>
        </el-form-item>

      </el-form>

      <el-button>Grade</el-button>
    </el-card>


    <!--    <el-pagination-->
    <!--      layout="prev, pager, next"-->
    <!--      :total="groupsList.length"-->
    <!--      :page-size="pageSize"-->
    <!--      background-->
    <!--      @current-change="handleCurrentChange">-->
    <!--    </el-pagination>-->
  </div>
</template>

<script>
export default {
  name: 'EventGrading',
  data () {
    return {
      pageSize: 1,
      groupList: [
        { groupId: 1, memberList: ['11810101', '11810102'] },
        { groupId: 2, memberList: ['11810103', '11810104', '11810105'] },
      ],
      idx: -1,
    }
  },
  methods: {
    onClickDetail (scope) {
      this.idx = scope.$index
      console.log(scope.$index)
    },
  },
}
</script>

<style scoped>

</style>

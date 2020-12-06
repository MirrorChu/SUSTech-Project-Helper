<template>
  <div class="right-bot">
    <el-row>
      <el-col :span="8">
        <div class="grid-content">
          <div class="right-bot-fir">
            <div>
              <h1>LEFT</h1>
            </div>
          </div>
        </div>
      </el-col>
      <el-col :span="16">
        <div class="grid-content">
          <div class="right-bot-sec">
            <div>
              <h1>RIGHT</h1>
              <div
                v-for="(item, index) in botList"
                :key="index"
                class="right-bot-content"
              >
                <el-row class="right-el-row">
                  <el-col :span="6" style="text-align:left">
                    <span>{{ item.title }}</span>
                  </el-col>
                  <el-col :span="6">
                    <span>{{ item.year }}</span>
                  </el-col>
                  <el-col :span="6">
                    <span>
                      <i class="el-icon-user"></i>
                      {{ item.num }}
                    </span>
                  </el-col>
                  <el-col :span="6">
                    <span>
                      <i class="el-icon-view"></i>
                      {{ item.like }}
                    </span>
                  </el-col>
                </el-row>
              </div>
            </div>
          </div>
        </div>
      </el-col>
    </el-row>
    <el-row>
      <el-tree :data="data" :props="defaultProps" @node-click="handleNodeClick" style="background-color: black"></el-tree>
    </el-row>
    <el-row></el-row>
    <el-row>
      <el-pagination
        class="msg-pagination-container"
        layout="prev, pager, next"
        :current-page="currentPage"
        :page-size="pageSize"
        :total="100"
        @current-change="handleCurrentChange"
      />
    </el-row>
  </div>
</template>
<script>
export default {
  data() {
    return {
      //TODO
      isBackground: true,
      currentPage: 1,
      pageSize:5,
      Lists:[],
      defaultProps: {
        children: 'children',
        label: 'label'
      },
      data:[{
      label: '一级 1',
        children: [{
      label: '二级 1-1',
      children: [{
        label: '三级 1-1-1'
      }]
    }]
    }, {
      label: '一级 2',
        children: [{
        label: '二级 2-1',
        children: [{
          label: '三级 2-1-1'
        }]
      }, {
        label: '二级 2-2',
        children: [{
          label: '三级 2-2-1'
        }]
      }]
    }, {
      label: '一级 3',
        children: [{
        label: '二级 3-1',
        children: [{
          label: '三级 3-1-1'
        }]
      }, {
        label: '二级 3-2',
        children: [{
          label: '三级 3-2-1'
        }]
      }]
    }]
    }
  },
  name: 'rightBandBot',
  props: {
    botList: {
      default() {
        return []
      },
    },
  },
  methods:{
    //TODO
    handleCurrentChange(){

    },
    handleNodeClick(data) {
      console.log(data);
    }
  }
}
</script>
<style scoped>
.right-bot {
  height: 55%;
  width: 100%;
  /* background-color: #fff; */
  z-index: 10;
  position: absolute;
  bottom: 0;
  opacity: 0.8;
  filter: drop-shadow(100px -100px 200px black);
}
.right-bot .right-bot-fir {
  width: 70%;
  margin: 0 15%;
  /* background-color: rgb(190, 42, 42); */
}
.right-bot .right-bot-fir h1,
.right-bot .right-bot-sec h1 {
  margin: 0 0 10px 0;
  color: rgb(255, 255, 255);
}
.right-bot .right-bot-fir img {
  width: 90%;
  margin-bottom: 5%;
}

.right-bot .right-bot-sec {
  width: 90%;
  margin: 0 3%;
  /* background-color: rgb(156, 18, 18); */
}
.right-bot-sec .right-bot-content {
  height: 10%;
  line-height: 50px;
  font-weight: bolder;
  color: #fff;
  margin-bottom: 3%;
  filter: drop-shadow(5px 5px 10px black);
  text-align: center;
}
.right-bot-sec .right-bot-content .right-el-row {
  opacity: 1;
}
.msg-pagination-container{

}
 .msg-pagination-container.is-background.el-pager li {
   /*对页数的样式进行修改*/
   background-color: #FF8800;
   color: #FF8800;
 }
.msg-pagination-container.is-background .btn-next {
  /*对下一页的按钮样式进行修改*/
  background-color: #10263c;
  color: #FFF;
}
.msg-pagination-container.is-background .btn-prev {
  /*对上一页的按钮样式进行修改*/
  background-color: #10263c;
  color: #FFF;
}
.msg-pagination-container.is-background .el-pager li:not(.disabled).active {
  /*当前选中页数的样式进行修改*/
  background-color: #FF8800;
  color: #FF8800;
}
</style>

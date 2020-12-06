<template>
  <div class="right-top">
    <el-row>
      <el-col :span="12">
        <div class="grid-content">
          <div class="right-top-fir">
            <el-input class="search" placeholder="Search for project" prefix-icon="el-icon-search"></el-input>
          </div>
        </div>
      </el-col>
<!--      <el-col :span="5">-->
<!--        <el-button plain class="btn-fir">朴素按钮</el-button>-->
<!--      </el-col>-->
      <el-col :span="12">
        <div class="grid-content">
          <div class="right-top-sec">
            <img class="right-img" src="../../assets/img/1-5.jpg" alt="右头像" />
          </div>
        </div>
      </el-col>
    </el-row>
    <el-row style="margin-left: 50px">
      <el-col :span="2" style="color: white;font-size: 17px;margin-top: -17px" >
        <h3>Upload </h3>
      </el-col>
      <el-col :span="2" style="color: #FF9900;font-size: 17px;margin-top: -17px">
        <h3>Project</h3>
      </el-col>
      <el-button @click="onClickUpload"  class="el-icon-upload" style="margin-top: -7px"></el-button>
    </el-row>
  </div>
</template>
<script>
export default {
  name: "rightBandTop",
  methods:{
    onClickUpload(){
      // TODO
    }
  }
};
</script>
<style>
.right-top {
  width: 100%;
  height: 0px;
  z-index: 10;
  position: absolute;
  /*margin-left: 20px;*/
  /* background-color: rgb(116, 12, 12); */
}
.right-top .right-top-fir {
  line-height: 90px;
  padding-left: 50px;
  margin-top: -5px;
  margin-bottom: -45px;
  padding-bottom: -41px;
}
/*.right-top .right-top-fir .el-input__inner {*/
/*  width: 60%;*/
/*  border-radius: 50px;*/
/*  background-color: rgb(88, 85, 85);*/
/*  border: none;*/
/*  color: #fff;*/
/*  height: 35px;*/
/*}*/
.right-top-sec {
  height: 0px;
  /* background-color: rgb(152, 223, 131); */
}
.right-top-sec .right-img {
  padding: 20px;
  float: right;
  height: 40px;
  border-radius: 50%;
}
</style>

<template>
  <div class="left-top">
    <el-col :span="4"><img src="../../assets/img/download.png" alt="logo" /></el-col>
    <el-col :span="22" style="text-align: right;font-size: 18px;position: fixed">
      <h4>Welcome, {{11810101}}</h4>
    </el-col>
  </div>
</template>
<script>
export default {
  name: 'leftBandTop',
  data(){
    return{
      sid: this.$route.params.sid,
    }
  },
  mounted() {
    console.log(this.$route.params.sid)
  }
}
</script>
<style scoped>
.left-top {
  padding-left: 20px;
  padding-bottom: 25px;
  height: 25px;
  position: relative;
   background-color: rgba(247,248,248,0.9);
}
.left-top img {
  position: fixed;
  /*bottom:130px;*/
  /*top: -42px;*/
  left: -5px;
  /*border-radius: 50%;*/
  height: 55px;
  width: 143px;
  /*padding-top: 5px;*/
  /*margin-left: -40px;*/
  /*margin-top: 5px;*/
  /*padding-top: 30px;*/
}
</style>

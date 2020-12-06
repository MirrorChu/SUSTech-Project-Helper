<template>
  <div class="right-mid">
    <el-row>
      <el-col :span="8">
        <div class="grid-content">
          <div class="right-mid-fir">
            <div>
              <h1>Notifications</h1>
            </div>
          </div>
        </div>
      </el-col>
      <el-col :span="16">
        <div class="grid-content">
          <div class="right-mid-sec">
            <div>
              <h1>Project</h1>
              <div
                v-for="(item, index) in midList"
                :key="index"
                class="right-mid-content"
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
  </div>
</template>
<script>
export default {
  name: 'rightBandmid',
  props: {
    midList: {
      default() {
        return []
      },
    },
  },
}
</script>
<style scoped>
.right-mid {
  margin-top: 125px;
  height: 55%;
  width: 100%;
  /* background-color: #fff; */
  z-index: 10;
  position: absolute;
  /*midtom: 0;*/
  opacity: 0.8;
  filter: drop-shadow(100px -100px 200px black);
}
.right-mid .right-mid-fir {
  width: 70%;
  margin: 0 15%;
  /* background-color: rgb(190, 42, 42); */
}
.right-mid .right-mid-fir h1,
.right-mid .right-mid-sec h1 {
  margin: 0 0 10px 0;
  color: rgb(255, 255, 255);
}
.right-mid .right-mid-fir img {
  width: 90%;
  margin-midtom: 5%;
}
.span-fir {
  color: aliceblue;
  margin-midtom: 5%;
}
.btn-fir {
  width: 90%;
  color: #fff;
  background-color: transparent;
}

.right-mid .right-mid-sec {
  width: 90%;
  margin: 0 3%;
  /* background-color: rgb(156, 18, 18); */
}
.right-mid-sec .right-mid-content {
  height: 10%;
  line-height: 50px;
  font-weight: bolder;
  color: #fff;
  /*margin-midtom: 3%;*/
  filter: drop-shadow(5px 5px 10px black);
  text-align: center;
}
.right-mid-sec .right-mid-content .right-el-row {
  opacity: 1;
}
</style>

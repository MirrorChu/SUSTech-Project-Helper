<template>
  <div class="rightBand">
    <right-band-top></right-band-top>
<!--    <img src="../../assets/img/widthPic.jpg" alt="右大图" />-->
    <right-band-mid></right-band-mid>
    <right-band-bot></right-band-bot>
  </div>
</template>
<script>
import rightBandTop from './rightBandTop'
import rightBandBot from './rightBandBot'
import rightBandMid from './rightBandMid'
export default {
  name: 'rightBand',
  data() {
    return {
      botList: [
      ],
    }
  },
  components: {
    rightBandTop,
    rightBandMid,
    rightBandBot,
  },
}
</script>
<style scoped>
.rightBand {
  margin-bottom: 0px;
  padding-bottom: 0px;
  height: 100vh;
  width: 100%;
  position: relative;
  background-color: black;
}
/*.rightBand img {*/
/*  height: 100%;*/
/*  width: 100%;*/
/*  position: abosulte;*/
/*  background-size: cover;*/
/*  opacity: 0.8;*/
/*  filter: alpha(opacity=60);*/
/*}*/
</style>

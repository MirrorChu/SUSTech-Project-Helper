<template>
  <div class="leftBand">
    <left-band-top></left-band-top>
    <left-band-mid></left-band-mid>
<!--    <left-band-bot :botList="botList"></left-band-bot>-->
  </div>
</template>
<script>
import leftBandTop from './leftBandTop'
import leftBandMid from './leftBandMid'
// import leftBandBot from './leftBandBot'
export default {
  name: 'leftBand',
  data() {
    return {
      // midList: [],
      // botList: [],
    }
  },
  components: {
    leftBandTop,
    leftBandMid,
    // leftBandBot,
  },
}
</script>
<style scoped>
.leftBand {
  height: 100vh;
  background-color: #F7F8F8;
  margin: 0;
  /*padding-left: 0%;*/
}
</style>

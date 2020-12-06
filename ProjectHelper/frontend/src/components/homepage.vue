<template>
  <div class="homepage">
    <el-row>
        <left-band></left-band>
    </el-row>
  </div>
</template>
<script>
import leftBand from '../components/Left_band/leftBand'
import rightBand from '../components/Right_band/rightBand'
import profile from './profile'
import { updateCookie, getCookie, delCookie } from '../assets/js/cookie.js'
export default {
  name: 'homepage',
  data() {
    return {
      sid: 3463462,
      password: this.$route.params.pswd,
      name: '',
      showNav: false,
    }
  },
  components: {
    leftBand,
  },
  methods: {

  }
}
</script>

<style scoped>
.nav:not(.el-menu--collapse) {
  width: 200px;
  min-height: 400px;
}
.homepage{
  margin-top: -60px;
  margin-left: -10px;
  bottom: 500px;
  margin-bottom: -300px;
  padding-bottom: -300px;
}
</style>

<template>
  <el-container>
    <el-header style="height: 100px; background-color: #08213b; line-height: 100px;">
      <comp-header></comp-header>
    </el-header>
    <el-main style="padding:0px">
      <router-view></router-view>
    </el-main>
    <el-footer>
      <comp-footer></comp-footer>
   </el-footer>
  </el-container>
</template>
<style>
  .el-card {
    margin-bottom: 10px;
  }
  .li {
    float: none;
  }

</style>
<script>
  import CompHeader from '@/components/navigator/Header'
  import CompSidebar from '@/components/navigator/Sidebar'
  import CompFooter from '@/components/navigator/Footer'

  export default {
    name: 'dashboard',
    data() {
      return {
        s: 0
      }
    },
    components: {
      CompHeader,
      CompSidebar,
      CompFooter,
    },
    mounted: function() {
      this.get_authority()
    },
    methods: {
      get_authority() {
        if (sessionStorage.getItem('authority') == true) {
            s = 1
        }
      }
    }
  }
</script>

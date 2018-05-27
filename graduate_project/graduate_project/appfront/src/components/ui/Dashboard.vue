<template>
  <el-container>
    <el-header>
      <comp-header></comp-header>
    </el-header>
    <el-container>
      <el-aside width="200px">
        <comp-sidebar></comp-sidebar>
      </el-aside>
      <el-container>
        <el-main>
          <router-view></router-view>
        </el-main>
        <el-footer>
          <comp-footer></comp-footer>
        </el-footer>
      </el-container>
    </el-container>
  </el-container>
</template>
<style>
  .el-header {
    background-color: #B3C0D1;
    color: #333;
    line-height: 100px;
  }
  .el-aside {
    color: #333;
    margin-top: 100px;
  }
  .el-card {
    margin-bottom: 10px;
  }
</style>
<script>
  import CompHeader from '@/components/navigator/Header'
  import CompSidebar from '@/components/navigator/Sidebar'
  import CompFooter from '@/components/navigator/Footer'

  export default {
    name: 'dashboard',
    components: {
      CompHeader,
      CompSidebar,
      CompFooter
    },
    ready () {
    }
  }
</script>

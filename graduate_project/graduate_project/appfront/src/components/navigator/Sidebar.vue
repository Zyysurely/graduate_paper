<template>
  <el-aside width="200px">
    <el-menu router :default-active="$route.path" class="el-menu-vertical-demo">
      <el-submenu index="1">
        <template slot="title">
          <i class="el-icon-menu"></i>
          <span>Search Tools</span>
        </template>
        <el-menu-item-group>
          <el-menu-item index="algorithm">Search User</el-menu-item>
          <el-menu-item index="/loans/application_list">Search Loan</el-menu-item>
          <el-menu-item index="/financial/transaction_list">Search Transaction</el-menu-item>
        </el-menu-item-group>
      </el-submenu>
      <el-submenu index="2">
        <template slot="title">
          <i class="el-icon-menu"></i>
          <span>Audit</span>
        </template>
        <el-menu-item-group>
          <el-menu-item index="/audit/task_list">Task List</el-menu-item>
          <el-menu-item index="/audit/report">Report</el-menu-item>
        </el-menu-item-group>
      </el-submenu>
      <el-submenu index="3">
        <template slot="title">
          <i class="el-icon-menu"></i>
          <span>Collection</span>
        </template>
        <el-menu-item-group>
          <el-menu-item index="/collection/task_list">Task List</el-menu-item>
          <el-menu-item index="/collection/report">Report</el-menu-item>
        </el-menu-item-group>
      </el-submenu>
    </el-menu>
  </el-aside>
</template>
<script>
  export default {
    name: 'sidebar',
    data () {
      return {}
    },
    ready () {
    }
  }
</script>

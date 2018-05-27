<template>
    <div>
      <el-container>
        <el-menu
          router :default-active="$route.path"
          class="el-menu-demo"
          mode="horizontal"
          @select="handleSelect"
          background-color="#08213b"
          text-color="#fff"
          active-text-color="#ffd04b">
          <el-menu-item index="/demo"><h1><img src="./little.jpg" height="50" width="50"/>Network Alignment</h1></el-menu-item>
          <el-submenu index="">
            <template slot="title">
              <h1>Algorithm</h1>
            </template>
            <el-menu-item index="/algorithm">New</el-menu-item>
            <el-menu-item index="/result">Result</el-menu-item>
          </el-submenu>
          <el-menu-item index="/datamanagement" v-if="s===0" disabled><h1>Management</h1></el-menu-item>
          <el-menu-item index="/datamanagement" v-if="s===1"><h1>Management</h1></el-menu-item>
          <el-menu-item index="/"><a href="https://weibo.com/u/5444905621?refer_flag=1001030101_&is_hot=1" target="_blank"><h1>Contact me <img src="../../assets/images/heart.gif" height="50" width="50"/></h1></a></el-menu-item>
        </el-menu>
        <el-button type="warning" style="margin-left:30%" @click="logout()">logout</el-button>
      </el-container>
    </div>
</template>
<style>
  .h1 {
    font-family: Comic Sans MS;
    font-size:20px;
  }
  .div {
    font-size: 1.75em;
		letter-spacing: 6px;
		margin-top: 10px;
  }
</style>
<script>
  export default {
    name: 'header',
    data() {
      return {
        s: 0,
      }
    },
    mounted: function() {
      this.get_authority()
    },
    methods: {
      get_authority() {
        if (sessionStorage.getItem('authority') == 'true') {
            this.s = 1
        }
       },
      handleSelect(key, keyPath) {
        console.log(key, keyPath);
      },
      logout() {
        sessionStorage.clear()
        this.$router.push({ path: '/login' })
      }
    }
  }
</script>

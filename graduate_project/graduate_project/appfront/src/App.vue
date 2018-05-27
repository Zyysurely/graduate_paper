<template>
<router-view @userSignIn="userSignIn"></router-view>
</template>

<script>
export default {
  name: 'app',
  data(){
    return{
      userName: sessionStorage.userName
    }
  },
  methods:{
    userSignIn(userName){
      sessionStorage.userName = userName;
      this.userName = sessionStorage.userName;
    }
  }
}
</script>

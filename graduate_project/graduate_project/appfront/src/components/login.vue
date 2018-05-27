<template>
  <div class="wrapper">
      <div style="margin-left:20%; margin-right:20%; margin-top:8%;">
        <el-carousel :interval="5000" arrow="always">
            <el-carousel-item v-for="item in 4" :key="item">
              <img src="../assets/images/1.jpg"/>
            </el-carousel-item>
        </el-carousel>
      </div>
      <div class="login-container">
      <div id="canvascontainer" ref='can'></div>
        <Form ref="loginForm" autoComplete="on" :model="loginForm" :rules="ruleInline"  class="card-box login-form">
          <FormItem prop="user">
            <Input type="text" v-model="loginForm.user" placeholder="Username">
                <Icon type="ios-person-outline" slot="prepend"></Icon>
            </Input>
          </FormItem>
          <Form-item prop="password">
              <Input type="password" v-model="loginForm.password" placeholder="Password" @keyup.enter.native="handleLogin">
                  <Icon type="ios-locked-outline" slot="prepend"></Icon>
              </Input>
          </Form-item>
          <Form-item>
              <Button type="primary" @click="handleLogin('loginForm')" long>登录</Button>
          </Form-item>
          <div class='tips'>admin账号为:zyy 密码network</div>
              <div class='tips'>editor账号:zhaoyingying 密码network</div>
        </Form>
      </div>
  </div>
</template>
<script>
  import Router from 'vue-router'
  export default {
      name: 'login',
      data () {
        const validateEmail = (rule, value,  callback) => {
          if (!isWscnEmail(value)) {
            callback(new Error('请输入正确的合法邮箱'));
          } else {
            callback();
          }
        };
        var checkAge = (rule, value, callback) => {
          if (!value) {
            return callback(new Error('年龄不能为空'));
          }
          setTimeout(() => {
            if (!Number.isInteger(value)) {
              callback(new Error('请输入数字值'));
            } else {
              if (value < 18) {
                callback(new Error('必须年满18岁'));
              } else {
                callback();
              }
            }
          }, 1000);
        };
        var validatePass = (rule, value, callback) => {
          if (value === '') {
            callback(new Error('请输入密码'));
          } else {
            if (this.ruleForm2.checkPass !== '') {
              this.$refs.ruleForm2.validateField('checkPass');
            }
            callback();
          }
      };
      var validatePass2 = (rule, value, callback) => {
        if (value === '') {
          callback(new Error('请再次输入密码'));
        } else if (value !== this.ruleForm2.pass) {
          callback(new Error('两次输入密码不一致!'));
        } else {
          callback();
        }
      };
      return {
        loginForm: {
            user: '',
            password: ''
        },
        ruleInline: {
            user: [
                { required: true, message: 'Please fill in the user name', trigger: 'blur' }
            ],
            password: [
                { required: true, message: 'Please fill in the password.', trigger: 'blur' },
                { type: 'string', min: 6, message: 'The password length cannot be less than 6 bits', trigger: 'blur' }
            ]
        },
        ruleForm2: {
          pass: '',
          checkPass: '',
          age: ''
        },
        rules2: {
          pass: [
            { validator: validatePass, trigger: 'blur' }
          ],
          checkPass: [
            { validator: validatePass2, trigger: 'blur' }
          ],
          age: [
            { validator: checkAge, trigger: 'blur' }
          ]
        },
        loginRules: {
          email: [
              { required: true, trigger: 'blur', validator: validateEmail }
          ],
          password: [
              { required: true, trigger: 'blur', validator: validatePass }
          ]
          },
        loading: false,
        showDialog: false
      }
    },
    mounted () {
    },
    methods: {
      submitForm(formName) {
        this.$refs[formName].validate((valid) => {
          if (valid) {
            alert('submit!');
          } else {
            console.log('error submit!!');
            return false;
          }
        });
      },
      resetForm(formName) {
        this.$refs[formName].resetFields();
      },
      handleLogin(formName){
        this.$http.post('http://127.0.0.1:8000/api/login',
        {name: this.loginForm.user, passwd: this.loginForm.password},
        {emulateJSON: true})
        .then((response) => {
          var res = JSON.parse(response.bodyText)
          if (res.success == 'yes') {
            sessionStorage.setItem('user_name', this.loginForm.user)
            sessionStorage.setItem('authority', res.authority)
            this.$router.push({ path: '/demo' })
          } else {
            return this.$confirm('The password or username you entered is incorrect')
          }
        })
      }
    }
  }
</script>
<style>
  .el-carousel__item h3 {
    color: #475669;
    font-size: 18px;
    opacity: 0.75;
    line-height: 300px;
    margin: 0;
  }
  .demo-ruleForm {
    margin: 40px;
  }
</style>
<style rel="stylesheet/scss" lang="scss">
     .tips{
      font-size: 14px;
      color: #fff;
      margin-bottom: 5px;
    }
    .login-container {
        height: 500px;
        input:-webkit-autofill {
            -webkit-box-shadow: 0 0 0px 1000px #293444 inset !important;
            -webkit-text-fill-color: #fff !important;
        }
        input {
            background: transparent;
            border: 1px solid #2d8cf0;
            -webkit-appearance: none;
            border-radius: 3px;
            padding: 12px 5px 12px 15px;
            color: #eeeeee;
            height: 50px;
        }
        .el-input {
            display: inline-block;
            height: 47px;
            width: 90%;
        }
        .svg-container {
            padding: 6px 5px 6px 15px;
            color: #889aa4;
        }
        .title {
            font-size: 26px;
            font-weight: 400;
            color: #eeeeee;
            margin: 0px auto 40px auto;
            text-align: center;
            font-weight: bold;
        }
        .login-form {
            position: absolute;
            left: 0;
            right: 0;
            width: 400px;
            padding: 35px 35px 15px 35px;
            margin: 120px auto;
        }
        .el-form-item {
            border: 1px solid rgba(255, 255, 255, 0.1);
            background: rgba(0, 0, 0, 0.1);
            border-radius: 5px;
            color: #454545;
        }
        .forget-pwd {
            color: #fff;
        }
    }
</style>

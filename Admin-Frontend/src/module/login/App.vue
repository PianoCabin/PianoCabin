<template>
  <div id="app">
    <el-card class="box-card login-card">
      <el-form class="login-form" :model="login_info" label-position="top" :rules="rules" @submit.native.prevent="login">
        <el-form-item class="login-title">
          <h1>登录</h1>
        </el-form-item>
        <el-form-item class="login-item" label="用户名" prop="username">
          <el-input v-model="login_info.username" placeholder="请输入管理员用户名"></el-input>
        </el-form-item>
        <el-form-item class="login-item" label="密码" prop="password">
          <el-input type="password" v-model="login_info.password" placeholder="请输入管理员密码"></el-input>
        </el-form-item>
        <el-form-item class="login-item">
          <el-button class="help-button" @click.prevent>帮助</el-button>
          <el-button class="login-button" type="primary" @click="login">登录</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script>
  import Utils from "../../common/js/utils"

  export default {
    name: 'app',
    data () {
      return{
        // 登录信息
        login_info: {
          username: '',
          password: ''
        },

        //校验规则
        rules: {
          username : [
            { required: true, message: "用户名不能为空", trigger: 'blur' }
          ],
          password : [
            { required: true, message: "密码不能为空", trigger: 'blur' }
          ]
        }
      }
    },

    created () {
      Utils.get(this, '/a/login/', null, function (_this, res) {
        if(res.code === 1)
          Utils.setURL("room")
      })
    },

    methods: {
      login: function () {
        Utils.post(this, '/a/login/',
          {
            username: this.login_info.username,
            password: this.login_info.password
          },
          function (_this, res) {
            if (res.code === 1) {
              _this.$message.success('登录成功')
              Utils.setURL("room/")
            }
            else if(res.msg)
              _this.$message.error('用户名或密码错误，请重新输入')
        })
      }
    }
  }
</script>

<style>
  .login-card {
    width: 20%;
    min-width: 35rem;
    margin-left: auto;
    margin-right: auto;
    margin-top: 15%;
  }

  .login-item {
    width: 70%;
    color: #940085 !important;
    margin-left: auto;
    margin-right: auto;
    margin-top: 5%;
  }

  .login-title {
    text-align: center;
    margin-top: 5%;
  }

  .help-button {
    border: None !important;
    color: #940085 !important;
    font-weight: 800 !important;
  }

  .login-button {
    margin-left: 55% !important;
  }

  label {
    font-size: small !important;
    color: #940085 !important;
  }
</style>

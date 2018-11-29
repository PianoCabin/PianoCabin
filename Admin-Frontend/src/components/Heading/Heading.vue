<!--部件用作网页顶部标题栏-->
<template>
    <div class="heading">
      <el-row justify="center">
        <el-header class="head-title">琴屋管理员</el-header>
        <el-button class="head-button" @click="logout">登出</el-button>
        <el-button class="head-button">账号</el-button>
        <el-button class="head-button left">头像</el-button>
      </el-row>
      <el-row><hr class="segment-line" noshade=true/></el-row>
    </div>
</template>

<script>
    import Utils from "../../common/js/utils"

    export default {
        name: "heading",
        methods : {
          logout: function () {
            Utils.post(this, "/a/logout/", null, function (_this, res) {
              Utils.setURL('login/')
            })
          }
        }
    }
</script>

<style scoped>
  .heading {
    margin-top: 2rem;
  }

  .head-button {
    width: 5rem !important;
    float: right;
    margin-left: 2rem !important;
    border: None !important;
    color: #940085 !important;
    font-weight: 800 !important;
    font-size: large;
  }

  .head-title {
    width: 15rem !important;
    float: left;
    text-align: left;
    font-size: xx-large;
    color: #7D7979;
    margin-left: 2.5rem;
  }

  .segment-line {
    border-color: #eceff1;
  }
</style>

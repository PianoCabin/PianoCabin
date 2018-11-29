<!--部件用作侧边栏-->
<template>
    <div class="side-bar">
      <el-menu :default-active="activated" class="menu" @select="menuSelected">
        <el-menu-item index="1" class="menu-item">
          <i class="el-icon-menu"></i>
          <span>琴房管理</span>
        </el-menu-item>
        <el-menu-item index="2" class="menu-item">
          <i class="el-icon-edit"></i>
          <span>订单管理</span>
        </el-menu-item>
        <el-menu-item index="3" class="menu-item">
          <i class="el-icon-message"></i>
          <span>消息管理</span>
        </el-menu-item>
        <el-menu-item index="4" class="menu-item">
          <i class="el-icon-service"></i>
          <span>反馈管理</span>
        </el-menu-item>
      </el-menu>
    </div>
</template>

<script>
  import Utils from "../../common/js/utils"

  export default {
    name: "side-bar",

    props: ["activated"],
    
    methods: {
      menuSelected : function (index) {
        switch (index) {
          case "1":
            Utils.setURL('room/');
            break;
          case "2":
            Utils.setURL('order/');
            break;
          case "3":
            Utils.setURL('news/');
            break;
          case "4":
            Utils.setURL('feedback/');
            break;
          default:
            break;
        }
      }
    }
  }
</script>

<style scoped>
  .menu {
    border: None !important;
    text-align: center;
  }

  .menu-item {
    font-size: medium;
  }
</style>

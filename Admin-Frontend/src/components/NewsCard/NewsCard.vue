<!--部件用作消息、反馈信息卡片-->
<template>
  <div id="news-card">
    <el-card class="box-card">
      <!--slot用于插入标题-->
      <el-row class="title"><h1><slot name="title"></slot></h1></el-row>
      <el-row><hr class="segment-line" noshade=true/></el-row>
      <el-row class="publish-time">
        <!--slot用于插入发布人(反馈卡片使用)-->
        <el-col :span="8" class="news-info publisher"><slot name="publisher">&nbsp</slot></el-col>
        <!--slot用于插入发布时间-->
        <el-col :span="8" class="news-info">发布时间：<slot name="publish-time"></slot></el-col>
        <!--slot用于插入阅读状态(反馈卡片使用)-->
        <el-col :span="8" class="news-info status"><slot name="status">&nbsp</slot></el-col>
      </el-row>
    </el-card>
  </div>
</template>

<script>
  export default {
    name: "news-card"
  }
</script>

<style scoped>
  .box-card {
    height: 11rem;
  }

  .title {
    text-align: center;
  }

  .segment-line {
    width: 10% !important;
    height: 2px;
    background-color: #8E2781;
    border-color: #8E2781;
    margin-left: auto;
    margin-right: auto;
  }

  .news-info {
    min-width: 30px !important;
    text-align: center !important;
  }

  .publish-time {
    text-align: center;
    margin-top: 10px;
  }

  .publisher {
    /*text-align: right !important;*/
  }

  .status {
    /*text-align: left !important;*/
    color: #8e2781 !important;
    font-weight: bold !important;
  }
</style>

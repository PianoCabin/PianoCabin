<template>
  <div id="app">
    <!--顶部标题栏-->
    <heading></heading>

    <el-container>
      <!--侧边导航栏-->
      <el-aside width="18rem"><side-bar activated="1" class="side-bar"></side-bar></el-aside>

      <!--主内容区-->
      <el-main>
        <!--编辑详情区-->
        <div class="feedback-card">

          <!--反馈详情卡片区-->
          <el-card class="feedback-card">
            <el-row class="title"><h1>{{feedback_detail.feedback_title}}</h1></el-row>
            <el-row><hr class="inner-segment-line" noshade=true/></el-row>
            <el-row class="info">
              <el-col :span="12" class="publisher">发布人：{{feedback_detail.user_id}}</el-col>
              <el-col :span="12" class="publish-time">发布时间：{{feedback_detail.feedback_time | getFullTime}}</el-col>
            </el-row>
            <el-row><div class="feedback-content">{{feedback_detail.feedback_content}}</div></el-row>
          </el-card>

          <!--返回按钮-->
          <el-button class="return-button" @click="returnToFeedback"></el-button>
        </div>
      </el-main>
    </el-container>

  </div>
</template>

<script>
  import Heading from '../../components/Heading/Heading'
  import SideBar from "../../components/SideBar/SideBar"
  import Utils from "../../common/js/utils"
  import * as Vue from "vue";

  Vue.filter('getFullTime', function (timestamp) {
    return new Date(parseFloat(timestamp) * 1000).toLocaleString()
  })

  export default {
    name: 'app',
    components: {
      SideBar,
      Heading
    },

    created() {
      let len = window.location.href.split('/').length
      let feedback_id = window.location.href.split('/')[len - 2].split('@')[1]
      console.log(feedback_id);
      Utils.get(this, '/a/feedback/detail?feedback_id=' + feedback_id, null, function (_this, res) {
        if (res.code === 0) {
          _this.$message.error("获取反馈详细信息失败")
          Utils.setURL('feedback/')
        } else {
          console.log(res.data)
          _this.feedback_detail = res.data
        }
      })
    },

    data() {
      return {
        feedback_detail: {
          user_id: '',
          feedback_time: new Date().toLocaleString(),
          feedback_content: '',
          feedback_title: ''
        }
      }
    },

    methods: {
      returnToFeedback: function () {
        Utils.setURL('feedback/')
      }
    }
  }
</script>

<style>
  .side-bar {
    margin-right: 1rem;
    min-width: 13rem;
  }

  .feedback-card {
    width: 50%;
    min-width: 60rem;
    margin-right: auto;
    margin-left: auto;
  }

  .title {
    text-align: center;
  }

  .inner-segment-line {
    width: 10% !important;
    height: 2px;
    background-color: #8E2781;
    border-color: #8E2781;
    margin-left: auto;
    margin-right: auto;
  }

  .info {
    margin-top: 2rem;
    text-align: center;
  }

  .feedback-content {
    min-height: 15rem;
    margin-top: 5rem;
    margin-left: 2rem;
    margin-right: auto;
  }

  .return-button {
    width: 4rem;
    height: 4rem;
    border-radius: 4rem !important;
    background: #ffffff url("./images/back_icon.png") center center no-repeat !important;
    box-shadow: 1px 1px 1px #888888;
    margin-left: 50% !important;
    margin-right: auto !important;
    margin-top: 2rem !important;
  }
</style>

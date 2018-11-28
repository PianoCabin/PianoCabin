<template>
  <div id="app">
    <heading></heading>

    <el-container>
      <el-aside width="18rem"><side-bar activated="4" class="side-bar"></side-bar></el-aside>

      <el-main>
        <div class="content select-panel">
          <el-tabs v-model="activated" @tab-click="handleTabClick">
            <el-tab-pane label="全部" name="0">
              <news-card @click="getDetail" class="news-card" v-for="feedback in feedback_list.slice(page_start,page_end)">
                <nobr slot="title">{{feedback.feedback_title}}</nobr>
                <nobr slot="publisher">{{feedback.user_id}}</nobr>
                <nobr slot="publish-time">{{feedback.time|getDate}}&nbsp{{feedback.time|getTime}}</nobr>
                <nobr slot="status">{{feedback.read_status|read_status}}</nobr>
                <nobr slot="card-id">{{feedback.feedback_id}}</nobr>
              </news-card>
            </el-tab-pane>
            <el-tab-pane label="已读" name="1">
              <news-card @click="getDetail" class="news-card" v-for="feedback in read_feedback_list.slice(page_start,page_end)">
                <nobr slot="title">{{feedback.feedback_title}}</nobr>
                <nobr slot="publisher">{{feedback.user_id}}</nobr>
                <nobr slot="publish-time">{{feedback.time|getDate}}&nbsp{{feedback.time|getTime}}</nobr>
                <nobr slot="status">{{feedback.read_status|read_status}}</nobr>
                <nobr slot="card-id">{{feedback.feedback_id}}</nobr>
              </news-card>
            </el-tab-pane>
            <el-tab-pane label="未读" name="2">
              <news-card @click="getDetail" class="news-card" v-for="feedback in unread_feedback_list.slice(page_start,page_end)">
                <nobr slot="title">{{feedback.feedback_title}}</nobr>
                <nobr slot="publisher">{{feedback.user_id}}</nobr>
                <nobr slot="publish-time">{{feedback.time|getDate}}&nbsp{{feedback.time|getTime}}</nobr>
                <nobr slot="status">{{feedback.read_status|read_status}}</nobr>
                <nobr slot="card-id">{{feedback.feedback_id}}</nobr>
              </news-card>
            </el-tab-pane>
          </el-tabs>
        </div>
        <!--<el-button class="fab" type="primary">+</el-button>-->
        <div class="pagination-div">
          <el-pagination
            @current-change="handlePageChange"
            :current-page.sync="current_page"
            :page-size="page_size"
            layout="prev, pager, next, jumper"
            :total="total_len"
            class="pagination">
          </el-pagination>
        </div>
      </el-main>
    </el-container>
  </div>
</template>

<script>
  import OrderCard from "../../components/OrderCard/OrderCard"
  import Heading from "../../components/Heading/Heading"
  import SideBar from "../../components/SideBar/SideBar"
  import NewsCard from "../../components/NewsCard/NewsCard"
  import * as Vue from "vue";
  import Utils from "../../common/js/utils"

  Vue.filter('read_status',function (int) {
    if (int === 1)
      return "已读"
    else
      return "未读"
  })

  Vue.filter('getDate', function (timestamp) {
    let time = new Date(parseFloat(timestamp) * 1000)
    let year = time.getFullYear().toString()
    let month = (time.getMonth() + 1).toString()
    let date = time.getDate().toString()
    return [year, month, date].join('-')
  })

  // 根据时间戳获取时间
  Vue.filter('getTime', function (timestamp) {
    let time = new Date(parseFloat(timestamp) * 1000)
    let hour = time.getHours().toString()
    let minute = time.getMinutes().toString()
    return [hour, minute].join(':')
  })

  export default {
    name: "App",
    components: {NewsCard, SideBar, Heading, OrderCard},
    created(){
      Utils.get(this,"/a/feedback/list/",null,function (_this,res) {
        if(res.code === 0){
          _this.$message.error("获取反馈失败")
        }
        else{
          console.log(res)
          _this.feedback_list = res.data.feedback_list
          let len = _this.feedback_list.length

          _this.total_len = len
          _this.page_start = 0
          _this.page_end = Math.min(_this.page_size,len)

          for(let i = 0; i < len ; i++){
            switch (_this.feedback_list[i].read_status) {
              case 0:
                _this.unread_feedback_list.push(_this.feedback_list[i]);
                break
              case 1:
                _this.read_feedback_list.push(_this.feedback_list[i]);
                break
              default:
                break
            }
          }
        }
      })
    },
    data () {
      return {
        activated: "0",

        current_page: 1,

        total_len: 0,

        page_start: 0,

        page_end: 0,

        page_size: 10,

        feedback_list: [],

        read_feedback_list: [],

        unread_feedback_list: []
      }
    },

    methods: {
      handlePageChange : function (val) {
        // TO DO
        this.page_start = (val - 1) * this.page_size
        switch (this.activated) {
          case "0":
            this.total_len = this.feedback_list.length
            this.page_end = Math.min(this.page_start + this.page_size,this.feedback_list.length)
            break
          case "1":
            this.total_len = this.read_feedback_list.length
            this.page_end = Math.min(this.page_start + this.page_size,this.read_feedback_list.length)
            break
          case "2":
            this.total_len = this.unread_feedback_list.length
            this.page_start = Math.min(this.page_start + this.page_size,this.unread_feedback_list.length)
            break
          default:
            break
        }
      },
      handleTabClick : function (tab,event) {
        this.current_page = 1
        this.page_start = 0
        switch (tab.name) {
          case "0":
            this.total_len = this.feedback_list.length
            this.page_end = Math.min(this.feedback_list.length,this.page_size)
            break
          case "1":
            this.total_len = this.read_feedback_list.length
            this.page_end = Math.min(this.read_feedback_list.length,this.page_size)
            break
          case "2":
            this.total_len = this.unread_feedback_list.length
            this.page_end = Math.min(this.unread_feedback_list.length,this.page_size)
            break
          default:
            break
        }
      },
      getDetail(feedback_id){
        console.log(feedback_id);
        Utils.get(this,'/a/feedback/detail?feedback_id='+feedback_id,null,function (_this,res) {
          if(res.code === 0){
            _this.$message.error("获取反馈详细信息失败")
          }
          else{
            console.log(res.data)
          }

        })
      }
    }
  }
</script>

<style scoped>
  .side-bar {
    margin-right: 1rem;
    min-width: 13rem;
  }

  .select-panel div {
    font-size: medium !important;
  }

  .news-card {
    width: 50%;
    min-width: 50rem;
    margin: 2rem auto 1rem;
  }

  .fab {
    width: 5rem;
    height: 5rem;
    border-radius: 5rem;
    font-size: 3rem;
    box-shadow: 2px 2px 2px #888888;
    position: fixed;
    bottom: 4rem;
    right: 4rem;
  }

  .pagination-div {
    position: relative;
    top: 2rem;
    width: 100%;
  }

  .pagination {
    width: fit-content !important;
    margin:0 auto !important;
  }
</style>

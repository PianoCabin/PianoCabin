<template>
  <div id="app">
    <heading></heading>
    <el-container>
      <el-aside width="18rem"><side-bar activated="3" class="side-bar"></side-bar></el-aside>
      <el-main>
        <div class="content select-panel">
          <news-card @click="getDetail" v-for="news in news_list.slice(page_start,page_end)" class="news-card">
            <nobr slot="title">{{news.news_title}}</nobr>
            <nobr slot="publish-time">{{news.publish_time | getDate}} &nbsp; {{news.publish_time | getTime}}</nobr>
            <template slot="card-id">{{news.news_id}}</template>
          </news-card>
        </div>
        <el-button @click="createNews" class="fab" type="primary">+</el-button>
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
  import * as Vue from "vue"
  import Utils from "../../common/js/utils"

  // 根据时间戳获取日期
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
    components: {
      NewsCard,
      SideBar,
      Heading,
      OrderCard
    },

    created(){
      Utils.get(this,'/a/news/list',null,function (_this,res) {
        if(res.code === 0)
          _this.$message.error("获取消息失败")
        else {
          console.log(res)
          _this.news_list = res.data.news_list

          let len = _this.news_list.length

          _this.total_len = len
          _this.page_start = 0
          _this.page_end = Math.min(_this.page_size,len)
        }
      })
    },
    data () {
      return {
        current_page: 1,

        total_len: 0,

        page_start: 0,

        page_end: 0,

        page_size: 10,

        news_list:[],
      }
    },

    methods: {
      handlePageChange : function (val) {
        // TO DO
        this.page_start = (val - 1) * this.page_size
        this.page_end = Math.min(this.news_list.length,this.page_start + this.page_size)
      },
      createNews(){
        Utils.setURL('news-create@$/');
      },
      getDetail(news_id){
        console.log(news_id);
        Utils.setURL('news-create@'+news_id+'/')
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

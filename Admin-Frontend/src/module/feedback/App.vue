<template>
  <div id="app">
    <heading></heading>
    <el-container>
      <el-aside width="18rem"><side-bar activated="4" class="side-bar"></side-bar></el-aside>
      <el-main>
        <div class="content select-panel">
          <el-tabs v-model="activated">
            <el-tab-pane label="全部" name="0"></el-tab-pane>
            <el-tab-pane label="已读" name="1">
              <news-card class="news-card">
                <nobr slot="title">关于国庆节琴房使用的通知</nobr>
                <nobr slot="publisher">aaaaaaaaaaaaaaaaaaaaaaaaaaaa</nobr>
                <nobr slot="publish-time">2018/09/30 16:00</nobr>
                <nobr slot="status">消息未读</nobr>
              </news-card>
            </el-tab-pane>
            <el-tab-pane label="未读" name="2"></el-tab-pane>
          </el-tabs>
        </div>
        <el-button class="fab" type="primary">+</el-button>
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
  export default {
    name: "App",
    components: {NewsCard, SideBar, Heading, OrderCard},
    data () {
      return {
        activated: "0",

        current_page: 1,

        total_len: 0,

        page_start: 0,

        page_end: 0,

        page_size: 10
      }
    },

    methods: {
      handlePageChange : function () {
        // TO DO
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
    position: fixed;
    bottom: 2rem;
    left: 18rem;
    width: calc(100vw - 18rem) !important;
  }

  .pagination {
    width: fit-content !important;
    margin:0 auto !important;
  }
</style>

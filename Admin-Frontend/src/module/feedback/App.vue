<template>
  <div id="app">
    <heading></heading>

    <el-container>
      <el-aside width="18rem">
        <side-bar activated="4" class="side-bar"></side-bar>
      </el-aside>

      <el-main>
        <div class="content select-panel">
          <el-tabs v-model="activated" @tab-click="handleTabClick">
            <el-tab-pane label="全部" name="0">
              <el-table :data="feedback_list.slice(page_start,page_end)" style="width: 100%" highlight-current-row
                        @row-click="getDetail">
                <el-table-column prop="user_id" label="反馈人" width="300"></el-table-column>
                <el-table-column prop="feedback_title" label="标题" width="250"></el-table-column>
                <el-table-column label="内容" width="600">
                  <template slot-scope="scope"><p class="feedback-content">{{ scope.row.feedback_content }}</p></template>
                </el-table-column>
                <el-table-column label="反馈时间" width="220">
                  <template slot-scope="scope"><p>{{ scope.row.feedback_time | getFullTime}}</p></template>
                </el-table-column>
                <el-table-column label="阅读情况" width="100">
                  <template slot-scope="scope"><p>{{ scope.row.read_status | getStatus}}</p></template>
                </el-table-column>
                <el-table-column class-name="feedback-id" prop="feedback_id" width="0"></el-table-column>
              </el-table>
            </el-tab-pane>
            <el-tab-pane label="已读" name="1">
              <el-table :data="read_feedback_list.slice(page_start,page_end)" style="width: 100%" highlight-current-row
                        @row-click="getDetail">
                <el-table-column prop="user_id" label="反馈人" width="300"></el-table-column>
                <el-table-column prop="feedback_title" label="标题" width="250"></el-table-column>
                <el-table-column label="内容" width="600">
                  <template slot-scope="scope"><p class="feedback-content">{{ scope.row.feedback_content }}</p></template>
                </el-table-column>
                <el-table-column label="反馈时间" width="220">
                  <template slot-scope="scope"><p>{{ scope.row.feedback_time | getFullTime}}</p></template>
                </el-table-column>
                <el-table-column label="阅读情况" width="100">
                  <template slot-scope="scope"><p>{{ scope.row.read_status | getStatus}}</p></template>
                </el-table-column>
                <el-table-column class-name="feedback-id" prop="feedback_id" width="0"></el-table-column>
              </el-table>
            </el-tab-pane>
            <el-tab-pane label="未读" name="2">
              <el-table :data="unread_feedback_list.slice(page_start,page_end)" style="width: 100%" highlight-current-row
                        @row-click="getDetail">
                <el-table-column prop="user_id" label="反馈人" width="300"></el-table-column>
                <el-table-column prop="feedback_title" label="标题" width="250"></el-table-column>
                <el-table-column label="内容" width="600">
                  <template slot-scope="scope"><p class="feedback-content">{{ scope.row.feedback_content }}</p></template>
                </el-table-column>
                <el-table-column label="反馈时间" width="220">
                  <template slot-scope="scope"><p>{{ scope.row.feedback_time | getFullTime}}</p></template>
                </el-table-column>
                <el-table-column label="阅读情况" width="100">
                  <template slot-scope="scope"><p>{{ scope.row.read_status | getStatus}}</p></template>
                </el-table-column>
                <el-table-column class-name="feedback-id" prop="feedback_id" width="0"></el-table-column>
              </el-table>
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

  // 获取阅读状态文字
  Vue.filter('getStatus', function (val) {
    return val ? "已读" : "未读"
  })

  // 获取完整时间
  Vue.filter('getFullTime', function (timestamp) {
    return new Date(parseFloat(timestamp) * 1000).toLocaleString()
  })

  export default {
    name: "App",
    components: {NewsCard, SideBar, Heading, OrderCard},
    created() {
      Utils.get(this, "/a/feedback/list/", null, function (_this, res) {
        if (res.code === 0) {
          _this.$message.error("获取反馈失败")
        }
        else {
          console.log(res)
          _this.feedback_list = res.data.feedback_list
          let len = _this.feedback_list.length

          _this.total_len = len
          _this.page_start = 0
          _this.page_end = Math.min(_this.page_size, len)

          for (let i = 0; i < len; i++) {
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
    data() {
      return {
        activated: "0",

        current_page: 1,

        total_len: 0,

        page_start: 0,

        page_end: 2,

        page_size: 10,

        feedback_list: [],

        read_feedback_list: [],

        unread_feedback_list: []
      }
    },

    methods: {
      handlePageChange: function (val) {
        // TO DO
        this.page_start = (val - 1) * this.page_size
        switch (this.activated) {
          case "0":
            this.total_len = this.feedback_list.length
            this.page_end = Math.min(this.page_start + this.page_size, this.feedback_list.length)
            break
          case "1":
            this.total_len = this.read_feedback_list.length
            this.page_end = Math.min(this.page_start + this.page_size, this.read_feedback_list.length)
            break
          case "2":
            this.total_len = this.unread_feedback_list.length
            this.page_start = Math.min(this.page_start + this.page_size, this.unread_feedback_list.length)
            break
          default:
            break
        }
      },
      handleTabClick: function (tab, event) {
        this.current_page = 1
        this.page_start = 0
        switch (tab.name) {
          case "0":
            this.total_len = this.feedback_list.length
            this.page_end = Math.min(this.feedback_list.length, this.page_size)
            break
          case "1":
            this.total_len = this.read_feedback_list.length
            this.page_end = Math.min(this.read_feedback_list.length, this.page_size)
            break
          case "2":
            this.total_len = this.unread_feedback_list.length
            this.page_end = Math.min(this.unread_feedback_list.length, this.page_size)
            break
          default:
            break
        }
      },

      // 响应单行点击
      getDetail(row, event, column) {
        let feedback_id = parseInt(event.currentTarget.getElementsByClassName('feedback-id')[0].innerText)
        Utils.get(this, '/a/feedback/detail?feedback_id=' + feedback_id, null, function (_this, res) {
          if (res.code === 0) {
            _this.$message.error("获取反馈详细信息失败")
          } else {
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

  .pagination-div {
    position: relative;
    top: 2rem;
    width: 100%;
  }

  .pagination {
    width: fit-content !important;
    margin: 0 auto !important;
  }

  .feedback-content {
    white-space: nowrap !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
  }
</style>

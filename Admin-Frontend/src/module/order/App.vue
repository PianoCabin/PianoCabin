<template>
  <div id="app">
    <heading></heading>

    <el-container>
      <el-aside width="18rem">
        <side-bar activated="2" class="side-bar"></side-bar>
      </el-aside>

      <el-main>
        <div class="filter">
          <el-row>
            <div class="search-item fl">
              <span>订单编号：</span>
              <el-input @blur="handleFilter" class="info" v-model="filter_info.order_id" placeholder="请输入订单编号">
              </el-input>
            </div>
            <div class="search-item fl">
              <span>琴房房号：</span>
              <el-input @blur="handleFilter" class="info" v-model="filter_info.room_num" placeholder="请输入琴房房号">
              </el-input>
            </div>
          </el-row>
          <el-row>
            <div class="search-item fl">
              <el-select value="0" v-model="id_type_selected" style="width: 7rem">
                <el-option key="0" value="0" label="学号工号："></el-option>
                <el-option key="1" value="1" label="微信ID："></el-option>
              </el-select>
              <el-input @blur="handleFilter" class="info" v-model="filter_info.user_id" placeholder="请输入订单编号"></el-input>
            </div>
            <div class="search-item fl">
              <span>下单时间：</span>
              <el-date-picker :default-time="['00:00:00', '23:59:59']" @blur="handleFilter" v-model="date_range" type="daterange" range-separator="至" start-placeholder="开始日期" end-placeholder="结束日期">
              </el-date-picker>
            </div>
          </el-row>
        </div>
        <div class="content select-panel">
          <el-tabs v-model="activated" @tab-click="handleTabClick">
            <el-tab-pane label="全部" name="0">
              <order-card v-for="order in order_list.slice(page_start, page_end)" class="order-card">
                <nobr slot="brand">{{order.brand}}</nobr>
                <nobr slot="room-num">{{order.room_num}}</nobr>
                <nobr slot="user-id">{{order.user_id}}</nobr>
                <nobr slot="order-id">{{order.order_id}}</nobr>
                <nobr slot="order-time">{{order.start_time | getDate}}&nbsp{{order.start_time | getTime}} ~
                  {{order.end_time | getTime}}
                </nobr>
                <nobr slot="create-time">{{order.create_time | getFullTime}}</nobr>
                <nobr slot="order-state">{{order.order_status | getStatus}}</nobr>
                <nobr slot="price">{{order.price}}</nobr>
              </order-card>
            </el-tab-pane>
            <el-tab-pane label="已完成" name="1">
              <order-card v-for="order in finished_order_list.slice(page_start, page_end)" class="order-card">
                <nobr slot="brand">{{order.brand}}</nobr>
                <nobr slot="room-num">{{order.room_num}}</nobr>
                <nobr slot="user-id">{{order.user_id}}</nobr>
                <nobr slot="order-id">{{order.order_id}}</nobr>
                <nobr slot="order-time">{{order.start_time | getDate}}&nbsp{{order.start_time | getTime}} ~
                  {{order.end_time | getTime}}
                </nobr>
                <nobr slot="create-time">{{order.create_time | getFullTime}}</nobr>
                <nobr slot="order-state">{{order.order_status | getStatus}}</nobr>
                <nobr slot="price">{{order.price}}</nobr>
              </order-card>
            </el-tab-pane>
            <el-tab-pane label="已支付" name="2">
              <order-card v-for="order in paid_order_list.slice(page_start, page_end)" class="order-card">
                <nobr slot="brand">{{order.brand}}</nobr>
                <nobr slot="room-num">{{order.room_num}}</nobr>
                <nobr slot="user-id">{{order.user_id}}</nobr>
                <nobr slot="order-id">{{order.order_id}}</nobr>
                <nobr slot="order-time">{{order.start_time | getDate}}&nbsp{{order.start_time | getTime}} ~
                  {{order.end_time | getTime}}
                </nobr>
                <nobr slot="create-time">{{order.create_time | getFullTime}}</nobr>
                <nobr slot="order-state">{{order.order_status | getStatus}}</nobr>
                <nobr slot="price">{{order.price}}</nobr>
              </order-card>
            </el-tab-pane>
            <el-tab-pane label="未支付" name="3">
              <order-card v-for="order in unpaid_order_list.slice(page_start, page_end)" class="order-card">
                <nobr slot="brand">{{order.brand}}</nobr>
                <nobr slot="room-num">{{order.room_num}}</nobr>
                <nobr slot="user-id">{{order.user_id}}</nobr>
                <nobr slot="order-id">{{order.order_id}}</nobr>
                <nobr slot="order-time">{{order.start_time | getDate}}&nbsp{{order.start_time | getTime}} ~
                  {{order.end_time | getTime}}
                </nobr>
                <nobr slot="create-time">{{order.create_time | getFullTime}}</nobr>
                <nobr slot="order-state">{{order.order_status | getStatus}}</nobr>
                <nobr slot="price">{{order.price}}</nobr>
              </order-card>
            </el-tab-pane>
            <el-tab-pane label="已取消" name="4">
              <order-card v-for="order in canceled_order_list.slice(page_start, page_end)" class="order-card">
                <nobr slot="brand">{{order.brand}}</nobr>
                <nobr slot="room-num">{{order.room_num}}</nobr>
                <nobr slot="user-id">{{order.user_id}}</nobr>
                <nobr slot="order-id">{{order.order_id}}</nobr>
                <nobr slot="order-time">{{order.start_time | getDate}}&nbsp{{order.start_time | getTime}} ~
                  {{order.end_time | getTime}}
                </nobr>
                <nobr slot="create-time">{{order.create_time | getFullTime}}</nobr>
                <nobr slot="order-state">{{order.order_status | getStatus}}</nobr>
                <nobr slot="price">{{order.price}}</nobr>
              </order-card>
            </el-tab-pane>
          </el-tabs>
        </div>

        <!--页面切换区-->
        <el-footer>
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
        </el-footer>
      </el-main>
    </el-container>
  </div>
</template>

<script>
  import OrderCard from "../../components/OrderCard/OrderCard"
  import Heading from "../../components/Heading/Heading"
  import SideBar from "../../components/SideBar/SideBar"
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

  // 获取完整时间
  Vue.filter('getFullTime', function (timestamp) {
    return new Date(parseFloat(timestamp) * 1000).toLocaleString()
  })

  Vue.filter('getStatus', function (status) {
    switch (status) {
      case 0:
        return "已取消";
      case 1:
        return "未支付"
      case 2:
        return "已支付"
      case 3:
        return "已完成"
      default:
        break
    }
  })

  export default {
    name: "App",
    components: {SideBar, Heading, OrderCard},

    created() {
      Utils.post(this, '/a/order/list/', null, function (_this, res) {
        if (res.code === 0)
          _this.$message.error("获取订单失败")
        else {
          _this.order_list = res.data.order_list
          let len = _this.order_list.length

          _this.total_len = len
          _this.page_start = 0
          _this.page_end = len < _this.page_size ? len : _this.page_size

          for (let i = 0; i < len; i++) {
            switch (_this.order_list[i].order_status) {
              case 0:
                _this.canceled_order_list.push(_this.order_list[i]);
                break;
              case 1:
                _this.unpaid_order_list.push(_this.order_list[i]);
                break;
              case 2:
                _this.paid_order_list.push(_this.order_list[i]);
                break;
              case 3:
                _this.finished_order_list.push(_this.order_list[i]);
                break;
              default:
                break;
            }
          }
        }
      })
    },

    data() {
      return {
        activated: "0",

        order_list: [],

        finished_order_list: [],

        paid_order_list: [],

        unpaid_order_list: [],

        canceled_order_list: [],

        // 当前页
        current_page: 1,

        // 总的元素个数
        total_len: 0,

        // 本页起始元素index
        page_start: 0,

        // 本页结束元素index
        page_end: 0,

        // 单页元素个数
        page_size: 10,

        // 筛选信息
        filter_info: {
          order_id: '',
          room_num: '',
          user_id: ''
        },

        // 选择用于筛选的id类型
        id_type_selected: "0",

        // 订单日期范围
        date_range: null
      }
    },

    methods: {
      // 响应标签栏点击
      handleTabClick: function (tab, event) {
        this.current_page = 1
        this.page_start = 0
        switch (tab.name) {
          case "0":
            this.total_len = this.order_list.length
            this.page_end = this.order_list.length < this.page_size ? this.order_list.length : this.page_size;
            break;
          case "1":
            this.total_len = this.finished_order_list.length
            this.page_end = this.finished_order_list.length < this.page_size ? this.finished_order_list.length : this.page_size;
            break;
          case "2":
            this.total_len = this.paid_order_list.length
            this.page_end = this.paid_order_list.length < this.page_size ? this.paid_order_list.length : this.page_size;
            break;
          case "3":
            this.total_len = this.unpaid_order_list.length
            this.page_end = this.unpaid_order_list.length < this.page_size ? this.unpaid_order_list.length : this.page_size;
            break;
          case "4":
            this.total_len = this.canceled_order_list.length
            this.page_end = this.canceled_order_list.length < this.page_size ? this.canceled_order_list.length : this.page_size;
            break;
          default:
            break;
        }
      },

      // 响应页面切换
      handlePageChange: function (val) {
        this.page_start = (val - 1) * this.page_size
        switch (this.activated) {
          case "0":
            this.page_end = this.order_list.length < (this.page_start + this.page_size) ? this.order_list.length : (this.page_start + this.page_size);
            break;
          case "1":
            this.page_end = this.finished_order_list.length < (this.page_start + this.page_size) ? this.finished_order_list.length : (this.page_start + this.page_size);
            break;
          case "2":
            this.page_end = this.paid_order_list.length < (this.page_start + this.page_size) ? this.paid_order_list.length : (this.page_start + this.page_size);
            break;
          case "3":
            this.page_end = this.unpaid_order_list.length < (this.page_start + this.page_size) ? this.unpaid_order_list.length : (this.page_start + this.page_size);
            break;
          case "4":
            this.page_end = this.canceled_order_list.length < (this.page_start + this.page_size) ? this.canceled_order_list.length : (this.page_start + this.page_size);
            break;
          default:
            break;
        }
      },

      // 响应筛选条件变化
      handleFilter: function () {
        let data = {}
        let keys = Object.keys(this.filter_info)
        for (let i = 0; i < keys.length; i++) {
          let key = keys[i]
          if (this.filter_info[key] !== '') {
            if (key === 'user_id'){
              if (this.id_type_selected === '0')
                data.identity = this.filter_info.user_id
              else
                data.open_id = this.filter_info.user_id
            }
            else
              data[key] = this.filter_info[key]
          }
        }

        if (this.date_range !== null) {
          data.start_date = this.date_range[0].getTime() / 1000
          data.end_date = this.date_range[1].getTime() / 1000
        }

        Utils.post(this, '/a/order/list/', data, function (_this, res) {
          if (res.code === 0)
            _this.$message.error("获取订单失败")
          else {
            _this.order_list = res.data.order_list
            let len = _this.order_list.length

            for (let i = 0; i < len; i++) {
              switch (_this.order_list[i].order_status) {
                case 0:
                  _this.canceled_order_list.push(_this.order_list[i]);
                  break;
                case 1:
                  _this.unpaid_order_list.push(_this.order_list[i]);
                  break;
                case 2:
                  _this.paid_order_list.push(_this.order_list[i]);
                  break;
                case 3:
                  _this.finished_order_list.push(_this.order_list[i]);
                  break;
                default:
                  break;
              }
            }

            _this.handleTabClick({name: _this.activated})
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

  .order-card {
    width: 50%;
    min-width: 60rem;
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

  .filter {
    margin-bottom: 2rem;
  }

  .search-item {
    width: 30rem;
    margin-top: 2rem;
  }

  .info {
    width: 13rem;
  }

  .fl {
    float: left;
  }
</style>

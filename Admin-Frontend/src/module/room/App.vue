<template>
  <div id="app">
    <!--顶部标题栏-->
    <heading></heading>

    <el-container>
      <!--侧边导航栏-->
      <el-aside width="18rem"><side-bar activated="1" class="side-bar"></side-bar></el-aside>

      <!--主内容区-->
      <el-main>
        <div class="content select-panel">
          <!--琴房类型导航栏-->
          <el-menu :default-active="activated" mode="horizontal" @select="select">
            <el-submenu v-for="(_, key) in room_list" :index="key">
              <template slot="title">{{key}}</template>
              <el-menu-item v-for="(_, sub_key) in room_list[key]" :index="sub_key">{{sub_key}}</el-menu-item>
            </el-submenu>
          </el-menu>

          <!--单房间按钮-->
          <room @click="getDetail" v-for="room in selected_list" class="room">
            <template slot="room-num">{{room.room_num}}</template>
          </room>
        </div>

        <!--新建按钮-->
        <el-button @click="createRoom" class="fab" type="primary">+</el-button>
      </el-main>
    </el-container>
  </div>
</template>

<script>
  import Heading from '../../components/Heading/Heading'
  import SideBar from "../../components/SideBar/SideBar"
  import Room from "../../components/Room/Room"
  import Utils from "../../common/js/utils"

  export default {
    name: 'app',
    components: {
      Room,
      SideBar,
      Heading
    },

    created() {
      // 初始化琴房信息
      for (let i = 0; i < this.piano_type.length; i++)
        this.$set(this.room_list, this.piano_type[i], {})
      for (let i = 0; i < this.piano_type.length; i++) {
        let piano_type = this.piano_type[i]
        Utils.post(this, "/a/piano-room/list/",
          {
            "piano_type": piano_type
          },
          function (_this, rooms) {
            if (rooms.code === 0) {
              _this.$message.error("请求失败")
              return
            }
            else
              _this.$set(_this.room_list, piano_type, rooms.data["room_list"])

            if (_this.piano_type.length && _this.room_list[_this.piano_type[0]]) {
              if (Object.keys(_this.room_list[_this.piano_type[0]]).length) {
                _this.activated = Object.keys(_this.room_list[_this.piano_type[0]])[0]
                _this.selected_list = _this.room_list[_this.piano_type[0]][_this.activated]
              }
            }
          })
      }
    },

    data() {
      return {
        activated: "",

        // 琴房类型
        piano_type: ["钢琴房", "电钢琴", "小琴房"],

        // 琴房信息列表
        room_list: {},

        // 被选中的琴房信息
        selected_list: []
      }
    },

    methods: {
      // 响应顶部导航栏点击
      select: function (key, key_path) {
        this.selected_list = this.room_list[key_path[0]][key_path[1]]
      },

      // 响应房间图标点击
      getDetail: function (room_num) {
        Utils.setURL('room-detail@' + room_num + '/')
      },

      // 响应添加按钮点击
      createRoom: function () {
        Utils.setURL('room-detail@$/')
      }
    }
  }
</script>

<style>
  .side-bar {
    margin-right: 1rem;
    min-width: 13rem;
  }

  .el-submenu__title {
    font-size: medium !important;
  }

  .room {
    width: 10rem;
    margin-top: 2rem;
    float: left;
    margin-left: 1rem;
  }

  .fab {
    width: 5rem;
    height: 5rem;
    border-radius: 5rem !important;
    font-size: 3rem !important;
    box-shadow: 2px 2px 2px #888888;
    position: fixed;
    bottom: 4rem;
    right: 4rem;
  }
</style>

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
        <div class="edit-card">
          <!--头部紫色信息区-->
          <el-card class="edit-card above">
            <div class="header">
              <h1>{{room_info.brand}}</h1>
              <h2>{{room_info.room_num}}</h2>
            </div>
          </el-card>

          <!--底部主要编辑区-->
          <el-card class="edit-card below">
            <el-form label-width="8rem" class="form" @submit.prevent :rules="rules" :model="room_info" ref="room-edit-form">
              <el-form-item label="名称：" prop="brand">
                <el-input v-model="room_info.brand"></el-input>
              </el-form-item>
              <el-form-item label="房间号：" prop="room_num">
                <el-input :disabled="!new_room" v-model="room_info.room_num"></el-input>
              </el-form-item>
              <el-form-item label="类型：" prop="piano_type">
                <el-select v-model="room_info.piano_type" :placeholder="room_info.piano_type" value="">
                  <el-option v-for="type in piano_type" :label="type" :value="type"></el-option>
                </el-select>
              </el-form-item>
              <el-form-item label="校外人士价格：" prop="price_0">
                <el-col :span="8">
                  <el-input v-model.number="room_info.price_0" :placeholder="room_info.price_0"></el-input>
                </el-col>
                <el-col :span="8" class="price-text">元/小时</el-col>
              </el-form-item>
              <el-form-item label="教职工价格：" prop="price_1">
                <el-col :span="8">
                  <el-input v-model.number="room_info.price_1" :placeholder="room_info.price_1"></el-input>
                </el-col>
                <el-col :span="8" class="price-text">元/小时</el-col>
              </el-form-item>
              <el-form-item label="学生价格：" prop="price_2">
                <el-col :span="8">
                  <el-input v-model.number="room_info.price_2" :placeholder="room_info.price_2"></el-input>
                </el-col>
                <el-col :span="8" class="price-text">元/小时</el-col>
              </el-form-item>
              <el-form-item label="上下线状态：" prop="usable">
                <el-select v-model="room_info.usable" value="">
                  <el-option label="上线" value="上线"></el-option>
                  <el-option label="下线" value="下线"></el-option>
                </el-select>
              </el-form-item>
              <el-form-item label="艺术团属性：" prop="art_ensemble">
                <el-select v-model="room_info.art_ensemble" value="">
                  <el-option label="艺术团" value="艺术团"></el-option>
                  <el-option label="非艺术团" value="非艺术团"></el-option>
                </el-select>
              </el-form-item>
            </el-form>
          </el-card>

          <!--保存按钮-->
          <el-button class="save-button" @click="editRoom"></el-button>

          <!--返回按钮-->
          <el-button class="return-button" @click="returnToRoom"></el-button>
        </div>
      </el-main>
    </el-container>

    <!--保存弹出区-->
    <el-dialog
      title="确认"
      :visible.sync="dialog_visible"
      width="30%">
      <span>确认提交修改？</span>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialog_visible = false">取 消</el-button>
        <el-button type="primary" @click="handleSubmit">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
  import Heading from '../../components/Heading/Heading'
  import SideBar from "../../components/SideBar/SideBar"
  import Utils from "../../common/js/utils"

  export default {
    name: 'app',
    components: {
      SideBar,
      Heading
    },

    created() {
      // 初始化单房间数据
      let len = window.location.href.split('/').length
      let room = window.location.href.split('/')[len - 2].split('@')[1]
      if (room === "$") {
        this.new_room = true
        return
      }
      Utils.post(this, "/a/piano-room/list/",
        {
          room_num: room
        },
        function (_this, res) {
          if (res.code !== 0) {
            let rooms = res.data['room_list']
            if (Object.keys(rooms).length === 0) {
              _this.$message.error("房间不存在")
              Utils.setURL("room/")
              return
            }
            let brand = Object.keys(rooms)[0]
            _this.room_info = rooms[brand][0]
            _this.$set(_this.room_info, "usable", _this.usable_text[_this.room_info.usable])
            _this.$set(_this.room_info, "art_ensemble", _this.art_ensemble_text[_this.room_info.art_ensemble])
          }
        })
    },

    data() {
      return {
        usable_text: {
          true: "上线",
          false: "下线"
        },

        art_ensemble_text: {
          0: "非艺术团",
          1: "艺术团"
        },

        room_info: {
          brand: "未命名",
          room_num: "房间号",
          piano_type: "",
          price_0: 0,
          price_1: 0,
          price_2: 0,
          usable: "上线",
          art_ensemble: "非艺术团"
        },

        piano_type: ["钢琴房", "小琴房", "电钢琴"],

        // 表单校验规则
        rules: {
          brand: [{required: true, message: "请填写名称", trigger: 'blur'}],
          room_num: [{required: true, message: "请填写房间号", trigger: 'blur'}],
          piano_type: [{required: true, message: "请选择琴房类型", trigger: 'blur'}],
          price_0: [
            {required: true, message: "请填写价格", trigger: "blur"},
            {type: "number", message: "价格必须为数字", trigger: "blur"}
          ],
          price_1: [
            {required: true, message: "请填写价格", trigger: "blur"},
            {type: "number", message: "价格必须为数字", trigger: "blur"}
          ],
          price_2: [
            {required: true, message: "请填写价格", trigger: "blur"},
            {type: "number", message: "价格必须为数字", trigger: "blur"}
          ],
          usable: [{required: true, message: "请选择上下线状态", trigger: 'blur'}],
          art_ensemble: [{required: true, message: "请选择艺术团属性", trigger: 'blur'}],
        },

        // 是否为新建房间
        new_room: false,

        // 保存弹出区是否可见
        dialog_visible: false
      }
    },

    methods: {
      // 点击保存按钮
      editRoom: function () {
        let _this = this
        this.$refs['room-edit-form'].validate(function (state, obj) {
          if (state) {
            _this.dialog_visible = true
          }
        })
      },

      // 确认提交修改
      handleSubmit: function () {
        this.dialog_visible = false
        this.room_info.usable = (this.room_info.usable === "上线");
        this.room_info.art_ensemble = this.room_info.art_ensemble === "艺术团" ? 1 : 0
        if (this.new_room) {
          Utils.post(this, '/a/piano-room/create/', this.room_info, function (_this, res) {
            if (res.code === 1)
              Utils.setURL("room/")
            else
              _this.$message.error("提交修改失败")
          })
        } else {
          Utils.post(this, '/a/piano-room/edit/', this.room_info, function (_this, res) {
            if (res.code === 1)
              Utils.setURL("room/")
            else
              _this.$message.error("提交修改失败")
          })
        }
      },

      // 返回首页
      returnToRoom: function () {
        Utils.setURL('room/')
      }
    }
  }
</script>

<style>
  .side-bar {
    margin-right: 1rem;
    min-width: 13rem;
  }

  .above {
    background-color: #940085 !important;

  }

  .edit-card {
    width: 30%;
    min-width: 40rem;
    margin-right: auto;
    margin-left: auto;
  }

  .header {
    margin-left: 3rem;
    color: #ffffff;
  }

  .below {
    margin-bottom: 0 !important;
  }

  .form {
    width: 70%;
    margin-top: 2rem;
  }

  .price-text {
    margin-left: 1rem;
  }

  .save-button {
    width: 4rem;
    height: 4rem;
    border-radius: 4rem !important;
    background: #ffffff url("./images/save_icon.png") center center no-repeat !important;
    background-size: 2rem 2rem !important;
    box-shadow: 2px 2px 2px #888888;
    position: relative;
    bottom: 40rem;
    left: 80%;
  }

  .return-button {
    width: 4rem;
    height: 4rem;
    border-radius: 4rem !important;
    background: #ffffff url("./images/back_icon.png") center center no-repeat !important;
    box-shadow: 1px 1px 1px #888888;
    margin-left: 40% !important;
    margin-right: auto !important;
    margin-top: 2rem !important;
  }
</style>

<template>
  <div id="app">
    <heading></heading>

    <el-container>
      <el-aside width="18rem">
        <side-bar activated="5" class="side-bar"></side-bar>
      </el-aside>

      <el-main>
        <!--筛选条件区-->
        <div class="filter">
          <el-row>
            <div class="search-item fl">
              <span>预约权限：</span>
              <el-select
                @change="handleFilter"
                :value="0"
                v-model="filter_info.order_permission"
                style="width: 7rem"
              >
                <el-option key="2" :value="null" label="所有"></el-option>
                <el-option key="0" :value="true" label="允许"></el-option>
                <el-option key="1" :value="false" label="禁止"></el-option>
              </el-select>
            </div>
            <div class="search-item fl">
              <span>绑定身份：</span>
              <el-select
                @change="handleFilter"
                :value="0"
                v-model="filter_info.permission"
                style="width: 7rem"
              >
                <el-option key="3" :value="null" label="所有"></el-option>
                <el-option key="0" :value="0" label="校外人士"></el-option>
                <el-option key="1" :value="1" label="教职员工"></el-option>
                <el-option key="2" :value="2" label="在校学生"></el-option>
              </el-select>
            </div>
          </el-row>
          <el-row>
            <div class="search-item fl">
              <el-select value="0" v-model="id_type_selected" style="width: 7rem">
                <el-option key="0" value="0" label="学号工号："></el-option>
                <el-option key="1" value="1" label="用户ID："></el-option>
              </el-select>
              <el-input
                @blur="handleFilter"
                @keydown.enter.native="handleFilter"
                class="info"
                v-model="filter_info.user_id"
                placeholder="请输入用户ID"
              ></el-input>
            </div>
            <div class="search-item fl">
              <el-button
                @click="dialog_visible = true"
                class="el-button--primary"
                :disabled="!is_modified"
              >保存修改</el-button>
            </div>
          </el-row>
          <el-row>
            <hr class="line" noshade="true">
          </el-row>
        </div>
        <div class="content">
          <el-table :data="user_list" style="width: 100%">
            <el-table-column prop="user_id" label="用户ID"></el-table-column>
            <el-table-column label="工学号">
              <template slot-scope="scope">{{scope.row.identity | getIdentity }}</template>
            </el-table-column>
            <el-table-column label="绑定身份">
              <template slot-scope="scope">{{scope.row.permission | getPermission }}</template>
            </el-table-column>
            <el-table-column>
              <template slot="header" slot-scope="scope">
                <span>预约权限</span>
                <el-switch
                  @change="selectALlChange"
                  style="height: 50px !important;"
                  v-model="select_all"
                  inactive-color="#ff4949"
                ></el-switch>
              </template>
              <template slot-scope="scope">
                <el-switch
                  @change="selectChange"
                  v-model="user_list[scope.$index].order_permission"
                  inactive-color="#ff4949"
                  active-text="允许"
                  inactive-text="禁止"
                ></el-switch>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </el-main>
    </el-container>

    <!--保存弹出区-->
    <el-dialog title="确认" :visible.sync="dialog_visible" width="30%">
      <span>确认提交修改？</span>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialog_visible = false">取 消</el-button>
        <el-button type="primary" @click="handlePermissionChange">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import OrderCard from "../../components/OrderCard/OrderCard";
import Heading from "../../components/Heading/Heading";
import SideBar from "../../components/SideBar/SideBar";
import * as Vue from "vue";
import Utils from "../../common/js/utils";

Vue.filter("getPermission", function(permission) {
  switch (permission) {
    case 0:
      return "校外人士";
    case 1:
      return "教职员工";
    case 2:
      return "在校学生";
  }
});

Vue.filter("getIdentity", function(identity) {
  if (identity === "NULL") return "未绑定";
  else return identity;
});

export default {
  name: "App",
  components: { SideBar, Heading, OrderCard },

  created() {
    Utils.post(this, "/a/user/list/", null, function(_this, res) {
      if (res.code === 0) {
        _this.$message.error("获取用户信息失败");
      } else {
        _this.user_list = res.data.user_list;
      }
    });
  },

  data() {
    return {
      id_type_selected: "0",

      is_modified: false,

      select_all: true,

      dialog_visible: false,

      user_list: [],

      // 筛选信息
      filter_info: {
        user_id: "",
        order_permission: null,
        permission: null
      }
    };
  },

  methods: {
    // 点击全选
    selectALlChange: function(status) {
      let len = this.user_list.length;
      for (let i = 0; i < len; i++) this.user_list[i].order_permission = status;
      this.is_modified = true;
    },

    // 点击单个选择
    selectChange: function() {
      this.is_modified = true;
    },

    // 响应筛选条件变化
    handleFilter: function() {
      let data = {};
      let keys = Object.keys(this.filter_info);
      for (let i = 0; i < keys.length; i++) {
        let key = keys[i];
        if (this.filter_info[key] !== "" && this.filter_info[key] !== null) {
          if (key === "user_id") {
            if (this.id_type_selected === "0")
              data.identity = this.filter_info.user_id;
            else data.user_id = this.filter_info.user_id;
          } else data[key] = this.filter_info[key];
        }
      }

      Utils.post(this, "/a/user/list/", data, function(_this, res) {
        if (res.code === 0) {
          _this.$message.error("获取用户信息失败");
        } else {
          _this.user_list = res.data.user_list;
        }
      });

      this.is_modified = false;
    },

    // 响应权限修改
    handlePermissionChange: function() {
      Utils.post(this, "/a/user/edit/", { user_list: this.user_list }, function(
        _this,
        res
      ) {
        if (res.code === 0) {
          _this.$message.error("修改用户信息失败");
        } else {
          Utils.post(_this, "/a/user/list/", null, function(_this, res) {
            if (res.code === 0) {
              _this.$message.error("获取用户信息失败");
            } else {
              _this.user_list = res.data.user_list;
            }
          });

          _this.dialog_visible = false;
          _this.is_modified = false;
        }
      });
    }
  }
};
</script>

<style scoped>
.side-bar {
  margin-right: 1rem;
  min-width: 13rem;
}

.select-panel div {
  font-size: medium !important;
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

.line {
  border-color: #eceff1 !important;
  margin-top: 3rem;
  margin-bottom: 3rem;
}
</style>

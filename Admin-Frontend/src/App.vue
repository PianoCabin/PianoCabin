<template>
  <div id="app">
    <div v-if="!is_login" id="login">
      <div id="login-body">
        <el-form label-width="60px">
          <el-form-item label="用户名" style="font-weight: bold;">
            <el-input v-model="username"  placeholder="请输入用户名" />
          </el-form-item>
          <el-form-item label="密码" style="font-weight: bold;">
            <el-input v-model="password"  :type="password_type" placeholder="请输入密码">
              <i slot="suffix" class="el-icon-view" v-on:mousedown="showPassword" v-on:mouseup="hidePassword" v-on:mouseout="hidePassword"
                 style="font-size: 17px;vertical-align: middle;cursor:pointer;"></i>
            </el-input>
          </el-form-item>
          <el-button type="primary" v-on:click="login">登录</el-button>
        </el-form>
      </div>
    </div>
    <div v-else>
      <el-header style="text-align: right; font-size: 12px"></el-header>
      <el-container style="border: 1px solid #eee">
        <el-aside width="200px" style="background-color: rgb(238, 241, 246)">
          <el-menu :default-openeds="['1', '3']">
            <el-submenu index="1">
              <template slot="title">
                <i class="el-icon-menu" v-on:click="pianoList">
                </i>
                主页
              </template>
              <el-menu-item-group>
                <el-menu-item index="1-1" class="el-icon-edit-outline" v-on:click="pianoList"> 琴房列表</el-menu-item>
                <el-menu-item index="1-2" class="el-icon-edit-outline" v-on:click="newPiano"> 新建琴房</el-menu-item>
              </el-menu-item-group>
            </el-submenu>
            <el-menu-item index="5" @click="orderList">
              <template slot="title">
                <i class="el-icon-menu"></i>
                订单管理
              </template>
            </el-menu-item>
            <el-submenu index="2">
              <template slot="title">
                <i class="el-icon-bell"></i>
                通知
              </template>
              <el-menu-item-group>
                <el-menu-item index="2-1" class="el-icon-edit-outline" v-on:click="noticeList"> 通知列表</el-menu-item>
                <el-menu-item index="2-2" class="el-icon-edit-outline" v-on:click="newNotice"> 新建通知</el-menu-item>
              </el-menu-item-group>
            </el-submenu>
            <el-menu-item index="3" @click="receiveMessage">
              <template slot="title">
                <i class="el-icon-message"></i>
                反馈信息
              </template>
            </el-menu-item>
            <el-menu-item index="4" @click="updateUserMessage">
              <template slot="title">
                <i class="el-icon-setting"></i>
                更新用户身份
              </template>
            </el-menu-item>
          </el-menu>
        </el-aside>
        <el-container>
          <div v-if="page_type === 'piano_list'" class="main_paint">
            <div v-if="!piano_details_show && (page_type === 'piano_list')">
              <el-main>
                <el-tabs v-model="active_piano_type">
                  <el-tab-pane label="钢琴" name="first" id="piano1">
                    <el-row v-for="(value, key) in piano_list['钢琴']" :key="key">
                      <div style="padding: 14px;">
                        <span>{{ key }}</span>
                      </div>
                      <el-col :span="3" v-for="(item, index) in value" :key="index" :offset="index > 0 ? 1 : 0">
                        <el-card class="piano_card" shadow="hover" :body-style="{ padding: '0px' }">
                          <img src="/static/piano.png" class="image" v-on:click="pianoDetails(item, key, '钢琴')">
                          <div style="padding: 8px;">
                            <span style="font-size: 20px">{{ item.room_num }}</span>
                            <span v-if="item.online === 1">上线</span>
                            <span v-else>下线</span>
                            <span>
                              <el-popover placement="top" width="160" v-model="delete_visible['钢琴'][key][index]">
                                <p>确定删除该琴房吗？</p>
                                <div style="text-align: right; margin: 0">
                                  <!--<el-button size="mini" type="text" @click="delete_visible[key][index] = false">取消</el-button>-->
                                  <el-button type="primary" size="mini" @click="delete_visible[key][index] = false;deletePianoRoom('钢琴', item.room_num, key, index)">确定</el-button>
                                </div>
                                <el-button slot="reference" type="text" class="delete">删除</el-button>
                                </el-popover>
                            </span>
                          </div>
                        </el-card>
                      </el-col>
                    </el-row>
                  </el-tab-pane>
                  <el-tab-pane label="电子琴" name="second" id="piano2">
                    <el-row v-for="(value, key) in piano_list['电子琴']" :key="key">
                      <div style="padding: 14px;">
                        <span>{{ key }}</span>
                      </div>
                      <el-col :span="3" v-for="(item, index) in value" :key="index" :offset="index > 0 ? 1 : 0">
                        <el-card class="piano_card" shadow="hover" :body-style="{ padding: '0px' }">
                          <img src="/static/piano.png" class="image" v-on:click="pianoDetails(item, key, '电子琴')">
                          <div style="padding: 8px;">
                            <span style="font-size: 20px">{{ item.room_num }}</span>
                            <span v-if="item.online === 1">上线</span>
                            <span v-else>下线</span>
                            <span>
                              <el-popover placement="top" width="160" v-model="delete_visible['电子琴'][key][index]">
                                <p>确定删除该琴房吗？</p>
                                <div style="text-align: right; margin: 0">
                                  <!--<el-button size="mini" type="text" @click="delete_visible[key][index] = false">取消</el-button>-->
                                  <el-button type="primary" size="mini" @click="delete_visible[key][index] = false;deletePianoRoom('电子琴', item.room_num, key, index)">确定</el-button>
                                </div>
                                <el-button slot="reference" type="text" class="delete">删除</el-button>
                                </el-popover>
                            </span>
                          </div>
                        </el-card>
                      </el-col>
                    </el-row>
                  </el-tab-pane>
                  <el-tab-pane label="小琴屋" name="third" id="piano3">
                    <el-row v-for="(value, key) in piano_list['小琴屋']" :key="key">
                      <div style="padding: 14px;">
                        <span>{{ key }}</span>
                      </div>
                      <el-col :span="3" v-for="(item, index) in value" :key="index" :offset="index > 0 ? 1 : 0">
                        <el-card class="piano_card" shadow="hover" :body-style="{ padding: '0px' }">
                          <img src="/static/piano.png" class="image" v-on:click="pianoDetails(item, key, '小琴屋')">
                          <div style="padding: 8px;">
                            <span style="font-size: 20px">{{ item.room_num }}</span>
                            <span v-if="item.online === 1">上线</span>
                            <span v-else>下线</span>
                            <span>
                              <el-popover placement="top" width="160" v-model="delete_visible['小琴屋'][key][index]">
                                <p>确定删除该琴房吗？</p>
                                <div style="text-align: right; margin: 0">
                                  <!--<el-button size="mini" type="text" @click="delete_visible[key][index] = false">取消</el-button>-->
                                  <el-button type="primary" size="mini" @click="delete_visible[key][index] = false;deletePianoRoom('小琴屋', item.room_num, key, index)">确定</el-button>
                                </div>
                                <el-button slot="reference" type="text" class="delete">删除</el-button>
                                </el-popover>
                            </span>
                          </div>
                        </el-card>
                      </el-col>
                    </el-row>
                  </el-tab-pane>
                </el-tabs>
              </el-main>
            </div>
            <div v-if="piano_details_show && (page_type === 'piano_list')"  id="piano_details">
              <el-main>
                <el-col :span="10" :offset="1">
                  <el-card shadow="always" style="padding: 0 30px 0 30px; margin-top: 10px">
                    <el-form :model="piano_details_form" :rules="rules" ref="piano_details_form" label-width="100px" class="create_notice_form">
                      <el-form-item label="房间号">{{ piano_details_form.room_num }}</el-form-item>
                      <el-form-item label="琴品牌" prop="brand">
                        <el-select v-model="piano_details_form.brand" placeholder="请选择琴类型">
                          <el-option label="雅马哈立式钢琴" value="yamaha"></el-option>
                          <el-option label="卡瓦伊立式钢琴" value="kawayi"></el-option>
                          <el-option label="星海立式钢琴" value="xinghai"></el-option>
                          <el-option label="电子琴" value="electronic_organ"></el-option>
                        </el-select>
                      </el-form-item>
                      <el-form-item label="琴房类型" prop="piano_type">
                        <el-select v-model="piano_details_form.piano_type" placeholder="请选择琴房类型">
                          <el-option label="钢琴" value="piano_house"></el-option>
                          <el-option label="电子琴" value="electronic_organ_house"></el-option>
                          <el-option label="小琴屋" value="ordinary_house"></el-option>
                        </el-select>
                      </el-form-item>
                      <div style="font-weight: bold;">价格</div>
                      <el-form-item label="未绑定用户" prop="price_0">
                        <el-input v-model.number="piano_details_form.price_0" autocomplete="off" class="price_input"></el-input>
                        <span>元 / 小时</span>
                      </el-form-item>
                      <el-form-item label="教师" prop="price_1">
                        <el-input v-model.number="piano_details_form.price_1" autocomplete="off" class="price_input"></el-input>
                        <span>元 / 小时</span>
                      </el-form-item>
                      <el-form-item label="学生" prop="price_2">
                        <el-input v-model.number="piano_details_form.price_2" autocomplete="off" class="price_input"></el-input>
                        <span>元 / 小时</span>
                      </el-form-item>
                      <el-form-item label="状态" prop="is_online">
                        <el-radio-group v-model="piano_details_form.is_online">
                          <el-radio label="上线"></el-radio>
                          <el-radio label="下线"></el-radio>
                        </el-radio-group>
                      </el-form-item>
                      <el-form-item label="艺术团专用" prop="art_ensemble">
                        <el-radio-group v-model="piano_details_form.art_ensemble">
                          <el-radio label="是"></el-radio>
                          <el-radio label="否"></el-radio>
                        </el-radio-group>
                      </el-form-item>
                      <el-form-item>
                        <el-button type="primary" @click="editPianoDetails('piano_details_form')">保存</el-button>
                        <el-button @click="resetForm('piano_details_form')">重置</el-button>
                      </el-form-item>
                    </el-form>
                    <el-button type="primary" icon="el-icon-back" circle v-on:click="goBackPianoList"></el-button>
                  </el-card>
                </el-col>
              </el-main>
            </div>
          </div>
          <div v-else-if="page_type === 'new_piano'" class="main_paint">
            <el-main>
              <el-col :span="10" :offset="1">
                <el-card shadow="always" style="padding: 0 30px 0 30px; margin-top: 10px">
                  <el-form :model="piano_details_form" :rules="rules" ref="piano_details_form" label-width="100px" class="piano_details_form">
                    <el-form-item label="房间号" prop="room_num">
                      <el-input>
                        <el-input v-model="piano_details_form.room_num"></el-input>
                      </el-input>
                    </el-form-item>
                    <el-form-item label="琴品牌" prop="brand">
                      <el-select v-model="piano_details_form.brand" placeholder="请选择琴房类型">
                        <el-option label="雅马哈立式钢琴" value="yamaha"></el-option>
                        <el-option label="卡瓦伊立式钢琴" value="kawayi"></el-option>
                        <el-option label="星海立式钢琴" value="xinghai"></el-option>
                        <el-option label="电子琴" value="electronic_organ"></el-option>
                      </el-select>
                    </el-form-item>
                    <el-form-item label="琴房类型" prop="piano_type">
                      <el-select v-model="piano_details_form.piano_type" placeholder="请选择琴房类型">
                        <el-option label="钢琴房" value="piano_house"></el-option>
                        <el-option label="电子琴房" value="electronic_organ_house"></el-option>
                        <el-option label="小琴房" value="ordinary_house"></el-option>
                      </el-select>
                    </el-form-item>
                    <div style="font-weight: bold;">价格</div>
                    <el-form-item label="未绑定用户" prop="price_0">
                      <el-input v-model.number="piano_details_form.price_0" autocomplete="off" class="price_input"></el-input>
                      <span>元 / 小时</span>
                    </el-form-item>
                    <el-form-item label="教师" prop="price_1">
                      <el-input v-model.number="piano_details_form.price_1" autocomplete="off" class="price_input"></el-input>
                      <span>元 / 小时</span>
                    </el-form-item>
                    <el-form-item label="学生" prop="price_2">
                      <el-input v-model.number="piano_details_form.price_2" autocomplete="off" class="price_input"></el-input>
                      <span>元 / 小时</span>
                    </el-form-item>
                    <el-form-item label="状态" prop="is_online">
                      <el-radio-group v-model="piano_details_form.is_online">
                        <el-radio label="上线"></el-radio>
                        <el-radio label="下线"></el-radio>
                      </el-radio-group>
                    </el-form-item>
                    <el-form-item label="艺术团专用" prop="art_ensemble">
                      <el-radio-group v-model="piano_details_form.art_ensemble">
                        <el-radio label="是"></el-radio>
                        <el-radio label="否"></el-radio>
                      </el-radio-group>
                    </el-form-item>
                    <el-form-item>
                      <el-button type="primary" @click="createPianoRoom('piano_details_form')">立即创建</el-button>
                      <el-button @click="resetForm('piano_details_form')">重置</el-button>
                    </el-form-item>
                  </el-form>
                  <el-button type="primary" icon="el-icon-back" circle v-on:click="goBackPianoList"></el-button>
                </el-card>
              </el-col>
            </el-main>
          </div>
          <div v-else-if="page_type === 'order_list'" class="main_paint">
            <el-main>
              <el-tabs v-model="active_order_type">
                <el-tab-pane v-for="(value, key) in order_list" :key="key" :label="key" :name="order_list_name[key]">
                  <el-row>
                    <el-col :span="3" v-for="(item, index) in value" :key="index" :offset="index > 0 ? 1 : 0">
                      <el-card class="order_card" shadow="always" :body-style="{ padding: '0px' }">
                        <div style="padding: 8px;">
                          <span style="font-size: 20px">{{ item.brand }}</span>
                          <span>{{ item.room_num }}</span>
                        </div>
                        <div>
                          <span>预约人：</span>
                          <span>{{ item.user_id }}</span>
                        </div>
                        <div>
                          <span>预约日期：</span>
                        </div>
                        <div>
                          <span>预约时间：</span>
                          <span>{{ item.start_time }}</span>
                          <span>-</span>
                          <span>{{ item.end_time }}</span>
                        </div>
                        <div>
                          <span>状态：</span>
                          <span>{{ item.order_status }}</span>
                        </div>
                        <div>
                          <span>金额：</span>
                          <span>{{ item.price }}</span>
                        </div>
                      </el-card>
                    </el-col>
                  </el-row>
                </el-tab-pane>
                <!--<el-tab-pane label="未完成" name="second"></el-tab-pane>-->
                <!--<el-tab-pane label="已取消" name="third"></el-tab-pane>-->
              </el-tabs>
            </el-main>
          </div>
          <div v-else-if="!notice_details_show && page_type === 'notice_list'" class="main_paint">
            <el-main>
              <div>
              <el-row v-for="(item, index) in notice_list" :key="index">
                <el-card class="notice_card" shadow="always" :body-style="{ padding: '0px' }">
                  <div style="padding: 8px;">
                    <div slot="header">
                      <span>{{ item.news_title }}</span>
                    </div>
                    <div>
                      <span>发布时间：</span>
                      <span>{{ item.publish_time }}</span>
                    </div>
                  </div>
                </el-card>
              </el-row>
              </div>
            </el-main>
          </div>
          <div v-else-if="notice_details_show && page_type === 'notice_list'" class="main_paint">
            <el-container>
              <el-header>{{ this.message_details.title }}</el-header>
              <div style="float: right">{{ this.message_details.publish_time }}</div>
              <el-main>{{ this.message_details.content }}</el-main>
              <el-footer>
                <el-button type="primary" icon="el-icon-back" circle v-on:click="goBackNoticeList"></el-button>
              </el-footer>
            </el-container>
          </div>
          <div v-else-if="page_type === 'new_notice'" class="main_paint">
            <el-main>
              <el-form :model="notice_details_form" :rules="rules" ref="notice_details_form" label-width="100px" class="create_notice_form">
                <el-form-item label="活动名称" prop="title">
                  <el-input v-model="notice_details_form.title"></el-input>
                </el-form-item>
                <el-form-item label="正文" prop="content">
                  <el-input type="textarea" v-model="notice_details_form.content" id="new_notice_input"></el-input>
                </el-form-item>
                <el-form-item>
                  <el-button type="primary" @click="createNewNotice('notice_details_form')">立即创建</el-button>
                  <el-button @click="resetForm('notice_details_form')">重置</el-button>
                </el-form-item>
              </el-form>
            </el-main>
          </div>
          <div v-else-if="!feedback_message_details_show && page_type === 'receive_message'" class="main_paint">
            <el-main>
              <el-tabs v-model="active_message_type">
                <el-tab-pane label="未读" name="first">
                  <el-row v-for="(item, index) in feedback_message_list" :key="index">
                    <el-card class="message_card" shadow="always" :body-style="{ padding: '0px' }" @click="feedbackMessageDetails">
                      <div style="padding: 8px;">
                        <div slot="header">
                          {{ item.title }}
                        </div>
                        <div>
                          <span>反馈用户</span>
                          <span>{{ item.user_id }}</span>
                          <span>反馈时间</span>
                          <span>{{ item.time }}</span>
                        </div>
                      </div>
                    </el-card>
                  </el-row>
                </el-tab-pane>
                <el-tab-pane label="已读" name="second">
                  <el-row v-for="(item, index) in feedback_message_list" :key="index">
                    <el-card class="message_card" shadow="always" :body-style="{ padding: '0px' }">
                      <div style="padding: 8px;">
                        <div slot="header">
                          {{ item.title }}
                        </div>
                        <div>
                          <span>反馈用户</span>
                          <span>{{ item.user_id }}</span>
                          <span>反馈时间</span>
                          <span>{{ item.time }}</span>
                        </div>
                      </div>
                    </el-card>
                  </el-row>
                </el-tab-pane>
              </el-tabs>
            </el-main>
          </div>
          <div v-else-if="feedback_message_details_show && page_type === 'receive_message'" class="main_paint">
            <el-container>
              <el-header>{{ this.message_details.title }}</el-header>
              <div style="float: right">{{ this.message_details.publish_time }}</div>
              <el-main>{{ this.message_details.content }}</el-main>
              <el-footer>
                <span style="float: left">{{ this.message_details.user_id }}</span>
                <span style="float: right">
                  <el-button type="primary" icon="el-icon-back" circle v-on:click="goBackFeedbackMessageList"></el-button>
                </span>
              </el-footer>
            </el-container>
          </div>
        </el-container>
      </el-container>
    </div>
  </div>
</template>

<script>
export default {
  name: 'App',
  data () {
    return {
      is_login: false,
      username: '',
      password: '',
      password_type: 'password',
      page_type: 'piano_list',
      active_message_type: 'first',
      active_piano_type: 'first',
      active_order_type: 'first',
      piano_details_show: false,
      notice_details_show: false,
      update_user_confirm: false,
      feedback_message_details_show: false,
      delete_visible: {},
      notice_list: {},
      feedback_message_list: {},
      message_details: {},
      order_list: {},
      order_list_name: {
        '已完成': 'first',
        '未完成': 'second',
        '已取消': 'third'
      },
      piano_list: {},
      piano_details_form: {
        room_num: '',
        brand: '',
        piano_type: '',
        price_0: '',
        price_1: '',
        price_2: '',
        is_online: '',
        art_ensemble: '',
        old_piano_type: ''
      },
      notice_details_form: {
        title: '',
        content: ''
      },
      rules: {
        brand: [
          { required: false, trigger: 'change' }
        ],
        piano_type: [
          { required: true, message: '请选择琴房类型', trigger: 'change' }
        ],
        is_online: [
          { required: true, message: '请选择是否上线', trigger: 'change' }
        ],
        art_ensemble: [
          { required: true, message: '请选择是否为艺术团专用琴房', trigger: 'change' }
        ],
        price_0: [
          { required: true, message: '价格不能为空' },
          { type: 'number', message: '价格必须为数字值' }
        ],
        price_1: [
          { required: true, message: '价格不能为空' },
          { type: 'number', message: '价格必须为数字值' }
        ],
        price_2: [
          { required: true, message: '价格不能为空' },
          { type: 'number', message: '价格必须为数字值' }
        ],
        title: [
          { required: true, message: '请输入通知标题', trigger: 'blur' },
          { min: 3, max: 100, message: '长度在 3 到 100 个字符', trigger: 'blur' }
        ],
        time: [
          { type: 'date', required: true, message: '请选择时间', trigger: 'change' }
        ],
        data: [
          { type: 'date', required: true, message: '请选择日期', trigger: 'change' }
        ],
        content: [
          { required: true, message: '请输入通知标题', trigger: 'blur' },
          { min: 3, message: '长度大于 3 个字符', trigger: 'blur' }
        ],
        room_num: [
          { required: true, message: '请输入房间号', trigger: 'blur' }
        ]
      }
    }
  },
  created: function () {
    this.$http.get('/a/login').then(response => {
      let res = response.body
      this.is_login = res.code
      this.requestPianoDetails('钢琴')
      this.requestPianoDetails('电子琴')
      this.requestPianoDetails('小琴屋')
    }, response => {
      this.$message.error('服务器出错。')
    })
  },
  methods: {
    login: function () {
      // this.$http.get('/a/login', {
      //   params: {
      //     username: this.username,
      //     password: this.password
      //   },
      //   headers: {'X-Custom': '...'}
      // }).then(response => {
      //   console.log(response.body)
      // }, response => {
      //   // error callback
      // })
      this.$http.post('/a/login', {
        username: this.username,
        password: this.password
      }, {
        emulateJSON: true
      }).then(response => {
        let res = response.body
        if (res.code === 0) {
          this.$message.error('用户名或密码错误，请重新输入')
        } else {
          this.$message.success('登录成功')
          this.is_login = true
          this.requestPianoDetails('钢琴')
        }
      }, response => {
        this.$message.error('服务器出错。')
      })
    },
    requestPianoDetails: function (pianoType) {
      this.$http.post('/a/piano-room/list', {piano_type: pianoType}, {
        emulateJSON: true
      }).then(response => {
        let res = response.body
        if (res.code === 1) {
          let temp = this.piano_list
          this.piano_list = {}
          this.piano_list = temp
          this.piano_list[pianoType] = res.data.room_list
          this.delete_visible[pianoType] = []
          for (let key in this.piano_list[pianoType]) {
            this.delete_visible[pianoType][key] = []
            for (let i in this.piano_list[pianoType][key]) {
              this.delete_visible[pianoType][key][i] = false
            }
          }
        } else {
          this.$message.error(res.message)
        }
      }, response => {
        this.$message.error('服务器出错。')
      })
    },
    showPassword: function () {
      this.password_type = 'text'
    },
    hidePassword: function () {
      this.password_type = 'password'
    },
    pianoList: function () {
      this.page_type = 'piano_list'
      this.feedback_message_details_show = false
      this.piano_details_show = false
      this.notice_details_show = false
      this.update_user_confirm = false
    },
    newPiano: function () {
      this.piano_details_form.room_num = ''
      this.piano_details_form.brand = ''
      this.piano_details_form.piano_type = ''
      this.piano_details_form.price_0 = ''
      this.piano_details_form.price_1 = ''
      this.piano_details_form.price_2 = ''
      this.piano_details_form.is_online = ''
      this.piano_details_form.art_ensemble = ''
      this.page_type = 'new_piano'
      this.feedback_message_details_show = false
      this.piano_details_show = false
      this.notice_details_show = false
      this.update_user_confirm = false
    },
    orderList: function () {
      this.page_type = 'order_list'
      this.requestOrderDetails('已完成')
      this.requestOrderDetails('未完成')
      this.requestOrderDetails('已取消')
      this.feedback_message_details_show = false
      this.piano_details_show = false
      this.notice_details_show = false
      this.update_user_confirm = false
      console.log(this.page_type)
    },
    newNotice: function () {
      this.notice_details_form.title = ''
      this.notice_details_form.content = ''
      this.page_type = 'new_notice'
      this.feedback_message_details_show = false
      this.piano_details_show = false
      this.notice_details_show = false
      this.update_user_confirm = false
    },
    noticeList: function () {
      this.page_type = 'notice_list'
      this.requestNoticeList()
      this.feedback_message_details_show = false
      this.piano_details_show = false
      this.notice_details_show = false
      this.update_user_confirm = false
    },
    receiveMessage: function () {
      this.page_type = 'receive_message'
      this.feedback_message_details_show = false
      this.piano_details_show = false
      this.notice_details_show = false
      this.update_user_confirm = false
      this.requestFeedBackMessageList('已读')
      this.requestFeedBackMessageList('未读')
    },
    pianoDetails: function (item) {
      this.piano_details_form = {
        room_num: item.room_num,
        brand: item.brand,
        piano_type: item.piano_type,
        price_0: item.price_0,
        price_1: item.price_1,
        price_2: item.price_2,
        is_online: item.is_online ? '上线' : '下线',
        art_ensemble: item.art_ensemble ? '是' : '否',
        old_piano_type: item.piano_type
      }
      this.piano_details_show = true
    },
    feedbackMessageDetails: function (item) {
      this.$http.get('/a/news/detail', {
        params: {
          news_id: item.news_id
        },
        headers: {'X-Custom': '...'}
      }).then(response => {
        let res = response.body
        if (res.code === 1) {
          this.message_details.title = res.data.title
          this.message_details.content = res.data.content
          this.message_details.publish_time = res.data.publish_time
        } else {
          this.$message.error(res.message)
        }
      }, response => {
        this.$message.error('服务器出错。')
      })
      this.notice_details_show = true
    },
    goBackFeedbackMessageList: function () {
      this.page_type = 'receive_message'
      this.feedback_message_details_show = false
    },
    goBackPianoList: function () {
      this.page_type = 'piano_list'
      this.piano_details_show = false
    },
    editPianoDetails: function (formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          let data = {
            room_num: this.piano_details_form.room_num,
            brand: this.piano_details_form.brand,
            piano_type: this.piano_details_form.piano_type,
            price_0: this.piano_details_form.price_0,
            price_1: this.piano_details_form.price_1,
            price_2: this.piano_details_form.price_2,
            online: this.piano_details_form.is_online === '上线' ? 1 : 0,
            art_ensemble: this.piano_details_form.art_ensemble === '是' ? 1 : 0
          }
          this.$http.post('/a/piano-room/edit', data, {
            emulateJSON: true
          }).then(response => {
            let res = response.body
            if (res.code === 1) {
              this.$message(res.message)
              this.requestPianoDetails(this.piano_details_form.piano_type)
              this.requestPianoDetails(this.piano_details_form.old_piano_type)
              this.goBackPianoList()
            } else {
              this.$message.error(res.message)
            }
          }, response => {
            this.$message.error('服务器出错。')
          })
        } else {
          console.log('error submit!!')
          return false
        }
      })
    },
    updateUserMessage: function () {
      this.$confirm('此操作将更新用户信息, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.$message({
          type: 'success',
          message: '开始更新!'
        })
        this.$http.get('/a/user/update').then(response => {
          let res = response.body
          if (res.code === 1) {
          } else {
            this.$message.error(res.message)
          }
        }, response => {
          this.$message.error('服务器出错。')
        })
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '已取消更新'
        })
      })
    },
    resetForm: function (formName) {
      this.$refs[formName].resetFields()
    },
    downLine: function () {

    },
    getPianoDetails: function (piano) {
      this.$http.post('/a/piano-room/list', {
        piano_type: piano
      }, {
        emulateJSON: true
      }).then(response => {
        let res = response.body
        if (res.code === 0) {
          this.$message.error('获取琴房信息时出错！')
        } else {
          this.$message.success('更新成功！')
        }
      }, response => {
        this.$message.error('服务器出错。')
      })
    },
    deletePianoRoom: function (pianoType, num, key, index) {
      this.$http.post('/a/piano-room/delete', {
        room_num: num
      }, {
        emulateJSON: true
      }).then(response => {
        let res = response.body
        if (res.code === 0) {
          this.$message.error(res.message)
        } else {
          this.$message.success('删除成功！')
          this.piano_list[pianoType][key].splice(index, 1)
          this.delete_visible[pianoType][key].splice(index, 1)
        }
      }, response => {
        this.$message.error('服务器出错。')
      })
    },
    createPianoRoom: function (pianoDetails) {
      this.$refs[pianoDetails].validate(valid => {
        if (valid) {
          let data = {
            room_num: this.piano_details_form.room_num,
            brand: this.piano_details_form.brand,
            piano_type: this.piano_details_form.piano_type,
            price_0: this.piano_details_form.price_0,
            price_1: this.piano_details_form.price_1,
            price_2: this.piano_details_form.price_2,
            online: this.piano_details_form.is_online === '上线' ? 1 : 0,
            art_ensemble: this.piano_details_form.art_ensemble === '是' ? 1 : 0
          }
          this.$http.post('/a/piano-room/create', data, {
            emulateJSON: true
          }).then(response => {
            let res = response.body
            if (res.code === 1) {
              this.$message(res.message)
              this.requestPianoDetails(this.piano_details_form.piano_type)
              this.goBackPianoList()
            } else {
              this.$message.error(res.message)
            }
          }, response => {
            this.$message.error('服务器出错。')
          })
        } else {
          console.log('error submit!!')
          return false
        }
      })
    },
    createNewNotice: function (newDetails) {
      this.$refs[newDetails].validate(valid => {
        if (valid) {
          let data = {
            news_title: this.notice_details_form.title,
            news_content: this.notice_details_form.content
          }
          this.$http.post('/a/news/create', data, {
            emulateJSON: true
          }).then(response => {
            let res = response.body
            if (res.code === 1) {
              this.$message(res.message)
              this.noticeList()
            } else {
              this.$message.error(res.message)
            }
          }, response => {
            this.$message.error('服务器出错。')
          })
        } else {
          console.log('error submit!!')
          return false
        }
      })
    },
    goBackNoticeList: function () {
      this.page_type = 'notice_list'
      this.notice_details_show = false
    },
    requestNoticeList: function () {
      this.$http.get('/a/news/list').then(response => {
        console.log(response.body)
        let res = response.body
        if (res.code === 1) {
          let temp = this.news_list
          this.news_list = {}
          this.news_list = temp
          this.news_list = res.data.news_list
        } else {
          this.$message.error(res.message)
        }
      }, response => {
        this.$message.error('服务器出错。')
      })
    },
    requestOrderDetails: function (status) {
      this.$http.post('/a/order/list', {
        order_status: status === '未完成' ? 1 : (status === '已完成' ? 2 : 0)
      }, {
        emulateJSON: true
      }).then(response => {
        let res = response.body
        if (res.code === 1) {
          let temp = this.order_list
          this.order_list = {}
          this.order_list = temp
          this.order_list[status] = res.data.order_list
        } else {
          this.$message.error(res.message)
        }
      }, response => {
        this.$message.error('服务器出错。')
      })
    },
    requestFeedBackMessageList: function (status) {
      this.$http.post('/a/feedback/list', {
        read_status: status === '未读' ? 0 : 1
      }, {
        emulateJSON: true
      }).then(response => {
        let res = response.body
        if (res.code === 1) {
          let temp = this.feedback_message_list
          this.feedback_message_list = {}
          this.feedback_message_list = temp
          this.feedback_message_list[status] = res.data.feedback_message_list
        } else {
          this.$message.error(res.message)
        }
      }, response => {
        this.$message.error('服务器出错。')
      })
    }
  }
}

</script>

<style>
  body {
    margin: 0;
  }
  #new_notice_input {
    height: 400px;
  }
  #login {
    height: 100vh;
    overflow: hidden;
    background: url("./assets/background.jpeg") no-repeat center;
    background-size: contain;
    width: 100%;
  }
  .main_paint {
    width: 100%;
  }
  #login-body {
    background-color: rgba(25, 175, 225, 0.3);
    width: 250px;
    padding: 20px 15px 15px 10px;
    border-radius: 10px;
    position: absolute;
    left: 80%;
    top: 50%;
    text-align: center;
    transform: translate(-50%, -50%);
  }
  .el-header {
    background-color: #B3C0D1;
    color: #333;
    line-height: 60px;
  }
  .el-aside {
    color: #333;
    height: 100vh;
    overflow: hidden;
    width: 100%;
  }
  .piano_card {
    display: block;
  }
  .image {
    width: 100%;
    display: block;
  }
  .downLine {
    padding: 0;
    float: right;
  }
  .delete {
    padding: 0;
    float: right;
    color: red;
  }
  .delete:hover {
    color: crimson;
  }
  .price_input {
    width: 200px;
  }
</style>

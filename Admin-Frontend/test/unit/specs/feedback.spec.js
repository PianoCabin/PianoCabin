import App from '../../../src/module/feedback/App'
import Vue from 'vue'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import VueResource from 'vue-resource'
var expect = require('chai').expect;

/* eslint-disable no-new */

Vue.use(VueResource)
Vue.use(ElementUI)

window.test = true;

describe('反馈信息列表界面', () => {
  const vm = new Vue(App).$mount()

  it('检查内容为空时页面元素', () => {
    expect(vm.$el.querySelectorAll(".side-bar").length > 0).to.be.equal(true);
    expect(vm.$el.querySelectorAll(".select-panel").length > 0).to.be.equal(true);
    expect(vm.$el.querySelectorAll(".pagaination-div").length === 0).to.be.equal(true);
    expect(vm.$el.querySelectorAll(".pagination").length > 0).to.be.equal(true);
    expect(vm.$el.querySelectorAll(".feedback-content").length === 0).to.be.equal(true);
  });
  it('检查内容非空时全部信息列表显示', done => {
    vm.feedback_list = [{ user_id: "001", feedback_title: "test_title", feedback_content: "test_content", feedback_time: 1544369401, read_status: false },
        { user_id: "001", feedback_title: "test_title",feedback_content: "test_content", feedback_time: 1544369401, read_status: true }]
    vm.total_len = 2;
    Vue.nextTick(() => {
      expect(vm.$el.querySelectorAll(".pagination-div").length > 0).to.be.equal(true);
      expect(vm.$el.querySelectorAll(".feedback-content").length > 0).to.be.equal(true);
      expect(vm.$el.querySelectorAll("#pane-0 .el-table__row .el-table_1_column_1 .cell")[0].textContent).to.be.equal(vm.feedback_list[0].user_id);
      expect(vm.$el.querySelectorAll("#pane-0 .el-table__row .el-table_1_column_2 .cell")[0].textContent).to.be.equal(vm.feedback_list[0].feedback_title);
      expect(vm.$el.querySelectorAll("#pane-0 .el-table__row .el-table_1_column_3 .feedback-content")[0].textContent).to.be.equal("test_content");
      expect(vm.$el.querySelectorAll("#pane-0 .el-table__row .el-table_1_column_4 p")[0].textContent).to.be.equal('2018年12月9日 GMT+8下午11:30:01');
      done()
    })
  })
  it('检查内容非空时已读信息列表显示', done => {
    vm.read_feedback_list = [{ user_id: "001", feedback_title: "test_title", feedback_content: "test_content", feedback_time: 1544369401, read_status: true }]
    vm.total_len = 2;
    Vue.nextTick(() => {
      expect(vm.$el.querySelectorAll(".pagination-div").length > 0).to.be.equal(true);
      expect(vm.$el.querySelectorAll(".feedback-content").length > 0).to.be.equal(true);
      expect(vm.$el.querySelectorAll("#pane-0 .el-table__row .el-table_1_column_1 .cell")[0].textContent).to.be.equal(vm.read_feedback_list[0].user_id);
      expect(vm.$el.querySelectorAll("#pane-0 .el-table__row .el-table_1_column_2 .cell")[0].textContent).to.be.equal(vm.read_feedback_list[0].feedback_title);
      expect(vm.$el.querySelectorAll("#pane-0 .el-table__row .el-table_1_column_3 .feedback-content")[0].textContent).to.be.equal("test_content");
      expect(vm.$el.querySelectorAll("#pane-0 .el-table__row .el-table_1_column_4 p")[0].textContent).to.be.equal('2018年12月9日 GMT+8下午11:30:01');
      done()
    })
  })
  it('检查内容非空时未读信息列表显示', done => {
    vm.unread_feedback_list = [{ user_id: "001", feedback_title: "test_title", feedback_content: "test_content", feedback_time: 1544369401, read_status: false }]
    vm.total_len = 2;
    Vue.nextTick(() => {
      expect(vm.$el.querySelectorAll(".pagination-div").length > 0).to.be.equal(true);
      expect(vm.$el.querySelectorAll(".feedback-content").length > 0).to.be.equal(true);
      expect(vm.$el.querySelectorAll("#pane-0 .el-table__row .el-table_1_column_1 .cell")[0].textContent).to.be.equal(vm.unread_feedback_list[0].user_id);
      expect(vm.$el.querySelectorAll("#pane-0 .el-table__row .el-table_1_column_2 .cell")[0].textContent).to.be.equal(vm.unread_feedback_list[0].feedback_title);
      expect(vm.$el.querySelectorAll("#pane-0 .el-table__row .el-table_1_column_3 .feedback-content")[0].textContent).to.be.equal("test_content");
      expect(vm.$el.querySelectorAll("#pane-0 .el-table__row .el-table_1_column_4 p")[0].textContent).to.be.equal('2018年12月9日 GMT+8下午11:30:01');
      done()
    })
  })
})

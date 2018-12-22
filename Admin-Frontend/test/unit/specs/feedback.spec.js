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
    it('检查信息列表显示', done => {
        vm.feedback_detail = {
          feedback_list: [{ feedback_content: "test_content", feedback_time: 1544369401, read_status: false },
          { feedback_content: "test_content", feedback_time: 1544369401, read_status: true }],
          read_feedback_list: [{ feedback_content: "test_content", feedback_time: 1544369401, read_status: true }],
          unread_feedback_list: [{ feedback_content: "test_content", feedback_time: 1544369401, read_status: false }] };;
        vm.page_end = 1;
        vm.total_len = 2;
        console.log("hhhhhhhhhhhhhhhh")
        Vue.nextTick(() => {
          console.log("hhhhhhhhhhhhhhhh")
          console.log(vm.$el.querySelectorAll(".feedback-content").length)
          // expect(vm.$el.querySelectorAll(".pagaination-div").length > 0).to.be.equal(true);
          expect(vm.$el.querySelectorAll(".feedback-content").length === 0).to.be.equal(true);
          // expect(vm.$el.querySelectorAll("#pane-0 .el-table__row .el-table_1_column_3 .feedback-content")[0].text).to.be.equal("1test_content");
          done()
        })
    })
})
